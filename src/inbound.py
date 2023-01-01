import socket

from protocol import ProtocolType
from config import InboundConfig
from application_layer import HTTP, BTP


class Inbound:
    host: str
    port: int
    protocol: ProtocolType
    uuid: str
    socket: socket = None

    def __init__(self, config: InboundConfig):
        self.host = config.host
        self.port = config.port
        self.protocol = config.protocol
        self.uuid = config.uuid
        self.socket_recv_buf_size = 8 * 1024

    def listen(self, socket_proxy):
        # listen to any connection to the inbound and get its socket
        self.socket, _ = socket_proxy.accept()

    def connect(self):
        match self.protocol:
            case ProtocolType.HTTP:
                return HTTP.inbound_connect(self.socket,
                                            self.socket_recv_buf_size)
            case ProtocolType.BTP:
                return BTP.inbound_connect(self.socket,
                                           self.uuid,
                                           self.socket_recv_buf_size)

    def close(self):
        if self.socket is not None:
            self.socket.close()

    def create_fake_connection(self):
        HTTP.send_fake_response(self.socket)
