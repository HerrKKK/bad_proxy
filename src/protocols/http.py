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
    redirect_header = b'HTTP/1.1 301 Moved Permanently\r\n' \
                    + b'Cache-Control: no-store\r\n' \
                    + b'Location: https://google.com/ \r\n\r\n'
    response_body = '''
        <html><body><h1>404 not found</h1>
        <p>This route is deprecated, please visit https://wwr-blog.com/<p>
        </body></html>
    '''

    @staticmethod
    def inbound_connect(client_socket: socket,
                        buf_size: Optional[int] = 8192) -> (str, int):
        req_data = client_socket.recv(buf_size)
        if req_data == b'':
            print('inbound received none data')
            return None, None, None

        # 解析http请求数据
        http_packet = HttpRequestPacket(req_data)

        # 修正http请求数据
        tmp = b'%s//%s' % (http_packet.req_uri.split(b'//')[0], http_packet.host)
        req_data = req_data.replace(tmp, b'')

        # HTTP
        if http_packet.method in [b'GET', b'POST', b'PUT', b'DELETE', b'HEAD']:
            pass
        # HTTPS，会先通过CONNECT方法建立TCP连接
        if http_packet.method == b'CONNECT':
            success_msg = b'%s %d Connection Established\r\nConnection: close\r\n\r\n' \
                          % (http_packet.version, 200)
            client_socket.send(success_msg)  # 完成连接，通知客户端
            req_data = client_socket.recv(buf_size)
            # 客户端得知连接建立，会将真实请求数据发送给代理服务端

        # 获取服务端host、port
        if b':' in http_packet.host:
            server_host, server_port = http_packet.host.split(b':')
        else:
            server_host, server_port = http_packet.host, 80

        if isinstance(server_port, bytes):
            server_port = int(server_port.decode())
        return server_host.decode(), server_port, req_data

    @staticmethod
    def send_fake_response(server_socket: socket):
        headers = b'HTTP/1.1 200 OK\r\n' \
                + b'Content-Type: text/html\r\n' \
                + b'Content-Length: ' + str(len(HTTP.response_body)).encode() \
                + b'Connection: close \r\n\r\n'
        server_socket.send(headers + HTTP.response_body.encode())
