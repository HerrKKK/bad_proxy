import sys
import getopt
import _thread as thread

from bad_proxy import BadProxy
from config import Config, read_config


class StartUp:
    @staticmethod
    def start(config: Config):
        while True:
            try:
                instance = BadProxy(config)
                instance.inbound.socket_accept()
                thread.start_new_thread(instance.proxy(), ())
            except KeyboardInterrupt:
                break


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
    StartUp.start(app_config)
