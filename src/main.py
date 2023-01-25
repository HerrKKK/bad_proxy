import getopt
import threading
import socket
import ssl
import sys

from config import Config
from protocols import LRU, ProtocolEnum
from proxy import BadProxy, DomainCache


class StartUp:
    socket_proxy: socket = None
    socket_proxy_unsafe: socket
    context: ssl.SSLContext

    @classmethod
    def init(cls, config: Config):
        cls.socket_proxy_unsafe = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM
        )
        # recycle the port after socket closed
        cls.socket_proxy_unsafe.setsockopt(
            socket.SOL_SOCKET, socket.SO_REUSEADDR, 1
        )
        cls.socket_proxy_unsafe.bind(
            (config.inbound_config.host, config.inbound_config.port)
        )
        cls.socket_proxy_unsafe.listen(10)
        cls.socket_proxy = cls.socket_proxy_unsafe

        if config.inbound_config.tls is True:
            cls.context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
            cls.context.load_cert_chain(
                config.inbound_config.tls_cert_path,
                config.inbound_config.tls_key_path
            )

            cls.socket_proxy = cls.context.wrap_socket(
                cls.socket_proxy_unsafe,
                server_side=True
            )
        # init singletons to prevent concurrent issues later
        if config.outbound_config.direct_connect_cn is True:
            DomainCache.get_instance()
        if config.inbound_config.protocol == ProtocolEnum.BTP:
            LRU.get_instance()

    @classmethod
    def start(cls, config: Config):
        print(
            'listening on ',
            config.inbound_config.host,
            config.inbound_config.port
        )
        while True:
            try:
                instance = BadProxy(config)
                print('\nwaiting for connection\n')
                instance.inbound.listen(cls.socket_proxy)
                thread = threading.Thread(target=instance.proxy)
                thread.start()
            except KeyboardInterrupt:
                sys.exit()
            except Exception as e:
                print(e)

    @classmethod
    def main(cls):
        config_filename = 'conf/config.json'
        try:
            opts, _ = getopt.getopt(sys.argv[1:], 'c:', ['config='])
            for opt, arg in opts:
                if opt in ('-c', '--config'):
                    config_filename = arg
        except Exception as ex:
            print('error', ex)
            sys.exit()

        print(f'use {config_filename} as config')
        app_config = Config(config_filename)
        cls.init(app_config)
        cls.start(app_config)


if __name__ == '__main__':
    StartUp.main()
