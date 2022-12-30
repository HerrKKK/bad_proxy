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
    target_host: str
    target_port: int

    def __init__(self, config: OutboundConfig):
        self.host = config.host
        self.port = config.port
        self.protocol = config.protocol

    def connect(self,
                target_host: str,
                target_port: int,
                payload: Optional[bytes] = None):
        self.target_host = target_host  # domain or address
        self.target_port = target_port

        if self.protocol == ProtocolType.FREEDOM:
            print(f'outbound connect to target {target_host}: {target_port}')
            self.socket = connect_socket(target_host, target_port)
        else:
            print(f'outbound connect to assigned {self.host}: {self.port}')
            self.socket = connect_socket(self.host, self.port)
        if payload is not None:
            self.send(payload)

    def recv(self):
        # decode response to raw data
        response_data = self.socket.recv(8 * 1024)
        match self.protocol:
            case ProtocolType.HTTP:
                return response_data
            case ProtocolType.BTP:
                return BTPResponse(response_data).payload
            case ProtocolType.FREEDOM:
                # print('freedom data: ', response_data)
                return response_data

    def send(self, raw_data: bytes):
        # encode request to outbound host/port
        # print(f 'outbound send, protocol: {self.protocol}, data: {raw_data}')
        match self.protocol:
            case ProtocolType.HTTP:
                self.socket.send(raw_data)
                return
            case ProtocolType.BTP:
                # host not right! use those from http request!
                self.socket.send(BTP.encode_request(self.target_host,
                                                    self.target_port,
                                                    raw_data))
            case ProtocolType.FREEDOM:
                self.socket.send(raw_data)
                return
