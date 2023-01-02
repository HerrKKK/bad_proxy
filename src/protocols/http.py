import socket


class HttpRequest:
    method: bytes = None
    version: bytes = None
    req_uri: bytes = None
    headers: dict = {}

    def __init__(self, data: bytes):
        self.__parse(data)

    def __parse(self, data: bytes):
        """
        GET https://test.com HTTP/1.1\r\n
        Host: test.test.com\r\n
        Content-Type: text/html\r\n
        Cache-Control: max-age=0\r\n\r\n
        """
        req_line_end = data.find(b'\r\n')  # end of the request line
        header_end = data.find(b'\r\n\r\n')  # end of the header

        # Request-Line
        self.req_line = data[:req_line_end]
        # method request_uri version in request line
        self.method, self.req_uri, self.version = self.req_line.split()

        # Request Header Fields
        headers = data[req_line_end + 2: header_end]
        for header in headers.split(b'\r\n'):
            k, v = header.split(b': ')
            self.headers[k] = v
        self.host = self.headers.get(b'Host')
        self.req_data = data[header_end + 4:]


class HttpResponse:
    version: bytes = None
    status_code: bytes = None
    headers: dict = {}

    def __init__(self, data: bytes):
        self.__parse(data)

    def __parse(self, data: bytes):
        """
        HTTP/1.1 301 Moved Permanently\r\n
        Host: test.test.com\r\n
        Location: test.test.com\r\n
        Content-Type: text/html\r\n
        Cache-Control: max-age=0\r\n\r\n
        """
        resp_line_end = data.find(b'\r\n')  # end of the request line
        header_end = data.find(b'\r\n\r\n')  # end of the header

        # Request-Line
        self.resp_line = data[:resp_line_end]
        # method request_uri version in request line
        resp_line_tokens = self.resp_line.split(b' ')
        self.version, self.status_code = resp_line_tokens[0], resp_line_tokens[1]

        # Response Header Fields
        headers = data[resp_line_end + 2: header_end]
        for header in headers.split(b'\r\n'):
            k, v = header.split(b': ')
            self.headers[k] = v
        self.resp_data = data[header_end + 4:]


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
                        buf_size: int | None = 8192) -> (str, int, bytes):
        req_data = client_socket.recv(buf_size)
        if req_data == b'':
            print('inbound received none data')
            return None, None, None

        # parse http request
        http_packet = HttpRequest(req_data)

        # remove domain of proxy itself in payload
        proxy_domain = b'%s//%s' % (http_packet.req_uri.split(b'//')[0],
                                    http_packet.host)
        req_data = req_data.replace(proxy_domain, b'')

        # HTTP
        if http_packet.method in [b'GET', b'POST', b'PUT', b'DELETE', b'HEAD']:
            pass
        # HTTPS use connect to build TCP connection
        if http_packet.method == b'CONNECT':
            # HTTP/1.1 200 Connection Established\r\nConnection: Close\r\n\r\n
            success_msg = b'%s %d Connection Established\r\nConnection: close\r\n\r\n' \
                          % (http_packet.version, 200)
            client_socket.send(success_msg)  # connection built
            req_data = client_socket.recv(buf_size)
            # client will send tls data after recv success message

        # get target host and port
        target_host, target_port = http_packet.host.split(b':')\
            if b':' in http_packet.host else (http_packet.host, 80)

        if isinstance(target_port, bytes):
            target_port = int(target_port.decode())
        return target_host.decode(), target_port, req_data

    @staticmethod
    def reverse_inbound_connect(inbound_socket: socket,
                                buff_size: int | None = 8192) -> (str,
                                                                  int,
                                                                  bytes | HttpRequest):
        req_data = inbound_socket.recv(buff_size)
        if req_data == b'':
            print('inbound received none data')
            return None, None, None

        # parse http request
        http_packet = HttpRequest(req_data)
        target_host, target_port = http_packet.host.split(b':') \
            if b':' in http_packet.host else (http_packet.host, 80)

        if isinstance(target_port, bytes):
            target_port = int(target_port.decode())
        return target_host.decode(), target_port, req_data

    @staticmethod
    def reverse_outbound_connect(outbound_socket: socket,
                                 proxy_addr: bytes,
                                 target_addr: bytes,
                                 raw_data: bytes,
                                 buff_size: int | None = 8192) -> bytes:
        # replace domain of proxy itself to target
        rewritten_data = raw_data.replace(proxy_addr, target_addr)
        return rewritten_data

    @staticmethod
    def rewrite_redirect(outbound_socket: socket,
                         raw_data: bytes,
                         buff_size: int | None = 8192) -> bytes:
        pass

    @staticmethod
    def send_fake_response(server_socket: socket):
        headers = b'HTTP/1.1 200 OK\r\n' \
                + b'Content-Type: text/html\r\n' \
                + b'Content-Length: ' + str(len(HTTP.response_body)).encode() \
                + b'Connection: close \r\n\r\n'
        server_socket.send(headers + HTTP.response_body.encode())
