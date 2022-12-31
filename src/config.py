import json
from typing import Optional

from protocol import ProtocolType


class BoundConfig:
    host: str
    port: int
    protocol: ProtocolType
    tls: bool

    def __init__(self,
                 host: Optional[str] = None,
                 port: Optional[int] = None,
                 protocol: Optional[str] = None,
                 tls: Optional[bool] = False,
                 **kwargs):
        self.host = host
        self.port = port
        self.protocol = ProtocolType.interpret_string(protocol)
        self.tls = tls


class InboundConfig(BoundConfig):
    tls_cert_path: str
    tls_key_path: str


class OutboundConfig(BoundConfig):
    tls_root_ca_path: str


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

        if config.inbound_config.tls is True \
            and 'tls_cert_path' in config_json['inbound'] \
                and 'tls_key_path' in config_json['inbound']:
            config.inbound_config.tls_cert_path = config_json['inbound']['tls_cert_path']
            config.inbound_config.tls_key_path = config_json['inbound']['tls_key_path']

        config.outbound_config = OutboundConfig(**config_json['outbound'])
        if config.outbound_config.tls is True \
                and 'tls_root_ca_path' in config_json['outbound']:
            config.outbound_config.tls_root_ca_path = config_json['outbound']['tls_root_ca_path']

        print(f'use {filename} as config')

    return config
