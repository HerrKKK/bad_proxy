import sys
import ssl
import socket
import getopt
import threading

from ssl import SSLContext
from protocols import LRU, ProtocolEnum
from proxy import BadProxy, DomainCache
from config import Config


class StartUp:
    socket_proxy: socket = None
    socket_proxy_unsafe: socket
    context: SSLContext
    config: Config

    def __del__(self):
        self.socket_proxy.close()

    def init_config(self):
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
        self.config = Config(config_filename)

    def init_socket(self):
        self.socket_proxy_unsafe = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # recycle the port after socket closed
        self.socket_proxy_unsafe.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket_proxy_unsafe.bind((self.config.inbound_config.host,
                                       self.config.inbound_config.port))
        self.socket_proxy_unsafe.listen(10)
        self.socket_proxy = self.socket_proxy_unsafe

        if self.config.inbound_config.tls is True:
            self.context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
            self.context.load_cert_chain(self.config.inbound_config.tls_cert_path,
                                         self.config.inbound_config.tls_key_path)

            self.socket_proxy = self.context.wrap_socket(self.socket_proxy_unsafe,
                                                         server_side=True)

    def init_caches(self):
        # init singletons to prevent concurrent issues later
        if self.config.outbound_config.direct_connect_cn is True:
            DomainCache.get_instance()
        if self.config.inbound_config.protocol == ProtocolEnum.BTP:
            LRU.get_instance()

    def start(self):
        print('listening on ',
              self.config.inbound_config.host,
              self.config.inbound_config.port)
        while True:
            try:
                instance = BadProxy(self.config)
                print('\nwaiting for connection\n')
                instance.inbound.listen(self.socket_proxy)
                thread = threading.Thread(target=instance.proxy)
                thread.start()
            except KeyboardInterrupt:
                sys.exit()
            except Exception as e:
                print(e)

    def main(self):
        self.init_config()
        self.init_socket()
        self.init_caches()
        self.start()


if __name__ == '__main__':
    StartUp().main()
