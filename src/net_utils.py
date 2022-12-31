import socket


def connect_socket(host, port) -> socket:
    # 解析DNS获取对应协议簇、socket类型、目标地址
    # getaddrinfo -> [(family, socket_type, proto, canonname, target_addr),]
    (family, socket_type, _, _, target_addr) = socket.getaddrinfo(host, port)[0]
    print(target_addr)
    tmp_socket = socket.socket(family, socket_type)
    tmp_socket.setblocking(False)
    tmp_socket.settimeout(5)
    tmp_socket.connect(target_addr)
    return tmp_socket
