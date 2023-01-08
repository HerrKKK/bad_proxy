import asyncio
import select

from config import Config
from protocols import BTPException, HttpRequest
from .inbound import Inbound
from .outbound import Outbound


async_proxy = True


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
            # self.non_block_listen()
        except BTPException as e:
            print('invalid btp connection', e)
            http_request = HttpRequest(e.raw_data)  # check if a http request
            print(f'active http detection from {http_request.host}')
            self.inbound.send_fake_response()
        finally:
            self.inbound.close()
            self.outbound.close()

    # async listen with select
    def non_block_listen(self):
        is_recv = True
        while is_recv:
            rlist, _, _ = select.select([self.inbound.socket,
                                         self.outbound.socket],
                                        [], [], 2)
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

    def async_listen(self):
        self.outbound.socket.setblocking(False)
        self.inbound.socket.setblocking(False)
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        inbound_listen = self.inbound_listen()
        outbound_listen = self.outbound_listen()
        loop.run_until_complete(asyncio.gather(inbound_listen,
                                               outbound_listen))
        loop.close()

    async def inbound_listen(self):
        loop = asyncio.get_event_loop()
        while True:
            inbound_data = await loop.sock_recv(self.inbound.socket, 8192)
            if inbound_data == b'':
                break
            await loop.sock_sendall(self.outbound.socket, inbound_data)

    async def outbound_listen(self):
        loop = asyncio.get_event_loop()
        while True:
            outbound_data = await loop.sock_recv(self.outbound.socket, 8192)
            if outbound_data == b'':
                break
            await loop.sock_sendall(self.inbound.socket, outbound_data)
