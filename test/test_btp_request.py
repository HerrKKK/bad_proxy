from src.application_layer import BTP, BTPRequest


def test_btp_request(host: str,
                     port: int,
                     data: str):
    return BTP.encode_request(host, port, data.encode(encoding='utf-8'))


def test_parse_btp_request(data: bytes):
    return BTPRequest(data)


if __name__ == '__main__':
    btp_request_bytes = test_btp_request('127.0.0.1', 9999, 'test msg')
    btp_request = test_parse_btp_request(btp_request_bytes)
    print('test: ',
          btp_request.host,
          btp_request.port,
          btp_request.payload.decode())
