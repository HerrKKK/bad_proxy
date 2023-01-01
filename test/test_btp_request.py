import uuid
from src.protocols import BTP, BTPRequest


def test_btp_request(host: str,
                     port: int,
                     data: str):
    return BTP.encode_request(host, port, data.encode(encoding='utf-8'))


def test_parse_btp_request(data: bytes):
    return BTPRequest(data)


if __name__ == '__main__':
    u = uuid.uuid4()
    print(len(u.bytes), u.bytes)
    btp_request_bytes = test_btp_request('127.0.0.1', 9999, 'test msg')
    btp_request = test_parse_btp_request(btp_request_bytes)
    print('test: ',
          btp_request.host,
          btp_request.host_len,
          btp_request.port,
          btp_request.uuid,
          btp_request.payload.decode())
