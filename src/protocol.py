class ProtocolType:
    RAW = 0
    HTTP = 1
    BTP = 2
    FREEDOM = 3

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
            case _:
                raise Exception('NO MATCH PROTOCOL!')
