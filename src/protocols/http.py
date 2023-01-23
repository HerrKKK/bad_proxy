import socket


class HttpRequest(object):
    method: bytes
    req_uri: bytes
    version: bytes
    headers: dict = {}
    host: bytes
    payload: bytes

    __valid_methods: list[bytes] = [
        b'GET', b'HEAD', b'POST', b'PUT', b'DELETE',
        b'CONNECT', b'OPTIONS', b'TRACE', b'PATCH'
    ]

    def __init__(self, data):
        self.__parse(data)

    def __parse(self, data):
        req_line_end = data.find(b'\r\n')
        headers_end = data.find(b'\r\n\r\n')

        assert req_line_end > 0 and headers_end > 0

        # request line
        req_line = data[:req_line_end]
        self.method, self.req_uri, self.version = req_line.split()

        assert self.method in self.__valid_methods

        # request header
        headers = data[req_line_end + 2: headers_end]
        for header in headers.split(b'\r\n'):
            k, v = header.split(b': ')
            self.headers[k] = v
        self.host = self.headers.get(b'Host')
        self.payload = data[headers_end + 4:]


class HTTP:
    @staticmethod
    def inbound_connect(inbound_socket: socket,
                        buff_size: int | None = 8192
                        ) -> (str, int, bytes):
        raw_data = inbound_socket.recv(buff_size)
        if raw_data == b'':
            print('inbound received none data')
            return None, None, None

        http_request = HttpRequest(raw_data)

        # remove proxy hostname
        tmp = b'%s//%s' % (http_request.req_uri.split(b'//')[0],
                           http_request.host)
        raw_data = raw_data.replace(tmp, b'')

        # HTTPS
        if http_request.method == b'CONNECT':
            success_msg = (
                    b'%s %d Connection Established\r\nConnection: close\r\n\r\n'
                    % (http_request.version, 200)
            )
            inbound_socket.send(success_msg)
            raw_data = inbound_socket.recv(buff_size)

        server_host, server_port = (
            http_request.host.split(b':')
            if b':' in http_request.host
            else (http_request.host, 80)
        )

        if isinstance(server_port, bytes):
            server_port = int(server_port.decode())
        return server_host.decode(), server_port, raw_data
