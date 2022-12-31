import json
from typing import Optional

from protocol import ProtocolType


class BoundConfig:
    host: str
    port: int
    protocol: ProtocolType
    tls: bool


class InboundConfig(BoundConfig):
    tls_cert_path: str
    tls_key_path: str

    def __init__(self,
                 host: Optional[str] = None,
                 port: Optional[int] = None,
                 protocol: Optional[str] = None,
                 tls: Optional[bool] = False,
                 tls_cert_path: Optional[str] = None,
                 tls_key_path: Optional[str] = None):
        self.host = host
        self.port = port
        self.protocol = ProtocolType.interpret_string(protocol)
        self.tls = tls
        self.tls_cert_path = tls_cert_path
        self.tls_key_path = tls_key_path


class OutboundConfig(BoundConfig):
    tls_root_ca_path: str

    def __init__(self,
                 host: Optional[str] = None,
                 port: Optional[int] = None,
                 protocol: Optional[str] = None,
                 tls: Optional[bool] = False,
                 tls_root_ca_path: Optional[str] = None):
        self.host = host
        self.port = port
        self.protocol = ProtocolType.interpret_string(protocol)
        self.tls = tls
        self.tls_root_ca_path = tls_root_ca_path


class Config:
    inbound_config: InboundConfig
    outbound_config: OutboundConfig


def read_config(filename: Optional[str] = 'conf/config.json'):
    if filename is None:
        filename = 'config.json'

    config = Config()

    with open(filename, 'r') as f:
        text = f.read()
        config_json = json.loads(text)
        config.inbound_config = InboundConfig(**config_json['inbound'])
        config.outbound_config = OutboundConfig(**config_json['outbound'])

    return config
