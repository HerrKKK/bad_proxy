import socket


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


def connect_socket(host, port) -> socket:
    # 解析DNS获取对应协议簇、socket类型、目标地址
    # getaddrinfo -> [(family, socket_type, proto, canonname, target_addr),]
    (family, socket_type, _, _, target_addr) = socket.getaddrinfo(host, port)[0]

    tmp_socket = socket.socket(family, socket_type)
    tmp_socket.setblocking(False)
    tmp_socket.settimeout(5)
    tmp_socket.connect(target_addr)
    return tmp_socket
