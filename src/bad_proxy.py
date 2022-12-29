import select

from inbound import Inbound
from outbound import Outbound
from protocol import ProtocolType
from config import Config


class BadProxy(object):
    """
    简单的HTTP代理
    客户端(client) <=> 代理端(proxy) <=> 服务端(server)
    """
    def __init__(self, config: Config):
        self.inbound = Inbound(config.inbound_config)
        self.outbound = Outbound(config.outbound_config)

    def proxy(self):
        """
        代理核心程序
        参数：socket_client 代理端与客户端之间建立的套接字
        """
        server_host, server_port = self.inbound.connect()

        if self.outbound.protocol == ProtocolType.FREEDOM:
            self.outbound.connect(server_host, server_port)

        self.outbound.connect()
        self.async_listen()

        # 使用select异步处理，不阻塞
    def async_listen(self):
        """
        使用select实现异步处理数据
        参数：socket_client 代理端与客户端之间建立的套接字
        参数：socket_server 代理端与服务端之间建立的套接字
        """
        _rlist = [self.inbound.socket, self.outbound.socket]
        is_recv = True
        while is_recv:
            try:
                rlist, _, elist = select.select(_rlist, [], [], 2)
                if elist:
                    break
                for tmp_socket in rlist:
                    is_recv = True
                    # 接收数据
                    data = tmp_socket.recv(self.inbound.socket_recv_buf_size)
                    if data == b'':
                        is_recv = False
                        continue

                    # socket_client状态为readable, 当前接收的数据来自客户端
                    if tmp_socket is self.inbound.socket:
                        self.outbound.socket.send(data)  # 将客户端请求数据发往服务端
                        # print('proxy', 'client -> server')

                    elif tmp_socket is self.outbound.socket:
                        self.inbound.socket.send(data)
                        # print('proxy', 'client <- server')

                # time.sleep(self.delay)  # 适当延迟以降低CPU占用
            except Exception as e:
                print(e)
                break

        self.inbound.socket.close()
        self.outbound.socket.close()
