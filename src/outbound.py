import ssl
import socket

from ssl import SSLContext
from typing import Optional

from protocols import ProtocolEnum
from config import OutboundConfig
from protocols import BTP


class Outbound:
    host: str
    port: int
    protocol: ProtocolEnum
    uuid: str
    tls: bool
    unsafe_socket: socket = None
    socket: socket = None
    context: SSLContext
    target_host: str
    target_port: int
    socket_recv_buf_size = 8 * 1024

    def __init__(self, config: OutboundConfig):
        self.host = config.host
        self.port = config.port
        self.protocol = config.protocol
        self.uuid = config.uuid
        self.tls = config.tls
        if self.tls is True:
            if hasattr(config, 'tls_root_ca_path') \
                    and config.tls_root_ca_path is not None:
                self.context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
                self.context.load_verify_locations(config.tls_root_ca_path)
            else:
                self.context = ssl.create_default_context()

    def socket_connect(self):
        # getaddrinfo -> [(family, socket_type, proto, canonname, target_addr),]
        host, port = self.host, self.port
        if self.protocol == ProtocolEnum.FREEDOM:
            print(f'outbound connect to {self.target_host}: {self.target_port}')
            host, port = self.target_host, self.target_port

        (family, socket_type, _, _, target_addr) = socket.getaddrinfo(host, port)[0]

        self.unsafe_socket = socket.socket(family, socket_type)
        self.unsafe_socket.setblocking(False)
        self.unsafe_socket.settimeout(5)
        self.unsafe_socket.connect(target_addr)
        self.socket = self.unsafe_socket

    def connect(self,
                target_host: str,
                target_port: int,
                payload: Optional[bytes] = b''):
        self.target_host = target_host  # hostname or address
        self.target_port = target_port

        self.socket_connect()

        if self.tls is True:
            self.socket = self.context.wrap_socket(self.unsafe_socket,
                                                   server_hostname=self.host)

        match self.protocol:
            case ProtocolEnum.BTP:
                if payload is None:
                    payload = ''
                payload = BTP.outbound_connect(self.socket,
                                               target_host,
                                               target_port,
                                               self.uuid) + payload

        # whether to send the first package from inbound
        if payload is not None:
            self.socket.send(payload)

    def close(self):
        if self.socket is not None:
            self.socket.close()
        if self.unsafe_socket is not None:
            self.unsafe_socket.close()
