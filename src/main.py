import sys
import ssl
import socket
import getopt
import threading

from proxy import BadProxy
from config import Config, read_config
from ssl import SSLContext


class StartUp:
    socket_proxy: socket
    socket_proxy_unsafe: socket
    context: SSLContext

    def __del__(self):
        self.socket_proxy.close()

    def start(self, config: Config):
        self.socket_proxy_unsafe = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 将SO_REUSEADDR标记为True, 当socket关闭后，立刻回收该socket的端口
        self.socket_proxy_unsafe.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket_proxy_unsafe.bind((config.inbound_config.host,
                                       config.inbound_config.port))
        self.socket_proxy_unsafe.listen(10)
        self.socket_proxy = self.socket_proxy_unsafe

        if config.inbound_config.tls is True:
            self.context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
            self.context.load_cert_chain(config.inbound_config.tls_cert_path,
                                         config.inbound_config.tls_key_path)

            self.socket_proxy = self.context.wrap_socket(self.socket_proxy_unsafe,
                                                         server_side=True)

        while True:
            try:
                instance = BadProxy(config)
                print('\nwaiting for connection\n')
                instance.inbound.listen(self.socket_proxy)
                thread = threading.Thread(target=instance.proxy)
                thread.start()
            except KeyboardInterrupt:
                sys.exit()
            except Exception as e:
                print(e)


if __name__ == '__main__':
    config_filename = None
    try:
        opts, _ = getopt.getopt(sys.argv[1:], 'c:', ['config='])
        for opt, arg in opts:
            if opt in ('-c', '--config'):
                config_filename = arg
    except Exception as ex:
        print('error', ex)
        sys.exit()

    app_config = read_config(config_filename)
    print('listening on ',
          app_config.inbound_config.host,
          app_config.inbound_config.port)
    StartUp().start(app_config)
