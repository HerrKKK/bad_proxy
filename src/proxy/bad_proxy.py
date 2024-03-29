import select

from config import Config
from .inbound import Inbound
from .outbound import Outbound
from protocols import BTPException, HttpRequest


class BadProxy:
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
            print('invalid btp connection', e)
            http_request = HttpRequest(e.raw_data)  # check if a http request
            print(f'active http detection from {http_request.host}')
            self.inbound.send_fake_response()
        finally:
            self.inbound.close()
            self.outbound.close()

    # async listen with select
    def async_listen(self):
        is_recv = True
        while is_recv:
            rlist, _, _ = select.select(
                [
                    self.inbound.socket,
                    self.outbound.socket
                ], [], [], 2
            )
            for sock in rlist:
                is_recv = True
                data = sock.recv(8192)
                # no data, try other socket
                if data == b'':
                    is_recv = False
                    continue

                # inbound received, outbound send data
                if sock is self.inbound.socket:
                    self.outbound.socket.send(data)
                # outbound received, inbound send data
                elif sock is self.outbound.socket:
                    self.inbound.socket.send(data)
