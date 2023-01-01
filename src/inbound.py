import socket

from protocol import ProtocolType
from config import InboundConfig
from application_layer import HTTP, BTP, BTPException


class Inbound:
    host: str
    port: int
    protocol: ProtocolType
    uuid: str
    socket: socket

    def __init__(self, config: InboundConfig):
        self.host = config.host
        self.port = config.port
        self.protocol = config.protocol
        self.uuid = config.uuid
        self.socket_recv_buf_size = 8 * 1024

    def listen(self, socket_proxy: socket):
        """
        获取已经与代理端建立连接的客户端套接字，如无则阻塞，直到可以获取一个建立连接套接字
        返回：socket_client 代理端与客户端之间建立的套接字
        """
        self.socket, _ = socket_proxy.accept()

    def connect(self):
        print(f'inbound bound to {self.host}: {self.port}')
        match self.protocol:
            case ProtocolType.HTTP:
                return HTTP.inbound_connect(self.socket,
                                            self.socket_recv_buf_size)
            case ProtocolType.BTP:
                return BTP.inbound_connect(self.socket,
                                           self.uuid,
                                           self.socket_recv_buf_size)

    def close(self):
        if hasattr(self, 'socket') and self.socket is not None:
            self.socket.close()

    def create_fake_connection(self):
        HTTP.send_fake_response(self.socket)
