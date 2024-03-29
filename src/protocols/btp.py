import hmac
import secrets
import socket
import time
from enum import IntEnum
from uuid import UUID

from .btp_lru import LRU


class BTPRequest:
    body: bytes
    digest: bytes  # 32 Bytes
    timestamp: int  # 4 Bytes
    confusion_len: int  # 1 Byte
    confusion_msg: bytes  # [0, 48] Bytes
    directive: int  # 1 Bytes
    host_len: int  # 1 Byte
    host: str  # [1, 254) Bytes
    port: int  # 2 Bytes
    payload: bytes  # fixed length is 41

    __startup_time: int = time.time()

    def __init__(self, data):
        self.__parse(data)

    def __parse(self, data: bytes):
        base = 0

        self.digest = data[base:base + 32]
        base += 32
        self.body = data[base:]

        self.confusion_len = int.from_bytes(
            data[base:base + 1], byteorder='big', signed=False
        )
        base += 1 + self.confusion_len

        self.timestamp = int.from_bytes(
            data[base:base + 4], byteorder='big', signed=False
        )
        if (
            self.timestamp < BTPRequest.__startup_time
            or abs(int(time.time()) - self.timestamp) > BTP.TIMEOUT
        ):
            raise BTPException('timeout', data)
        base += 4

        self.directive = int.from_bytes(
            data[base:base + 1], byteorder='big', signed=False
        )
        base += 1

        self.host_len = int.from_bytes(
            data[base:base + 1], byteorder='big', signed=False
        )
        base += 1

        self.host = data[base: base + self.host_len].decode(encoding='utf-8')
        base += self.host_len

        self.port = int.from_bytes(
            data[base:base + 2], byteorder='big', signed=False
        )
        base += 2

        if base - self.confusion_len - self.host_len != 41:
            raise BTPException('wrong btp request length', data)
        self.payload = data[base:]


class BTPResponse:
    confusion_len: int
    confusion_msg: bytes
    payload: bytes

    def __init__(self, data):
        self.__parse(data)

    def __parse(self, data: bytes):
        base = 0

        self.confusion_len = int.from_bytes(
            data[:1], byteorder='big', signed=False
        )
        base += 1 + self.confusion_len

        self.payload = data[base:]


class BTPDirective(IntEnum):
    NONE = 0
    CONNECT = 1


class BTPException(Exception):
    raw_data: bytes = None

    def __init__(self, msg: str, raw_data: bytes):
        super().__init__(msg)
        self.raw_data = raw_data


class BTP:
    TOKEN_LEN: int = 32
    REQUEST_CONFUSION_LEN = (0, 64)
    RESPONSE_CONFUSION_LEN = (64, 128)
    TIMEOUT = 210

    __secret_generator = secrets.SystemRandom()

    @staticmethod
    def inbound_connect(
        inbound_socket: socket,
        inbound_uuid: str,
        buff_size: int | None = 8192
    ) -> (str, int, bytes):
        raw_data = inbound_socket.recv(buff_size)
        if raw_data == b'':
            print('inbound connecting receiving none data')
            return None, None, None

        btp_request = BTPRequest(raw_data)

        if btp_request.digest != hmac.new(
            UUID(inbound_uuid).bytes,
            btp_request.body,
            'sha256'
        ).digest():
            raise BTPException('btp auth failure', raw_data)
        if btp_request.directive != BTPDirective.CONNECT:
            raise BTPException('wrong directive', raw_data)

        LRU.get_instance().add(btp_request.digest)

        return (btp_request.host.encode(),
                btp_request.port,
                btp_request.payload)  # to be sent immediately

    @classmethod
    def encode_request(
        cls,
        host: str,
        port: int,
        uuid_str: str,
        direct: BTPDirective = BTPDirective.CONNECT,
        payload: bytes | None = b''
    ) -> bytes:
        confusion_len = cls.__secret_generator.randint(
            *BTP.REQUEST_CONFUSION_LEN
        )
        confusion = secrets.token_bytes(nbytes=confusion_len)
        confusion_len = confusion_len.to_bytes(1, 'big')

        """
        vmess use time to calculate hash value and store
        all possible hash value in server to verify
        it's a bit hard to implement
        """
        timestamp = (
            int(time.time())
            + cls.__secret_generator.randint(0, 60)
            - 30
        ).to_bytes(4, 'big')

        directive = int(direct).to_bytes(1, 'big')
        host_bytes = host.encode(encoding='utf-8')
        host_len = len(host_bytes).to_bytes(1, 'big')
        port_bytes = port.to_bytes(2, 'big')

        body = (
            confusion_len
            + confusion
            + timestamp
            + directive
            + host_len
            + host_bytes
            + port_bytes
            + payload
        )

        digest = hmac.new(UUID(uuid_str).bytes, body, 'sha256').digest()
        return digest + body

    @classmethod
    def encode_response(cls, data) -> bytes:
        """
        :param data: plain bytes
        :return: BTP form response
        """
        confusion_len = cls.__secret_generator.randint(
            *BTP.RESPONSE_CONFUSION_LEN
        )
        confusion = secrets.token_bytes(nbytes=confusion_len)
        confusion_len = confusion_len.to_bytes(1, 'big')
        return confusion_len + confusion + data
