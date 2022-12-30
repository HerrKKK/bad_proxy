from typing import Optional

from protocol import ProtocolType
from net_utils import connect_socket
from config import OutboundConfig
from application_layer import BTP


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

        match self.protocol:
            case ProtocolType.FREEDOM:
                print(f'outbound connect to freedom {target_host}: {target_port}')
                self.socket = connect_socket(target_host, target_port)
            case ProtocolType.BTP:
                print(f'outbound connect to btp {self.host}: {self.port}')
                self.socket = connect_socket(self.host, self.port)
                BTP.outbound_connect(self.socket, target_host, target_port)
            case _:
                self.socket = connect_socket(self.host, self.port)

        # whether to send the first package
        if payload is not None:
            self.send(payload)

    def recv(self):
        # decode response to raw data
        response_data = self.socket.recv(8 * 1024)
        match self.protocol:
            case ProtocolType.HTTP:
                return response_data
            case ProtocolType.BTP:
                return response_data
                # return BTPResponse(response_data).payload
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
                self.socket.send(raw_data)
                # host not right! use those from http request!
                # self.socket.send(BTP.encode_request(self.target_host,
                #                                     self.target_port,
                #                                     raw_data))
                return
            case ProtocolType.FREEDOM:
                self.socket.send(raw_data)
                return
