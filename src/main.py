# https://github.com/WengChaoxi/simple-http-proxy/blob/main/simple_http_proxy.py
from __future__ import print_function

import socket
import select
import sys
import getopt
import _thread as thread


def debug(tag, msg):
    print('[%s] %s' % (tag, msg))


class HttpRequestPacket(object):
    # HTTP请求包
    def __init__(self, data):
        self.__parse(data)

    def __parse(self, data):
        """
        解析一个HTTP请求数据包
        GET https://test.wengcx.top/index.html
        HTTP/1.1\r\nHost: test.wwr-blog.top\r\nProxy-Connection: keep-alive\r\nCache-Control: max-age=0\r\n\r\n

        参数：data 原始数据
        """
        i0 = data.find(b'\r\n')  # 请求行与请求头的分隔位置
        i1 = data.find(b'\r\n\r\n')  # 请求头与请求数据的分隔位置

        # 请求行 Request-Line
        self.req_line = data[:i0]
        self.method, self.req_uri, self.version = self.req_line.split()  # 请求行由method、request uri、version组成

        # 请求头域 Request Header Fields
        self.req_header = data[i0+2:i1]
        self.headers = {}
        for header in self.req_header.split(b'\r\n'):
            k, v = header.split(b': ')
            self.headers[k] = v
        self.host = self.headers.get(b'Host')

        # 请求数据
        self.req_data = data[i1+4:]


class SimpleHttpProxy(object):
    """
    简单的HTTP代理
    客户端(client) <=> 代理端(proxy) <=> 服务端(server)
    """
    def __init__(self,
                 host='127.0.0.1',
                 port=8888,
                 listen=10,
                 buf_size=8,
                 delay=1):
        """
        初始化代理套接字，用于与客户端、服务端通信
        参数：host 监听地址，默认0.0.0.0，代表本机任意ipv4地址
        参数：port 监听端口，默认8080
        参数：listen 监听客户端数量，默认10
        参数：buf_size 数据传输缓冲区大小，单位kb，默认8kb
        参数：delay 数据转发延迟，单位ms，默认1ms
        """
        self.socket_proxy = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 将SO_REUSEADDR标记为True, 当socket关闭后，立刻回收该socket的端口
        self.socket_proxy.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket_proxy.bind((host, port))
        self.socket_proxy.listen(listen)

        self.socket_recv_buf_size = buf_size * 1024
        self.delay = delay/1000.0

        debug('info', 'bind=%s:%s' % (host, port))
        debug('info', 'listen=%s' % listen)
        debug('info', 'buf_size=%skb, delay=%sms' % (buf_size, delay))

    def __del__(self):
        self.socket_proxy.close()

    def __connect(self, host, port):
        """
        解析DNS得到套接字地址并与之建立连接
        参数：host 主机
        参数：port 端口
        返回：与目标主机建立连接的套接字
        """
        # 解析DNS获取对应协议簇、socket类型、目标地址
        # getaddrinfo -> [(family, socket_type, proto, canonname, target_addr),]
        (family, socket_type, _, _, target_addr) = socket.getaddrinfo(host, port)[0]

        tmp_socket = socket.socket(family, socket_type)
        tmp_socket.setblocking(False)
        tmp_socket.settimeout(5)
        tmp_socket.connect(target_addr)
        return tmp_socket

    def __proxy(self, socket_client):
        """
        代理核心程序
        参数：socket_client 代理端与客户端之间建立的套接字
        """
        # 接收客户端请求数据
        req_data = socket_client.recv(self.socket_recv_buf_size)
        if req_data == b'':
            return

        # 解析http请求数据
        http_packet = HttpRequestPacket(req_data)

        # 获取服务端host、port
        if b':' in http_packet.host:
            server_host, server_port = http_packet.host.split(b':')
        else:
            server_host, server_port = http_packet.host, 80

        # 修正http请求数据
        tmp = b'%s//%s' % (http_packet.req_uri.split(b'//')[0], http_packet.host)
        req_data = req_data.replace(tmp, b'')

        socket_server = self.__connect(server_host, server_port)  # 建立连接

        # HTTP
        if http_packet.method in [b'GET', b'POST', b'PUT', b'DELETE', b'HEAD']:
            pass
        # HTTPS，会先通过CONNECT方法建立TCP连接
        elif http_packet.method == b'CONNECT':
            success_msg = b'%s %d Connection Established\r\nConnection: close\r\n\r\n' \
                          % (http_packet.version, 200)
            socket_client.send(success_msg)  # 完成连接，通知客户端
            # 客户端得知连接建立，会将真实请求数据发送给代理服务端
            req_data = socket_client.recv(self.socket_recv_buf_size)  # 接收客户端真实数据

        socket_server.send(req_data)  # 将客户端真实请求数据发给服务端

        # 使用select异步处理，不阻塞
        self.__nonblocking(socket_client, socket_server)

    def __nonblocking(self, socket_client, socket_server):
        """
        使用select实现异步处理数据
        参数：socket_client 代理端与客户端之间建立的套接字
        参数：socket_server 代理端与服务端之间建立的套接字
        """
        _rlist = [socket_client, socket_server]
        is_recv = True
        while is_recv:
            try:
                # rlist, wlist, elist = select.select(_rlist, _wlist, _elist, [timeout])
                # 参数1：当列表_rlist中的文件描述符fd状态为readable时，fd将被添加到rlist中
                # 参数2：当列表_wlist中存在文件描述符fd时，fd将被添加到wlist
                # 参数3：当列表_xlist中的文件描述符fd发生错误时，fd将被添加到elist
                # 参数4：超时时间timeout
                #  1) 当timeout==None时，select将一直阻塞，直到监听的文件描述符fd发生变化时返回
                #  2) 当timeout==0时，select不会阻塞，无论文件描述符fd是否有变化，都立刻返回
                #  3) 当timeout>0时，若文件描述符fd无变化，select将被阻塞timeout秒再返回
                rlist, _, elist = select.select(_rlist, [], [], 2)
                if elist:
                    break
                for tmp_socket in rlist:
                    is_recv = True
                    # 接收数据
                    data = tmp_socket.recv(self.socket_recv_buf_size)
                    if data == b'':
                        is_recv = False
                        continue

                    # socket_client状态为readable, 当前接收的数据来自客户端
                    if tmp_socket is socket_client:
                        socket_server.send(data)  # 将客户端请求数据发往服务端
                        # debug('proxy', 'client -> server')

                    # socket_server状态为readable, 当前接收的数据来自服务端
                    elif tmp_socket is socket_server:
                        socket_client.send(data)  # 将服务端响应数据发往客户端
                        # debug('proxy', 'client <- server')

                # time.sleep(self.delay)  # 适当延迟以降低CPU占用
            except Exception as e:
                print(e)
                break

        socket_client.close()
        socket_server.close()

    def client_socket_accept(self):
        """
        获取已经与代理端建立连接的客户端套接字，如无则阻塞，直到可以获取一个建立连接套接字
        返回：socket_client 代理端与客户端之间建立的套接字
        """
        socket_client, _ = self.socket_proxy.accept()
        return socket_client

    def handle_client_request(self, socket_client):
        try:
            self.__proxy(socket_client)
        except Exception as e:
            print(e)

    def start(self):
        while True:
            try:
                # self.handle_client_request(self.client_socket_accept())
                thread.start_new_thread(self.handle_client_request, (self.client_socket_accept(), ))
            except KeyboardInterrupt:
                break


if __name__ == '__main__':
    # 默认参数
    host_addr, listen_port, listen_count, buffer_size, delay_interval = \
        '127.0.0.1', 8888, 10, 8, 1

    try:
        opts, _ = getopt.getopt(sys.argv[1:], 'h:p:l:b:d:', ['host=', 'port=', 'listen=', 'buf_size=', 'delay='])
        for opt, arg in opts:
            if opt in ('-h', '--host'):
                host_addr = arg
            elif opt in ('-p', '--port'):
                listen_port = int(arg)
            elif opt in ('-l', '--listen'):
                listen_count = int(arg)
            elif opt in ('-b', '--buf_size'):
                buffer_size = int(arg)
            elif opt in ('-d', '--delay'):
                delay_interval = float(arg)
    except Exception as ex:
        debug('error', ex)
        sys.exit()

    # 启动代理
    SimpleHttpProxy(host_addr,
                    listen_port,
                    listen_count,
                    buffer_size,
                    delay_interval).start()
