import socket
import ssl


class ClientSSL:
    @staticmethod
    def send_hello():
        # 生成SSL上下文
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        # 加载信任根证书
        context.load_verify_locations('certificate.pem')
        # context = ssl.create_default_context()

        with socket.create_connection(('127.0.0.1', 7777)) as sock:
            # 将socket打包成SSL socket
            # 一定要注意的是这里的server_hostname不是指服务端IP，而是指服务端证书中设置的CN
            with context.wrap_socket(sock, server_hostname='wwr-blog.com') as tls_socket:
                msg = "do i connect with server ?".encode("utf-8")
                tls_socket.send(msg)
                # 接收服务端返回的信息
                msg = tls_socket.recv(1024).decode("utf-8")
                print(f"receive msg from server : {msg}")
                tls_socket.close()


if __name__ == "__main__":
    ClientSSL.send_hello()
