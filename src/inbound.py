import socket

from protocol import ProtocolType
from config import InboundConfig
from application_layer import HTTP, BTP, BTPResponse


class Inbound:
    host: str
    port: int
    protocol: ProtocolType
    socket_proxy: socket
    socket: None

    def __init__(self, config: InboundConfig):
        self.host = config.host
        self.port = config.port
        self.protocol = config.protocol

        self.socket_proxy = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 将SO_REUSEADDR标记为True, 当socket关闭后，立刻回收该socket的端口
        self.socket_proxy.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket_proxy.bind((config.host, config.port))
        self.socket_proxy.listen(10)

        self.socket_recv_buf_size = 8 * 1024
        self.delay = 1/1000.0
        self.protocol = ProtocolType.HTTP

        print('info', 'bind=%s:%s' % (config.host, config.port))
        print('info', 'listen=%s' % 10)
        print('info', 'buf_size=%skb, delay=%sms' % (8, 1))

    def __del__(self):
        self.socket_proxy.close()

    def socket_accept(self):
        """
        获取已经与代理端建立连接的客户端套接字，如无则阻塞，直到可以获取一个建立连接套接字
        返回：socket_client 代理端与客户端之间建立的套接字
        """
        self.socket, _ = self.socket_proxy.accept()
        return self.socket

    def connect(self):
        match self.protocol:
            case ProtocolType.HTTP:
                return HTTP.inbound_connect(self.socket, self.socket_recv_buf_size)
            case ProtocolType.BTP:
                return BTP.inbound_connect(self.socket, self.socket_recv_buf_size)

    def recv(self):
        # decode request to next step, return raw data
        response_data = self.socket.recv(self.socket_recv_buf_size)
        match self.protocol:
            case ProtocolType.HTTP:
                return response_data
            case ProtocolType.BTP:
                return BTPResponse(response_data).payload

    def send(self, raw_data: bytes):
        # encode response to send
        match self.protocol:
            case ProtocolType.HTTP:
                return self.socket.send(raw_data)
            case ProtocolType.BTP:
                return self.socket.send(BTP.encode_response(raw_data))
