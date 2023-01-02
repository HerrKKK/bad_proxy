import ssl
import socket

from ssl import SSLContext

from src.protocols import ProtocolEnum
from src.config import OutboundConfig
from src.protocols import BTP, HttpRequest, HTTP


class Outbound:
    host: str
    port: int
    protocol: ProtocolEnum
    uuid: str
    buff_size: int
    tls: bool
    unsafe_socket: socket = None
    socket: socket = None
    context: SSLContext
    target_host: str
    target_port: int
    reverse_target_addr: bytes  # without port
    proxy_addr: bytes   # with port

    def __init__(self, config: OutboundConfig):
        self.host = config.host
        self.port = config.port
        self.protocol = config.protocol
        self.uuid = config.uuid
        self.buff_size = config.buf_size

        self.tls = config.tls
        if self.tls is True:
            if config.tls_root_ca_path is not None:
                self.context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
                self.context.load_verify_locations(config.tls_root_ca_path)
            else:
                self.context = ssl.create_default_context()

    def socket_connect(self):
        # getaddrinfo -> [(family, socket_type, proto, canonname, target_addr),]
        host, port = self.host, self.port
        if self.protocol == ProtocolEnum.FREEDOM:
            host, port = self.target_host, self.target_port

        (family, socket_type, _, _, target_addr) = socket.getaddrinfo(host, port)[0]
        print(f'outbound connect to {target_addr}')

        self.unsafe_socket = socket.socket(family, socket_type)
        self.unsafe_socket.setblocking(False)
        self.unsafe_socket.settimeout(5)
        self.unsafe_socket.connect(target_addr)
        self.socket = self.unsafe_socket

    def connect(self,
                target_host: str | None = None,
                target_port: int | None = None,
                payload: bytes | None = b''):
        """
        :param target_host: The destination of the request
        :param target_port: The port of the request
        :param payload: The payload of the first package of request
        :return: NO RETURN
        """
        self.target_host = target_host  # hostname or address
        self.target_port = target_port

        self.socket_connect()

        if self.tls is True:
            self.socket = self.context.wrap_socket(self.unsafe_socket,
                                                   server_hostname=self.host)

        match self.protocol:
            case ProtocolEnum.BTP:
                assert target_host is not None and target_port is not None
                if payload is None:
                    payload = ''
                payload = BTP.outbound_connect(self.socket,
                                               target_host,
                                               target_port,
                                               self.uuid,
                                               self.buff_size) + payload
            case ProtocolEnum.REVERSE:
                self.reverse_target_addr = self.host.encode()
                self.proxy_addr = b'%s:%d' % (target_host.encode(), target_port)
                # rewrite url
                payload = HTTP.reverse_outbound_connect(self.socket,
                                                        self.proxy_addr,
                                                        self.reverse_target_addr,
                                                        payload,
                                                        self.buff_size)

        # whether to send the first package from inbound
        if payload is not None:
            self.socket.send(payload)

    def process(self, raw_data: bytes):
        if self.protocol is ProtocolEnum.REVERSE:
            return raw_data.replace(self.reverse_target_addr,
                                    self.proxy_addr)
        return raw_data

    def send(self, raw_data: bytes):
        if self.protocol is ProtocolEnum.REVERSE:
            raw_data = raw_data.replace(self.proxy_addr,
                                        self.reverse_target_addr)
        self.socket.send(raw_data)

    def fallback(self, raw_data: bytes):
        """
        Warning:
        This is invoked as active detection detected!
        The function discard the outbound,
        connect it to a preset host:port,
        the protocol will be changed to HTTP/RAW
        """
        target_host = b'google.com:80'
        self.protocol = ProtocolEnum.HTTP
        http_request = HttpRequest(raw_data)
        rewrite_data = raw_data.replace(http_request.host, target_host)
        self.socket.send(rewrite_data)
        resp_data = self.socket.recv(self.buff_size)

    def close(self):
        if self.socket is not None:
            self.socket.close()
        if self.unsafe_socket is not None:
            self.unsafe_socket.close()
