import socket

from protocol import ProtocolType
from config import InboundConfig
from application_layer import HTTP, BTP, BTPRequest


class Inbound:
    host: str
    port: int
    protocol: ProtocolType
    socket: socket

    def __init__(self, config: InboundConfig):
        self.host = config.host
        self.port = config.port
        self.protocol = config.protocol

        self.socket_recv_buf_size = 8 * 1024
        self.delay = 1/1000.0

        # print('info', 'bind=%s:%s' % (config.host, config.port))
        # print('info', 'listen=%s' % 10)
        # print('info', 'buf_size=%skb, delay=%sms' % (8, 1))

    def listen(self, socket_proxy: socket):
        """
        获取已经与代理端建立连接的客户端套接字，如无则阻塞，直到可以获取一个建立连接套接字
        返回：socket_client 代理端与客户端之间建立的套接字
        """
        self.socket, _ = socket_proxy.accept()

    def connect(self):
        # print(f'host: {self.host}, port: {self.port}, protocol: {self.protocol}')
        match self.protocol:
            case ProtocolType.HTTP:
                return HTTP.inbound_connect(self.socket, self.socket_recv_buf_size)
            case ProtocolType.BTP:
                return BTP.inbound_connect(self.socket, self.socket_recv_buf_size)

    def recv(self):
        # decode request to next step, return raw data
        request_data = self.socket.recv(self.socket_recv_buf_size)
        match self.protocol:
            case ProtocolType.HTTP:
                return request_data
            case ProtocolType.BTP:
                return BTPRequest(request_data).payload

    def send(self, raw_data: bytes):
        # encode response to send
        match self.protocol:
            case ProtocolType.HTTP:
                self.socket.send(raw_data)
                return
            case ProtocolType.BTP:
                return self.socket.send(BTP.encode_response(raw_data))
