import socket


class HttpRequest(object):
    method: bytes
    req_uri: bytes
    version: bytes
    headers: dict = {}
    host: bytes
    payload: bytes

    def __init__(self, data):
        self.__parse(data)

    def __parse(self, data):
        req_line_end = data.find(b'\r\n')
        headers_end = data.find(b'\r\n\r\n')

        # request line
        req_line = data[:req_line_end]
        self.method, self.req_uri, self.version = req_line.split()

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
                        buff_size: int | None = 8192) -> (str, int, bytes):
        raw_data = inbound_socket.recv(buff_size)
        if raw_data == b'':
            print('inbound received none data')
            return None, None, None

        http_packet = HttpRequest(raw_data)

        # remove proxy hostname
        tmp = b'%s//%s' % (http_packet.req_uri.split(b'//')[0], http_packet.host)
        raw_data = raw_data.replace(tmp, b'')

        # HTTP
        if http_packet.method in [b'GET', b'POST', b'PUT', b'DELETE', b'HEAD']:
            pass
        # HTTPS
        if http_packet.method == b'CONNECT':
            success_msg = b'%s %d Connection Established\r\nConnection: close\r\n\r\n' \
                          % (http_packet.version, 200)
            inbound_socket.send(success_msg)
            raw_data = inbound_socket.recv(buff_size)

        server_host, server_port = http_packet.host.split(b':') \
            if b':' in http_packet.host else (http_packet.host, 80)

        if isinstance(server_port, bytes):
            server_port = int(server_port.decode())
        return server_host.decode(), server_port, raw_data
