import socket

from src.protocols import HttpRequest, HttpResponse


class ReverseProxy:
    inbound_socket: socket
    outbound_socket: socket
    buff_size: int = 8192

    target_host: str
    target_port: int
    proxy_host: str
    proxy_port: int
    proxy_ip: int

    request_data: bytes = b''
    response_data: bytes = b''

    def __init__(self):
        self.bin_addr = self.proxy_host.encode()\
                        + b':' + str(self.proxy_port).encode()
        pass

    def inbound_connect(self):
        raw_data = self.inbound_socket.recv(self.buff_size)
        if raw_data == b'':
            print('inbound received none data')
            return

        # parse http request
        http_packet = HttpRequest(raw_data)

        # remove domain of proxy itself in payload
        self.request_data = raw_data.replace(http_packet.host,
                                             self.target_host.encode()
                                             + b':' + str(self.target_port).encode())
        self.inbound_socket.send(self.request_data)

    def outbound_connect(self):
        resp_data = self.outbound_socket.recv(self.buff_size)
        # if 301/302, get location and send request again:
        #    self.outbound()
        http_response = HttpResponse(resp_data)

        match http_response.status_code:
            case 200:
                self.response_data = resp_data.replace()
            case 301 | 302:
                # handle data
                self.outbound_connect()
            case _:
                raise Exception('failed')

    def proxy(self):
        self.inbound_connect()
        self.outbound_connect()
        pass

    def async_listen(self):
        # epoll
        pass
