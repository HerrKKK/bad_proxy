import hmac
import socket
import secrets
import time

from uuid import UUID
from enum import IntEnum

secret_generator = secrets.SystemRandom()


class BTPRequest:
    body: bytes
    digest: bytes         # 32 Bytes
    timestamp: int        # 4 Bytes
    confusion_len: int    # 1 Byte
    confusion_msg: bytes  # [0, 48] Bytes
    directive: int        # 1 Bytes
    host_len: int         # 1 Byte
    host: str             # [1, 254) Bytes
    port: int             # 2 Bytes
    payload: bytes        # fixed length is 41

    def __init__(self, data):
        self.__parse(data)

    def __parse(self, data: bytes):
        base = 0

        self.digest = data[base: base + 32]
        base += 32
        self.body = data[base:]

        self.timestamp = int.from_bytes(data[base: base + 4],
                                        byteorder='big',
                                        signed=False)
        if abs(int(time.time()) - self.timestamp) > 180:
            raise BTPException('timeout')
        base += 4

        self.confusion_len = int.from_bytes(data[base: base + 1],
                                            byteorder='big',
                                            signed=False)
        base += 1 + self.confusion_len

        self.directive = int.from_bytes(data[base: base + 1],
                                        byteorder='big',
                                        signed=False)
        base += 1

        self.host_len = int.from_bytes(data[base: base + 1],
                                       byteorder='big',
                                       signed=False)
        base += 1

        self.host = data[base: base + self.host_len].decode(encoding='utf-8')
        base += self.host_len

        self.port = int.from_bytes(data[base: base + 2],
                                   byteorder='big',
                                   signed=False)
        base += 2

        if base - self.confusion_len - self.host_len != 41:
            raise BTPException('wrong btp request length')
        self.payload = data[base:]


class BTPResponse:
    confusion_len: int
    confusion_msg: bytes
    payload: bytes

    def __init__(self, data):
        self.__parse(data)

    def __parse(self, data: bytes):
        base = 0

        self.confusion_len = int.from_bytes(data[:1],
                                            byteorder='big',
                                            signed=False)
        base += 1 + self.confusion_len

        self.payload = data[base:]


class BTPDirective(IntEnum):
    NONE = 0
    CONNECT = 1


class BTPException(Exception):
    def __init__(self, msg: str):
        super(msg)


class BTP:
    @staticmethod
    def inbound_connect(inbound_socket: socket,
                        inbound_uuid: str,
                        buf_size: int | None = 8192) -> (str, int, bytes):
        req_data = inbound_socket.recv(buf_size)
        if req_data == b'':
            print('inbound connecting receiving none data')
            return None, None, None

        btp_request = BTPRequest(req_data)

        if btp_request.digest != hmac.new(UUID(inbound_uuid).bytes,
                                          btp_request.body,
                                          'sha256').digest():
            raise BTPException('btp auth failure')
        if btp_request.directive != BTPDirective.CONNECT:
            raise BTPException('wrong directive')

        btp_token = secrets.token_bytes(nbytes=8)
        # the random token will be attached to the head of  the first package
        inbound_socket.send(BTP.encode_response(btp_token))
        req_data = inbound_socket.recv(buf_size)  # listen immediately

        if req_data[:8] != btp_token:
            raise BTPException('btp challenge failure')

        return btp_request.host.encode(),\
            btp_request.port,\
            req_data[8:]  # btp_request.payload

    @staticmethod
    def outbound_connect(outbound_socket: socket,
                         target_host: str,  # tell server to connect target host
                         target_port: int,
                         outbound_uuid: str,
                         buf_size: int | None = 8192) -> bytes:  # return first package
        btp_request = BTP.encode_request(target_host,
                                         target_port,
                                         outbound_uuid,
                                         BTPDirective.CONNECT)
        outbound_socket.send(btp_request)
        # return btp token, the challenge for protecting any replay
        return BTPResponse(outbound_socket.recv(buf_size)).payload

    @staticmethod
    def encode_request(host: str,
                       port: int,
                       uuid_str: str,
                       direct: BTPDirective = BTPDirective.CONNECT,
                       payload: bytes | None = b'') -> bytes:
        timestamp = (int(time.time()) + secret_generator.randint(0, 60) - 30)\
            .to_bytes(4, 'big')

        confusion_len = secret_generator.randint(7, 32)
        confusion = secrets.token_bytes(nbytes=confusion_len)
        confusion_len = confusion_len.to_bytes(1, 'big')

        directive = int(direct).to_bytes(1, 'big')
        host_bytes = host.encode(encoding='utf-8')
        host_len = len(host_bytes).to_bytes(1, 'big')
        port_bytes = port.to_bytes(2, 'big')

        body = timestamp \
            + confusion_len \
            + confusion \
            + directive \
            + host_len \
            + host_bytes \
            + port_bytes \
            + payload

        digest = hmac.new(UUID(uuid_str).bytes, body, 'sha256').digest()
        return digest + body

    @staticmethod
    def encode_response(data) -> bytes:
        """
        :param data: plain bytes
        :return: BTP form response
        """
        confusion_len = secret_generator.randint(32, 64)
        confusion = secrets.token_bytes(nbytes=confusion_len)
        confusion_len = confusion_len.to_bytes(1, 'big')
        return confusion_len + confusion + data