import socket

from src.config import InboundConfig
from src.protocols import ProtocolEnum, HTTP, BTP


class Inbound:
    host: str
    port: int
    protocol: ProtocolEnum
    uuid: str
    socket: socket = None

    def __init__(self, config: InboundConfig):
        self.host = config.host
        self.port = config.port
        self.protocol = config.protocol
        self.uuid = config.uuid
        self.buff_size = config.buf_size

    def listen(self, socket_proxy):
        # listen to any connection to the inbound and get its socket
        self.socket, _ = socket_proxy.accept()

    def connect(self) -> (str, int, bytes):
        match self.protocol:
            case ProtocolEnum.HTTP:
                return HTTP.inbound_connect(self.socket,
                                            self.buff_size)
            case ProtocolEnum.BTP:
                return BTP.inbound_connect(self.socket,
                                           self.uuid,
                                           self.buff_size)

    def close(self):
        if self.socket is not None:
            self.socket.close()

    def create_fake_connection(self):
        HTTP.send_fake_response(self.socket)
