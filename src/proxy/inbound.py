import socket

from config import InboundConfig
from protocols import BTP, HTTP, ProtocolEnum


class Inbound:
    host: str
    port: int
    protocol: ProtocolEnum
    uuid: str
    socket: socket = None

    def __init__(self, config: InboundConfig):
        self.host = config.host
        self.port = config.port
        self.protocol = config.protocol
        self.uuid = config.uuid
        self.buff_size = config.buff_size

    def listen(self, socket_proxy):
        # listen to any connection to the inbound and get its socket
        self.socket, _ = socket_proxy.accept()

    def connect(self) -> (str, int, bytes):
        match self.protocol:
            case ProtocolEnum.HTTP:
                return HTTP.inbound_connect(self.socket,
                                            self.buff_size)
            case ProtocolEnum.BTP:
                return BTP.inbound_connect(self.socket,
                                           self.uuid,
                                           self.buff_size)

    def close(self):
        if self.socket is not None:
            self.socket.close()

    def send_fake_response(self):
        body = b'''
            <html><body><h1>404 not found</h1>
            <p>This route is deprecated, please visit https://wwr-blog.com/<p>
            </body></html>
        '''
        headers = (b'HTTP/1.1 200 OK\r\n'
                   + b'Content-Type: text/html\r\n'
                   + b'Content-Length: ' + str(len(body)).encode()
                   + b'Connection: close \r\n\r\n')
        self.socket.send(headers + body)
