from typing import Optional

from protocol import ProtocolType
from net_utils import connect_socket
from config import OutboundConfig
from application_layer import BTP, BTPResponse


class Outbound:
    host: str
    port: int
    protocol: ProtocolType
    socket: None

    def __init__(self, config: OutboundConfig):
        self.host = config.host
        self.port = config.port
        self.protocol = config.protocol

    def connect(self,
                server_host: Optional[str] = None,
                server_port: Optional[int] = None):
        if server_host is not None and server_port is not None:
            self.socket = connect_socket(server_host, server_port)
            return
        self.socket = connect_socket(self.host, self.port)

    def recv(self):
        # decode response to raw data
        response_data = self.socket.recv(8 * 1024)
        match self.protocol:
            case ProtocolType.HTTP:
                return response_data
            case ProtocolType.BTP:
                return BTPResponse(response_data).payload

    def send(self, raw_data: bytes):
        # encode request to outbound host/port
        match self.protocol:
            case ProtocolType.HTTP:
                return self.socket.send(raw_data)
            case ProtocolType.BTP:
                return self.socket.send(BTP.encode_request(self.host,
                                                           self.port,
                                                           raw_data))
