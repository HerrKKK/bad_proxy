import socket
import secrets
import hashlib
import uuid

from typing import Optional
from uuid import UUID
from enum import IntEnum

secret_generator = secrets.SystemRandom()


class BTPRequest:
    md5: bytes
    confusion_len: int
    confusion_msg: bytes
    uuid: str
    directive: int
    host_len: int
    host: str
    port: int
    payload: bytes

    def __init__(self, data):
        self.__parse(data)

    def __parse(self, data: bytes):
        assert len(data) > 54
        base = 0

        self.md5 = data[base: base + 16]
        base += 16
        assert self.md5 == hashlib.md5(data[base:]).digest()

        self.confusion_len = int.from_bytes(data[base: base + 1],
                                            byteorder='big',
                                            signed=False)
        base += 1 + self.confusion_len

        self.uuid = uuid.UUID(bytes=data[base: base + 16]).hex
        base += 16

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

        print(f'all len is {len(data)},',
              f'confusion len is {self.confusion_len},',
              f'host len is {self.host_len}',
              f'data len is {len(data) - base},')

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
    pass


class BTPException(Exception):
    pass


class BTP:
    @staticmethod
    def inbound_connect(inbound_socket: socket,  # inbound socket
                        inbound_uuid: str,
                        buf_size: Optional[int] = 8192) -> (str, int):
        req_data = inbound_socket.recv(buf_size)
        if req_data == b'':
            print('inbound connecting receiving none data')
            return None, None, None

        btp_request = BTPRequest(req_data)

        assert btp_request.uuid == inbound_uuid  # verify
        assert btp_request.directive == BTPDirective.CONNECT

        inbound_socket.send(BTP.encode_response('connected'.encode(encoding='utf-8')))
        req_data = inbound_socket.recv(buf_size)  # listen immediately

        return btp_request.host.encode(), btp_request.port, req_data  # btp_request.payload

    @staticmethod
    def outbound_connect(outbound_socket: socket,  # outbound socket
                         target_host: str,  # tell server to connect target host
                         target_port: int,
                         outbound_uuid: str,
                         buf_size: Optional[int] = 8192):
        btp_request = BTP.encode_request(target_host,
                                         target_port,
                                         outbound_uuid,
                                         BTPDirective.CONNECT)
        outbound_socket.send(btp_request)
        resp = outbound_socket.recv(buf_size)  # verify
        if BTPResponse(resp).payload.decode(encoding='utf-8') != 'connected':
            print(BTPResponse(resp).payload.decode(encoding='utf-8'))
            raise Exception('invalid btp connection')

    @staticmethod
    def encode_request(host: str,
                       port: int,
                       uuid_str: str,
                       direct: BTPDirective = BTPDirective.CONNECT,
                       payload: Optional[bytes] = b''):
        """
        :return: BTP form request
        """
        confusion_len = secret_generator.randint(7, 32)
        confusion = secrets.token_bytes(nbytes=confusion_len)

        confusion_len = confusion_len.to_bytes(1, 'big')
        uid = UUID(uuid_str).bytes
        # uuid = '01 6b 77 45 56 59 85 44-9f 80 f4 28 f7 d6 01 29'\
        #     .replace('-', '').replace(' ', '').encode(encoding='utf-8')
        directive = int(direct).to_bytes(1, 'big')
        host_bytes = host.encode(encoding='utf-8')
        host_len = len(host_bytes).to_bytes(1, 'big')
        port_bytes = port.to_bytes(2, 'big')

        body = confusion_len \
            + confusion \
            + uid \
            + directive \
            + host_len \
            + host_bytes \
            + port_bytes \
            + payload

        md5 = hashlib.md5(body).digest()
        return md5 + body

    @staticmethod
    def encode_response(data):
        """
        :param data: plain bytes
        :return: BTP form response
        """
        confusion_len = secret_generator.randint(7, 31)
        confusion = secrets.token_bytes(nbytes=confusion_len)
        confusion_len = confusion_len.to_bytes(1, 'big')
        return confusion_len + confusion + data
