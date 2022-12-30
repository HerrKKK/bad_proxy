import sys
import socket
import getopt
import threading

from bad_proxy import BadProxy
from config import Config, read_config


class StartUp:
    socket_proxy: socket

    def start(self, config: Config):
        try:
            self.socket_proxy = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # 将SO_REUSEADDR标记为True, 当socket关闭后，立刻回收该socket的端口
            self.socket_proxy.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.socket_proxy.bind((config.inbound_config.host,
                                    config.inbound_config.port))
            self.socket_proxy.listen(10)
            while True:
                instance = BadProxy(config)
                print('waiting for connection')
                instance.inbound.listen(self.socket_proxy)
                thread = threading.Thread(target=instance.proxy)
                thread.start()
        except Exception as e:
            print(e.__str__)
            sys.exit()


if __name__ == '__main__':
    config_filename = None
    try:
        opts, _ = getopt.getopt(sys.argv[1:], 'c:', ['config='])
        for opt, arg in opts:
            print(opt, arg)
            if opt in ('-c', '--config'):
                config_filename = arg
    except Exception as ex:
        print('error', ex)
        sys.exit()

    app_config = read_config(config_filename)
    StartUp().start(app_config)
