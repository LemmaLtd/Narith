'''
[Narith]
File:   Udp.py
Author: Saad Talaat
Date:   19th July 2013
brief:  Structure to hold UDP info
'''
from Narith.base.Packet.Protocol import Protocol
from Narith.base.Protocols import Dns
import threading

''' so far all reading from bytes,
    shall do classmethods soon '''


class Udp(Protocol):

    __protocols = {
        53: Dns.Dns
        }

    # Raw
    def __init__(self, b):
        super(Udp, self).__init__()
        #self._udp = {'src':None}
        self.corrupted = False
        try:
           #self._udp['src'] = int(b[:2].encode('hex'),16)
            #self._udp['dst'] = int(b[2:4].encode('hex'),16)
            #self._udp['len'] = int(b[4:6].encode('hex'),16)
            #self._udp['checksum'] = int(b[6:8].encode('hex'),16)
            length = int(b[4:6].encode('hex'), 16)
            self.__binary = b[:length]
        except:
            self.__corrupted = True
            return

    ###################
    # Properties

    @property
    def src(self):
        return int(self.__binary[:2].encode('hex'), 16)

    @src.setter
    def src(self, val):
        if (type(val) != int) or (val > 0xffff) or (val < 0):
            raise ValueError("Malformed Value")
        b1 = (val & ~0xff) >> 2
        b2 = (val & 0xff)
        self.__binary = chr(b1) + chr(b2) + self.__binary[2:]

    @property
    def dst(self):
        return int(self.__binary[2:4].encode('hex'), 16)

    @dst.setter
    def dst(self, val):
        if (type(val) != int) or (val > 0xffff) or (val < 0):
            raise ValueError("Malformed Value")
        b1 = (val & ~0xff) >> 2
        b2 = (val & 0xff)
        self.__binary = self.__binary[:2] + chr(b1) +\
                        chr(b2) + self.__binary[4:]

    @property
    def len(self):
        return int(self.__binary[4:6].encode('hex'), 16)

    @property
    def length(self):
        return 8

    @property
    def nextProtocol(self):
        if self.src < 1024:
            try:
                return self.__protocols[self.src]
            except:
                return None
        elif self.dst < 1024:
            try:
                return self.__protocols[self.dst]
            except:
                return None
        else:
            return None

    @property
    def iscorrupted(self):
        return self.__corrupted
