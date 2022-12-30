import socket

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
                                            byteorder='big',
                                            signed=False)
        print(f'confusion_len: {self.confusion_len}')
        base += 1 + self.confusion_len

        self.uuid = data[base: base + 16].decode(encoding='utf-8')
        base += 16

        self.directive = int.from_bytes(data[base: base + 16],
                                        byteorder='big',
                                        signed=False)
        base += 1

        self.host = socket.inet_ntoa(data[base: base + 4])
        base += 4

        self.port = int.from_bytes(data[base: base + 2],
                                   byteorder='big',
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
                                            byteorder='big',
                                            signed=False)
        base += 1 + self.confusion_len

        self.payload = data[base:]


class BTP:
    @staticmethod
    def inbound_connect(client_socket: socket,
                        buf_size: Optional[int] = 8192) -> (str, int):
        print(f'inbound btp connecting, buf size is {buf_size}')
        req_data = client_socket.recv(buf_size)
        if req_data == b'':
            print('inbound connecting receiving none data')
            return

        btp_request = BTPRequest(req_data)
        print('resolve btp request', btp_request.host, btp_request.port)
        return btp_request.host, btp_request.port

    @staticmethod
    def encode_request(host: str,
                       port: int,
                       data: bytes):
        """
        :return: BTP form request
        """
        confusion = bytes(29)
        confusion_len = (29).to_bytes(1, 'big')
        uuid = bytes(16)
        # uuid = '01 6b 77 45 56 59 85 44-9f 80 f4 28 f7 d6 01 29'\
        #     .replace('-', '').replace(' ', '').encode(encoding='utf-8')
        directive = (0).to_bytes(1, 'big')
        print(f'outbound btp host {host}, port: {port}')
        host_bytes = socket.inet_aton(host)
        port_bytes = port.to_bytes(2, 'big')

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
        confusion = bytes(29)
        confusion_len = (29).to_bytes(1, 'big')
        return confusion_len + confusion + data
