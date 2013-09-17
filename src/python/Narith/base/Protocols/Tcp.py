'''
[Narith]
File:   Tcp.py
Author: Saad Talaat
Date:   28th July 2013
brief:  Structure to hold Tcp info
'''
from Narith.base.Packet.Protocol import Protocol
from Narith.base.Protocols import Ftp, Http
import threading


class Tcp(Protocol):

    _flags = {
        #ECN
        'nonce': 0b100000000,
        'cwr': 0b10000000,
        'ecn-echo': 0b1000000,

        'urgent': 0b100000,
        'ack': 0b10000,
        'push': 0b1000,
        'reset': 0b100,
        'syn': 0b10,
        'fin': 0b1,
        }

    __protocols = {
        21: Ftp.Ftp,
        20: Ftp.Ftp.FtpData,
#        80: Http.Http,
        }

    def __init__(self, b):
        super(Tcp, self).__init__()
        self._tcp = dict()
        self.corrupted = False
        self._activeFlags = []

        #self._tcp['src']      = int(b[:2   ].encode('hex'),16)
        #self._tcp['dst']      = int(b[2:4  ].encode('hex'),16)
        #self._tcp['seqn']     = int(b[4:8  ].encode('hex'),16)
        #self._tcp['ackn']     = int(b[8:12 ].encode('hex'),16)
        #self._tcp['hlen']     = (int(b[12:13].encode('hex'),16) >> 4) *4
        #self._tcp['flags']    = int(b[12:14].encode('hex'),16) & 0xfff
        #self._tcp['winsize']  = int(b[14:16].encode('hex'),16)
        #self._tcp['checksum'] = int(b[16:18].encode('hex'),16)
        #TODO: pad and options
        #remaining = self._tcp['hlen'] - 18
        #self._tcp['pad'] = b[18:18+remaining]
        #self._tcp['c-checksum'] = self._checksum(b[:16] + '\x00\x00' + b[18:])
        length = (int(b[12:13].encode('hex'), 16) >> 4) * 4
        self.__binary = b[:length]

    def _checksum(self, tcp):
        checksum = 0
        count = 0
        size = len(tcp)
        while size > 1:
            checksum += int((str("%02x" % ord(tcp[count])) +\
                        str("%02x" % ord(tcp[count + 1]))), 16)
            size -= 2
            count += 2
        if size:
            checksum += ord(tcp[count])
        checksum = (checksum >> 16) + (checksum & 0xffff)
        checksum += (checksum >> 16)
        return (~checksum) & 0xffff

    ################
    # Properties
    ################
    @property
    def checksum(self):
        return int(self.__binary[16:18].encode('hex'), 16)

    @property
    def src(self):
        return int(self.__binary[:2].encode('hex'), 16)

    @src.setter
    def src(self, val):
        if (type(val) is not int) or (val > 0xffff) or (val < 0):
            raise ValueError("Malformed value")

        b1 = chr((val & ~0xff)) >> 2
        b2 = chr(val & 0xff)
        self.__binary = b1 + b2 + self.__binary[2:]

    @property
    def dst(self):
        return int(self.__binary[2:4].encode('hex'), 16)

    @dst.setter
    def dst(self, val):
        if (type(val) is not int) or (val > 0xffff) or (val < 0):
            raise ValueError("Malformed value")
        self.dst = val
        b1 = chr((val & ~0xff)) >> 2
        b2 = chr(val & 0xff)
        self.__binary = self.__binary[:2] + b1 + b2 + self.__binary[4:]

    @property
    def flags(self):
        flags = int(self.__binary[12:14].encode('hex'), 16) & 0xfff
        if len(self._activeFlags) != 0:
            return self._activeFlags
        for k, v in self._flags.iteritems():
            if (v & flags) != 0:
                self._activeFlags.append(k)
        return self._activeFlags

    @property
    def sequence(self):
        return int(self.__binary[4:8].encode('hex'), 16)

    @property
    def nextProtocol(self):
        trailer = map(lambda x: x == '\x00', self.__binary[self.length:])
        if trailer.count(True) == len(trailer) and len(trailer) != 0:
            return None

        if(self.src < 1024):
            try:
                return self.__protocols[self.src]
            except:
                return None
        else:
            try:
                return self.__protocols[self.dst]
            except:
                return None

    @property
    def length(self):
        return (int(self.__binary[12:13].encode('hex'), 16) >> 4) * 4

    @property
    def iscorrupted(self):
        return False

    ##################################
    # Checkers : Depends on Flags
    ##################################
    @property
    def isSyn(self):
        flags = self.flags
        if 'syn' in flags:
            return True
        else:
            return False

    @property
    def isFin(self):
        flags = self.flags
        if 'fin' in flags:
            return True
        else:
            return False

    @property
    def isAck(self):
        flags = self.flags
        if 'ack' in flags:
            return True
        else:
            return False

    @property
    def isPsh(self):
        flags = self.flags
        if 'push' in flags:
            return True
        else:
            return False
