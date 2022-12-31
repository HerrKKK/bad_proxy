import socket
import ssl


class ServerSSL:
    @staticmethod
    def build_listen():
        # 生成SSL上下文
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        # 加载服务器所用证书和私钥
        context.load_cert_chain('certificate.pem',
                                'key.pem')

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0) as sock:
            sock.bind(('0.0.0.0', 7777))
            sock.listen(10)
            # 将socket打包成SSL socket
            with context.wrap_socket(sock, server_side=True) as tls_socket:
                while True:
                    # 接收客户端连接
                    client_socket, addr = tls_socket.accept()
                    msg = client_socket.recv(1024).decode("utf-8")
                    print(f"receive msg from client {addr}：{msg}")
                    # 向客户端发送信息
                    msg = f"yes , you have client_socket connect with server.\r\n".encode("utf-8")
                    client_socket.send(msg)
                    client_socket.close()


if __name__ == "__main__":
    ServerSSL.build_listen()
