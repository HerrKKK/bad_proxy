import socket

from protocol import ProtocolType
from net_utils import HttpRequestPacket
from config import InboundConfig


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

    def http_connect(self) -> (str, int):
        req_data = self.socket.recv(self.socket_recv_buf_size)
        if req_data == b'':
            return

        # 解析http请求数据
        http_packet = HttpRequestPacket(req_data)

        # HTTP
        # if http_packet.method in [b'GET', b'POST', b'PUT', b'DELETE', b'HEAD']:
        #     pass
        # HTTPS，会先通过CONNECT方法建立TCP连接
        if http_packet.method == b'CONNECT':
            success_msg = b'%s %d Connection Established\r\nConnection: close\r\n\r\n' \
                          % (http_packet.version, 200)
            self.socket.send(success_msg)  # 完成连接，通知客户端
            # 客户端得知连接建立，会将真实请求数据发送给代理服务端

        # 获取服务端host、port
        if b':' in http_packet.host:
            server_host, server_port = http_packet.host.split(b':')
        else:
            server_host, server_port = http_packet.host, 80

        return server_host, server_port
