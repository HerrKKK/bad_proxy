import json

from protocols import ProtocolEnum


class BoundConfig:
    host: str
    port: int
    protocol: ProtocolEnum
    uuid: str
    tls: bool


class InboundConfig(BoundConfig):
    tls_cert_path: str
    tls_key_path: str

    def __init__(self,
                 host: str | None = None,
                 port: int | None = None,
                 protocol: str | None = None,
                 uuid: str | None = None,
                 tls: bool | None = False,
                 tls_cert_path: str | None = None,
                 tls_key_path: str | None = None):
        self.host = host
        self.port = port
        self.protocol = ProtocolEnum.interpret_string(protocol)
        self.uuid = uuid.replace('-', '').replace(' ', '')\
            if uuid is not None else None
        self.tls = tls
        self.tls_cert_path = tls_cert_path
        self.tls_key_path = tls_key_path


class OutboundConfig(BoundConfig):
    tls_root_ca_path: str

    def __init__(self,
                 host: str | None = None,
                 port: int | None = None,
                 protocol: str | None = None,
                 uuid: str | None = None,
                 tls: bool | None = False,
                 tls_root_ca_path: str | None = None):
        self.host = host
        self.port = port
        self.protocol = ProtocolEnum.interpret_string(protocol)
        self.uuid = uuid.replace('-', '').replace(' ', '') \
            if uuid is not None else None
        self.tls = tls
        self.tls_root_ca_path = tls_root_ca_path


class Config:
    inbound_config: InboundConfig
    outbound_config: OutboundConfig


def read_config(filename: str | None = 'conf/config.json'):
    if filename is None:
        filename = 'config.json'

    config = Config()

    with open(filename, 'r') as f:
        text = f.read()
        config_json = json.loads(text)
        config.inbound_config = InboundConfig(**config_json['inbound'])
        config.outbound_config = OutboundConfig(**config_json['outbound'])

    return config
