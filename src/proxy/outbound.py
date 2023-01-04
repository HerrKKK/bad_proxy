import ssl
import socket

from ssl import SSLContext

from protocols import ProtocolEnum
from config import OutboundConfig
from protocols import BTP, BTPDirective
from .domain_trie import DomainTrie


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

    def __init__(self, config: OutboundConfig):
        self.host = config.host
        self.port = config.port
        self.protocol = config.protocol
        self.uuid = config.uuid
        self.buff_size = config.buff_size

        self.tls = config.tls
        if self.tls is True:
            if config.tls_root_ca_path is not None:
                self.context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
                self.context.load_verify_locations(config.tls_root_ca_path)
            else:
                self.context = ssl.create_default_context()

    def socket_connect(self):
        # getaddrinfo -> [(family, socket_type, proto, canonname, target_addr),]
        (family, socket_type, _, _, target_addr) = socket.getaddrinfo(self.host, self.port)[0]

        self.unsafe_socket = socket.socket(family, socket_type)
        self.unsafe_socket.setblocking(False)
        self.unsafe_socket.settimeout(5)
        self.unsafe_socket.connect(target_addr)
        self.socket = self.unsafe_socket

    def connect(self,
                target_host: str,
                target_port: int,
                payload: bytes | None = b''):
        self.target_host = target_host  # hostname or address
        self.target_port = target_port

        # The domain trie will not init automatically, do not need to check if enabled
        if DomainTrie.get_instance().has_domain(self.target_host):
            self.protocol = ProtocolEnum.FREEDOM

        if self.protocol == ProtocolEnum.FREEDOM:
            self.host = self.target_host
            self.port = self.target_port
            print(f'outbound connect to {self.host}: {self.port}')

        self.socket_connect()

        if self.tls is True and self.protocol is not ProtocolEnum.FREEDOM:
            self.socket = self.context.wrap_socket(self.unsafe_socket,
                                                   server_hostname=self.host)

        if self.protocol is ProtocolEnum.BTP:
            payload = BTP.encode_request(target_host,
                                         target_port,
                                         self.uuid,
                                         BTPDirective.CONNECT,
                                         payload)

        # whether to send the first package from inbound
        if payload is not None:
            self.socket.send(payload)

    def close(self):
        if self.socket is not None:
            self.socket.close()
        if self.unsafe_socket is not None:
            self.unsafe_socket.close()
