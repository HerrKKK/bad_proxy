import json
from typing import Optional

from protocol import ProtocolType


class BoundConfig:
    host: str
    port: int
    protocol: ProtocolType

    def __init__(self,
                 host: Optional[str] = None,
                 port: Optional[int] = None,
                 protocol: Optional[str] = None):
        self.host = host
        self.port = port
        self.protocol = ProtocolType.interpret_string(protocol)


class InboundConfig(BoundConfig):
    pass


class OutboundConfig(BoundConfig):
    pass


class Config:
    inbound_config: InboundConfig
    outbound_config: OutboundConfig


def read_config(filename: Optional[str] = 'config.json'):
    if filename is None:
        filename = 'config.json'

    config = Config()

    with open(filename, 'r') as f:
        text = f.read()
        config_json = json.loads(text)
        config.inbound_config = InboundConfig(**config_json['inbound'])
        config.outbound_config = OutboundConfig(**config_json['outbound'])
        print(f'use {filename} as config')

    return config
