from .btp import BTP, BTPRequest, BTPResponse, BTPException
from .http import HTTP, HttpRequest, HttpResponse


class ProtocolEnum:
    RAW = 0        # inbound
    HTTP = 1       # inbound
    BTP = 2        # inbound/outbound
    FREEDOM = 3    # outbound
    BLACKHOLE = 4  # outbound
    REVERSE = 5    # inbound/outbound

    @staticmethod
    def interpret_string(protocol_str: str):
        match protocol_str:
            case 'raw':
                return ProtocolEnum.RAW
            case 'http':
                return ProtocolEnum.HTTP
            case 'btp':
                return ProtocolEnum.BTP
            case 'freedom':
                return ProtocolEnum.FREEDOM
            case 'blackhole':
                return ProtocolEnum.BLACKHOLE
            case 'reverse':
                return ProtocolEnum.REVERSE
            case _:
                print('no matched protocol')
                return None
