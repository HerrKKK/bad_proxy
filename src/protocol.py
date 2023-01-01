class ProtocolType:
    RAW = 0        # inbound
    HTTP = 1       # inbound
    BTP = 2        # inbound/outbound
    FREEDOM = 3    # outbound
    BLACKHOLE = 4  # outbound

    @staticmethod
    def interpret_string(protocol_str: str):
        match protocol_str:
            case 'raw':
                return ProtocolType.RAW
            case 'http':
                return ProtocolType.HTTP
            case 'btp':
                return ProtocolType.BTP
            case 'freedom':
                return ProtocolType.FREEDOM
            case 'blackhole':
                return ProtocolType.BLACKHOLE
            case _:
                raise Exception('NO MATCH PROTOCOL!')
