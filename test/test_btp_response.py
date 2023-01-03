import sys
sys.path.append("../src")

from protocols import BTP, BTPResponse


def test_btp_response(data: str):
    return BTP.encode_response(data.encode(encoding='utf-8'))


def test_parse_btp_response(data: bytes):
    return BTPResponse(data)


if __name__ == '__main__':
    btp_response_bytes = test_btp_response('test msg')
    btp_response = test_parse_btp_response(btp_response_bytes)
    print('test: ', btp_response.payload.decode())
