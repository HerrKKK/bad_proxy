from __future__ import annotations
import re
import socket
import ssl

from config import OutboundConfig
from protocols import BTP, BTPDirective, ProtocolEnum


class Outbound:
    host: str
    port: int
    protocol: ProtocolEnum
    uuid: str
    buff_size: int
    tls: bool
    unsafe_socket: socket = None
    socket: socket = None
    context: ssl.SSLContext
    target_host: str
    target_port: int
    direct_connect_cn: bool = False

    def __init__(self, config: OutboundConfig):
        self.host = config.host
        self.port = config.port
        self.protocol = config.protocol
        self.uuid = config.uuid
        self.buff_size = config.buff_size
        self.direct_connect_cn = config.direct_connect_cn

        self.tls = config.tls
        if self.tls is True:
            if config.tls_root_ca_path is not None:
                self.context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
                self.context.load_verify_locations(config.tls_root_ca_path)
            else:
                self.context = ssl.create_default_context()

    def socket_connect(self):
        # getaddrinfo -> [(family, socket_type, proto, canonname, target_addr),]
        # if target
        (family,
         socket_type,
         _, _,
         target_addr) = socket.getaddrinfo(self.host, self.port)[0]

        self.unsafe_socket = socket.socket(family, socket_type)
        self.unsafe_socket.setblocking(False)
        self.unsafe_socket.settimeout(10)
        self.unsafe_socket.connect(target_addr)
        self.socket = self.unsafe_socket

    def connect(
        self,
        target_host: str,
        target_port: int,
        payload: bytes | None = b''
    ):
        self.target_host = target_host  # hostname or address
        self.target_port = target_port

        # The domain trie will not init automatically, do not need to check if enabled
        if (
            self.direct_connect_cn is True
            and DomainCache.get_instance().has_domain(self.target_host)
        ):
            self.protocol = ProtocolEnum.FREEDOM

        if self.protocol == ProtocolEnum.FREEDOM:
            self.host = self.target_host
            self.port = self.target_port
            print(f'outbound connect to {self.host}: {self.port}')

        self.socket_connect()

        if self.tls is True and self.protocol is not ProtocolEnum.FREEDOM:
            self.socket = self.context.wrap_socket(
                self.unsafe_socket, server_hostname=self.host
            )

        if self.protocol is ProtocolEnum.BTP:  # btp outbound connect
            payload = BTP.encode_request(
                target_host,
                target_port,
                self.uuid,
                BTPDirective.CONNECT,
                payload
            )

        # whether to send the first package from inbound
        if payload is not None:
            self.socket.send(payload)

    def close(self):
        if self.socket is not None:
            self.socket.close()
        if self.unsafe_socket is not None:
            self.unsafe_socket.close()


class DomainCache:
    __DATA_FOLDER = 'domains/'
    __set: set[str] = None
    __instance: DomainCache = None

    def __init__(self):
        self.__set = set()

    def __contains__(self, domain: str):
        return domain in self.__set

    def __read_from_file(self, filename: str | None = 'geolocation-cn'):
        """
        Read from data maintained by v2fly community
        https://github.com/v2fly/domain-list-community/blob/master/data/geolocation-cn
        """
        filename = DomainCache.__DATA_FOLDER + filename

        file = open(filename, 'r', encoding='utf-8')
        content = file.read()
        # remove comment and empty lines
        comment_pattern = re.compile('(#.*(?=\n)|\x20*)', re.MULTILINE)
        content = comment_pattern.sub('', content)
        # domains start with include:
        include_pattern = re.compile(r'(?<=include:).*', re.MULTILINE)
        included_files = include_pattern.findall(content)
        # domain lines without include:
        domain_pattern = re.compile(r'^(?!include).+$', re.MULTILINE)
        domains = domain_pattern.findall(content)
        file.close()

        for domain in domains:
            self.__set.add(domain)
        for fn in included_files:
            self.__read_from_file(fn)

    @classmethod
    def get_instance(cls):
        # NOT thread safe
        if cls.__instance is None:
            cls.__instance = DomainCache()
            cls.__instance.__read_from_file()
        return cls.__instance

    def has_domain(self, domain: str):
        try:
            domains = domain.split('.')
            return f'{domains[-2]}.{domains[-1]}' in self.__set
        except Exception as e:
            print(e)
            return False
