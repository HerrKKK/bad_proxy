import select
import traceback

from src.config import Config
from src.protocols import HTTP, HttpRequest, BTPException
from .inbound import Inbound
from .outbound import Outbound


class BadProxy(object):
    def __init__(self, config: Config):
        self.inbound = Inbound(config.inbound_config)
        self.outbound = Outbound(config.outbound_config)

    def proxy(self):
        try:
            # Payload is the data from first package
            target_host, target_port, payload = self.inbound.connect()
            if target_host is None or target_port is None:
                return

            self.outbound.connect(target_host, target_port, payload)
            self.async_listen()
        except BTPException as e:
            print('invalid btp in connection: ', e)
            if self.outbound.fallback_host is not None:
                self.inbound.fallback()
                self.outbound.fallback()

                (target_host,
                 target_port,
                 payload) = HTTP.reverse_inbound_connect(self.inbound.socket,
                                                         self.inbound.buff_size,
                                                         e.raw_data)
                self.outbound.connect(target_host, target_port, payload)
                self.async_listen()
            else:
                HttpRequest(e.raw_data)  # check if a http request
                HTTP.send_fake_response(self.inbound.socket)
        except Exception as e:
            print(e)
            traceback.print_exc()
        finally:
            self.inbound.close()
            self.outbound.close()

    # async listen with select
    def async_listen(self):
        is_recv = True
        while is_recv:
            rlist, _, elist = select.select([self.inbound.socket,
                                             self.outbound.socket],
                                            [], [], 2)
            assert len(elist) == 0
            for sock in rlist:
                is_recv = True
                data = sock.recv(8192)
                # no data, try other socket
                if data == b'':
                    is_recv = False
                    continue

                # inbound received, outbound send data
                if sock is self.inbound.socket:
                    # print('inbound recv', data)
                    self.outbound.send(data)
                # outbound received, inbound send data
                elif sock is self.outbound.socket:
                    # print('outbound recv', data)
                    self.inbound.send(data)
