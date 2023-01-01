import ssl
import socket

from ssl import SSLContext
from typing import Optional

from protocol import ProtocolType
from net_utils import connect_socket
from config import OutboundConfig
from application_layer import BTP


class Outbound:
    host: str
    port: int
    protocol: ProtocolType
    uuid: str
    tls: bool
    unsafe_socket: socket
    socket: socket
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

    def connect(self,
                target_host: str,
                target_port: int,
                payload: Optional[bytes] = b''):
        self.target_host = target_host  # domain or address
        self.target_port = target_port

        if self.protocol == ProtocolType.FREEDOM:
            print(f'outbound connect to {self.target_host}: {self.target_port}')
            self.unsafe_socket = connect_socket(target_host, target_port)
        else:
            print(f'outbound connect to {self.host}: {self.port}')
            self.unsafe_socket = connect_socket(self.host, self.port)

        self.socket = self.unsafe_socket

        if self.tls is True:
            self.socket = self.context.wrap_socket(self.unsafe_socket,
                                                   server_hostname=self.host)

        match self.protocol:
            case ProtocolType.BTP:
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
        if hasattr(self, 'socket') and self.socket is not None:
            self.socket.close()
