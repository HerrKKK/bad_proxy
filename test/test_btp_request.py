import sys
import uuid

sys.path.append("../src")

from protocols import BTP, BTPRequest


def test_btp_request(host: str,
                     port: int,
                     uu_id: str,
                     directive: int,
                     data: str):
    return BTP.encode_request(host, port, uu_id, directive, data.encode())


def test_parse_btp_request(data: bytes):
    return BTPRequest(data)


if __name__ == '__main__':
    u = uuid.uuid4()
    btp_request_bytes = test_btp_request('127.0.0.1',
                                         9999,
                                         u.hex,
                                         0,
                                         'test msg')
    btp_request = test_parse_btp_request(btp_request_bytes)
    print('test: ',
          btp_request.host,
          btp_request.host_len,
          btp_request.port,
          btp_request.payload.decode())
