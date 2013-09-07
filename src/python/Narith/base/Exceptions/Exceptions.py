'''
[Narith]
Author: Saad Talaat
Date: 16th July 2013
brief: Protocols Exceptions
'''


class ProtError(Exception):
    ''' Protocol Exception '''
    pass

class MacAddrError(ProtError):
    ''' Protocol Exception '''
    pass

class BytesStreamError(ProtError):
    ''' Protocol Exception '''
    pass

class PcapError(Exception):
    ''' Pcap file Exception '''
    pass

class PcapStructureError(PcapError):
    ''' Pcap file Exception '''
    pass
