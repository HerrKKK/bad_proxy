from typing import Optional

from protocol import ProtocolType
from net_utils import connect_socket


class Outbound:
    host: str
    port: int
    protocol: ProtocolType
    socket: None

    def __init__(self):
        self.protocol = ProtocolType.FREEDOM

    def connect(self,
                server_host: Optional[str] = None,
                server_port: Optional[int] = None):
        if server_host is not None and server_port is not None:
            self.socket = connect_socket(server_host, server_port)
            return
        self.socket = connect_socket(self.host, self.port)
