import socket
import secrets
import uuid

from typing import Optional

secret_generator = secrets.SystemRandom()


class BTPRequest:
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
        base = 0

        self.confusion_len = int.from_bytes(data[:1],
                                            byteorder='big',
                                            signed=False)
        base += 1 + self.confusion_len

        self.uuid = uuid.UUID(bytes=data[base: base + 16]).hex
        base += 16

        self.directive = int.from_bytes(data[base: base + 16],
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
    def inbound_connect(client_socket: socket,  # inbound socket
                        buf_size: Optional[int] = 8192) -> (str, int):
        req_data = client_socket.recv(buf_size)
        if req_data == b'':
            print('inbound connecting receiving none data')
            return None, None, None

        btp_request = BTPRequest(req_data)
        req_data = None
        if btp_request.payload.decode(encoding='utf-8') == 'connect':
            client_socket.send(BTP.encode_response('connected'
                                                   .encode(encoding='utf-8')))
            req_data = client_socket.recv(buf_size)  # listen immediately
        return btp_request.host.encode(), btp_request.port, req_data  # btp_request.payload

    @staticmethod
    def outbound_connect(server_socket: socket,  # outbound socket
                         target_host: str,  # tell server to connect target host
                         target_port: int,
                         buf_size: Optional[int] = 8192):
        btp_request = BTP.encode_request(target_host,
                                         target_port,
                                         'connect'.encode(encoding='utf-8'))
        server_socket.send(btp_request)
        resp = server_socket.recv(buf_size)  # verify
        if BTPResponse(resp).payload.decode(encoding='utf-8') != 'connected':
            raise Exception('invalid btp connection')

    @staticmethod
    def encode_request(host: str,
                       port: int,
                       data: bytes):
        """
        :return: BTP form request
        """
        confusion_len = secret_generator.randint(11, 29)
        confusion = secrets.token_bytes(nbytes=confusion_len)
        assert len(confusion) == confusion_len

        confusion_len = confusion_len.to_bytes(1, 'big')
        uid = uuid.uuid4().bytes
        # uuid = '01 6b 77 45 56 59 85 44-9f 80 f4 28 f7 d6 01 29'\
        #     .replace('-', '').replace(' ', '').encode(encoding='utf-8')
        directive = (0).to_bytes(1, 'big')
        host_bytes = host.encode(encoding='utf-8')
        host_len = len(host_bytes).to_bytes(1, 'big')
        port_bytes = port.to_bytes(2, 'big')

        return confusion_len \
            + confusion \
            + uid \
            + directive \
            + host_len \
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
