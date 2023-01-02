import json

from protocols import ProtocolEnum


class BoundConfig:
    host: str
    port: int
    protocol: ProtocolEnum
    uuid: str
    tls: bool
    buf_size: int = 8 * 1024

    def __init__(self,
                 host: str = None,
                 port: int = None,
                 protocol: str = None,
                 uuid: str | None = None,
                 tls: bool | None = None):
        self.host = host
        self.port = port
        self.protocol = ProtocolEnum.interpret_string(protocol)
        self.uuid = uuid.replace('-', '').replace(' ', '') \
            if uuid is not None else None
        self.tls = tls


class InboundConfig(BoundConfig):
    tls_cert_path: str
    tls_key_path: str

    def __init__(self,
                 tls_cert_path: str | None = None,
                 tls_key_path: str | None = None,
                 **kwargs):
        super().__init__(**kwargs)
        self.tls_cert_path = tls_cert_path
        self.tls_key_path = tls_key_path


class OutboundConfig(BoundConfig):
    tls_root_ca_path: str
    fallback_host: str

    def __init__(self,
                 tls_root_ca_path: str | None = None,
                 fallback_host: str | None = None,
                 **kwargs):
        super().__init__(**kwargs)
        self.tls_root_ca_path = tls_root_ca_path
        self.fallback_host = fallback_host


class Config:
    inbound_config: InboundConfig
    outbound_config: OutboundConfig

    def __init__(self,
                 inbound: dict | None = None,
                 outbound: dict | None = None):
        self.inbound_config = InboundConfig(**inbound)
        self.outbound_config = OutboundConfig(**outbound)


def read_config(filename: str) -> Config | None:
    with open(filename, 'r') as f:
        text = f.read()
        config_json = json.loads(text)
        config = Config(**config_json)
        return config
