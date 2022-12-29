import socket
import struct

from typing import Optional


class BTPRequest:
    confusion_len: int
    confusion_msg: bytes
    uuid: str
    directive: int
    host: str
    port: int
    payload: bytes

    def __init__(self, data):
        self.__parse(data)

    def __parse(self, data: bytes):
        base = 0

        self.confusion_len = int.from_bytes(data[:1],
                                            byteorder='little',
                                            signed=False)
        base += 1 + self.confusion_len

        self.uuid = data[base: base + 16].decode(encoding='utf-8')
        base += 16

        self.directive = int.from_bytes(data[base: base + 16],
                                        byteorder='little',
                                        signed=False)
        base += 1

        int_ip = int.from_bytes(data[base: base + 1],
                                byteorder='little',
                                signed=False)
        self.host = socket.inet_ntoa(struct.pack('I', socket.htonl(int_ip)))
        base += 1

        self.port = int.from_bytes(data[base: base + 2],
                                   byteorder='little',
                                   signed=False)
        base += 2

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
                                            byteorder='little',
                                            signed=False)
        base += 1 + self.confusion_len

        self.payload = data[base:]


class BTP:
    @staticmethod
    def inbound_connect(client_socket: socket,
                        buf_size: Optional[int] = 8192) -> (str, int):
        req_data = client_socket.recv(buf_size)
        if req_data == b'':
            return

        btp_request = BTPRequest(req_data)
        return btp_request.host, btp_request.port

    @staticmethod
    def encode_request(host: str,
                       port: int,
                       data: bytes):
        """
        :return: BTP form request
        """
        confusion = bytes('d49f8881148139a77be5d7d5b6561c58')
        confusion_len = len(confusion).to_bytes(1, 'little')
        uuid = '01 6b 77 45 56 59 85 44-9f 80 f4 28 f7 d6 01 29'\
            .replace('-', '').replace(' ', '').encode(encoding='utf-8')
        directive = (0).to_bytes(1, 'little')
        host_bytes = host.encode(encoding='utf-8')
        port_bytes = port.to_bytes(2, 'little')

        return confusion_len \
            + confusion \
            + uuid \
            + directive \
            + host_bytes \
            + port_bytes \
            + data

    @staticmethod
    def encode_response(data):
        """
        :param data: plain bytes
        :return: BTP form response
        """
        confusion = bytes('d49f8881148139a77be5d7d5b6561c58')
        confusion_len = len(confusion).to_bytes(1, 'little')
        return confusion_len + confusion + data
