'''
[Narith]
File:   IP.py
Author: Saad Talaat
Date:   15th July 2013
brief:  Structure to hold IP info
'''
''' SUPPORT VERSION 6 '''

from Narith.base.Exceptions.Exceptions import *
from Narith.base.Packet.Protocol import Protocol
from Narith.base.Protocols import Tcp, Udp, Icmp, Igmp
import threading


class IP(Protocol):

    __protocols = {
        1:  Icmp.Icmp,
        2:  Igmp.Igmp,
        6:  Tcp.Tcp,
        17: Udp.Udp
        }

    #############################################
    # Version, Header Length, DSF, Total Length
    # Identification, Flags, Fragment Offset, Ttl
    # Protocol, checksum, Src, Dst
    # and I like the dictionary more..
    ##############################################
    def __init__(self, bs):
        super(IP, self).__init__()
        self.__ip	= {}

        # if inserted bytes less than 20 bytes then its not ip
        if len(bs) < 20:
            raise BytesStreamError("Given bytes array is too short")

        self.__binary = bs

        #pcap files are in big endian, too bad that iterator doesn't seem handy
        self.corrupted = False
        #self.__ip['version'] 	= (  int(bs[0].encode( 'hex'),16) & 0xf0) >> 4
        #self.__ip['dsf']	= (  int(bs[1].encode( 'hex'),16))
        self.__ip['len']	= ((int(bs[2].encode('hex'), 16)) << 8) \
                                + (int(bs[3].encode('hex'), 16))
        #self.__ip['id']	= (( int(bs[4].encode( 'hex'),16)) << 8) + (int(bs[5].encode('hex'),16))
        #self.__ip['flags']	= (( int(bs[6].encode( 'hex'),16)) & 0xe0)
        #self.__ip['frag-off']	= (((int(bs[6].encode( 'hex'),16)) << 8) & 0x1f) +(int(bs[7].encode('hex'),16))
        #self.__ip['ttl']	= (  int(bs[8].encode( 'hex'),16))

    def _checksum(self, ip):
        checksum = 0
        count	 = 0
        size = len(ip)

        while size > 1:
            checksum += int((str("%02x" % (ord(ip[count]))) +
                        str("%02x" % (ord(ip[count + 1])))), 16)
            size -= 2
            count += 2
        if size:
            checksum += ord(ip[count])

        checksum = (checksum >> 16) + (checksum & 0xffff)
        checksum += (checksum >> 16)

        return (~checksum) & 0xffff

    def verify(self):
        b = self.__binary
        if self.checksum != self._checksum(b[:10] + '\x00\x00' + b[12:self.length]):
            self.corrupted = True
            return
    ######################################################
    # Properties
    ######################################################

    @property
    def checksum(self):
        bs = self.__binary
        return ((int(bs[10].encode('hex'), 16)) << 8) + (int(bs[11].encode('hex'), 16))

    @property
    def raw(self):
        return self.__ip

    @property
    def rawSrc(self):
        return    ((int(self.__binary[12].encode('hex'), 16)) << 24) + ((int(self.__binary[13].encode('hex'), 16)) << 16) +\
                    ((int(self.__binary[14].encode('hex'), 16)) << 8) + (int(self.__binary[15].encode('hex'), 16))

    @rawSrc.setter
    def rawSrc(self, value):
        self.__binary = self.__binary[:12] + "".join([chr(int(j)) for j in value.split(".")]) + self.__binary[15:]

    @property
    def src(self):
        src = ""
        for l in range(4)[::-1]:
            src += str((self.rawSrc >> l * 8) & 0xff) + "."
        src = src[:len(src) - 1]
        return src

    @src.setter
    def src(self, val):
        if (type(val) != str):
            raise ValueError("Malformed value")
        elif (len(val.split(".")) != 4):
            raise ValueError("Malformed value")
        self.rawSrc = val

    @property
    def rawDst(self):
        return    ((int(self.__binary[16].encode('hex'), 16)) << 24) +\
                    ((int(self.__binary[17].encode('hex'), 16)) << 16) +\
                    ((int(self.__binary[18].encode('hex'), 16)) << 8) +\
                    (int(self.__binary[19].encode('hex'), 16))

    @rawDst.setter
    def rawDst(self, value):
        self.__binary = self.__binary[:16] + "".join([chr(int(j)) for j in value.split(".")]) + self.__binary[19:]

    @property
    def dst(self):
        dst = ""
        for l in range(4)[::-1]:
            dst += str((self.rawDst >> l * 8) & 0xff) + "."
        dst = dst[:len(dst) - 1]
        return dst

    @dst.setter
    def dst(self, val):
        if (type(val) != str):
            raise ValueError("Malformed value")
        elif (len(val.split(".")) != 4):
            raise ValueError("Malformed value")
        self.rawDst = val

    @property
    def nextProtocol(self):
        prot = (int(self.__binary[9].encode('hex'), 16))
        if prot not in self.__protocols:
            return None
        return self.__protocols[prot]

    @nextProtocol.setter
    def nextProtocol(self, val):
        if val not in self.__protocols.values():
            raise ValueError("Invalid Protocol")
        for k, v in self.__protocols.iteritems():
            if v == val:
                prot = k
                self.__binary = self.__binary[:9] + chr(prot) + self.__binary[10:]

    @property
    def length(self):
        return (int(self.__binary[0].encode('hex'), 16) & 0x0f) * 4

    def getDstSrc(self):
        return self.dst, self.src

    def getRawDstSrc(self):
        return self.rawDst, self.rawSrc
