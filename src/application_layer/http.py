import socket

from typing import Optional


class HttpRequestPacket(object):
    # HTTP请求包
    def __init__(self, data):
        self.__parse(data)

    def __parse(self, data):
        """
        解析一个HTTP请求数据包
        GET https://test.wengcx.top/index.html
        HTTP/1.1\r\nHost: test.wwr-blog.top\r\nProxy-Connection: keep-alive\r\nCache-Control: max-age=0\r\n\r\n

        参数：data 原始数据
        """
        i0 = data.find(b'\r\n')  # 请求行与请求头的分隔位置
        i1 = data.find(b'\r\n\r\n')  # 请求头与请求数据的分隔位置

        # 请求行 Request-Line
        self.req_line = data[:i0]
        self.method, self.req_uri, self.version = self.req_line.split()  # 请求行由method、request uri、version组成

        # 请求头域 Request Header Fields
        self.req_header = data[i0+2:i1]
        self.headers = {}
        for header in self.req_header.split(b'\r\n'):
            k, v = header.split(b': ')
            self.headers[k] = v
        self.host = self.headers.get(b'Host')

        # 请求数据
        self.req_data = data[i1+4:]


class HTTP:
    @staticmethod
    def inbound_connect(client_socket: socket,
                        buf_size: Optional[int] = 8192) -> (str, int):
        print(f'inbound http connecting, buf size is {buf_size}')
        req_data = client_socket.recv(buf_size)
        if req_data == b'':
            print('inbound received none data')
            return

        # 解析http请求数据
        http_packet = HttpRequestPacket(req_data)

        # HTTPS，会先通过CONNECT方法建立TCP连接
        if http_packet.method == b'CONNECT':
            success_msg = b'%s %d Connection Established\r\nConnection: close\r\n\r\n' \
                          % (http_packet.version, 200)
            print('https connected')
            client_socket.send(success_msg)  # 完成连接，通知客户端
            # 客户端得知连接建立，会将真实请求数据发送给代理服务端

        # 获取服务端host、port
        if b':' in http_packet.host:
            server_host, server_port = http_packet.host.split(b':')
        else:
            server_host, server_port = http_packet.host, 80

        print(f'target host: {server_host}, {server_port}')
        return server_host.decode(), int(server_port.decode())
