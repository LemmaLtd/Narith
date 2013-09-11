'''
[Narith]
File:   Eth.py
Author: Saad Talaat
Date:   15th July 2013
brief:  Structure to hold Ethernet info
'''
from Narith.base.Exceptions.Exceptions import *
from Narith.base.Packet.Protocol import Protocol
from Narith.base.Protocols import IP,Arp,IPv6
import threading

class Eth(Protocol):

    # FLAGS
    
    #type of data rep of input
    ISSTRING = False
    
    __protocols = {	'\x08\x06' : Arp.Arp,
    		'\x08\x00' : IP.IP,
    		'\x86\xDD' : IPv6.IPv6,
    		'\x00\x00' : None,
    		}
    	
    def __init__(self, binary):

    	# Check if in binary stream format or seperated format
    	super( Eth, self).__init__()
    	self.corrupted = False

    	if(type(binary) != str):
    		raise ValueError,"Malformed value type"

        self.__binary = binary


    ############################
    # Boolean Packet type checks
    def isIP(self):
    	return self.__protocols[self.type] == 'ip'
    def isARP(self):
    	return self.__protocols[self.type] == 'arp'


    ############################
    # Properties

    @property
    def type(self):
        t = self.__binary[12:14]
        if t not in self.__protocols.keys():
            return '\x00\x00'
        return t

    @type.setter
    def type(self, value):
        self.__binary = self.__binary[:12] + value

    @property
    def rawDst(self):
        return self.__binary[:6]

    @rawDst.setter
    def rawDst(self, value):
        self.__binary = value + self.__binary[6:14]

    @property
    def dst(self):
        dst = ""
    	for c in self.rawDst:
    		dst += c.encode('hex')
    		dst += ":"
    	dst = dst[:len(dst)-1]
    	return dst

    @dst.setter
    def dst(self,val):
    	if type(val) != str:
    		raise ValueError,"Malformed Value"
    	elif len(val.split(":")) != 6:
    		raise ValueError,"Malformed Value"
    	self.rawDst = "".join([chr(j) for j in  [int(c,base=16) for c in self.__sdst__.split(":")]])

    @property
    def rawSrc(self):
        return self.__binary[6:12]

    @rawSrc.setter
    def rawSrc(self, value):
        self.__binary = self.__binary[:6] + value + self.__binary[12:14]

    @property
    def src(self):
        src = ""
    	for c in self.rawSrc:
    		src += c.encode('hex')
    		src += ":"
    	src = src[:len(src)-1]
    	return src

    @src.setter
    def src(self,val):
    	if type(val) != str:
    		raise ValueError,"Malformed Value"
    	elif len(val.split(":")) != 6:
    		raise ValueError, "Malformed Value"
    	self.rawSrc = "".join([chr(j) for j in  [int(c,base=16) for c in self.__ssrc__.split(":")]])

    @property
    def nextProtocol(self):
    	return self.__protocols[self.type]

    @nextProtocol.setter
    def nextProtocol(self,value):
    	if( value not in self.__protocols.values()):
    		raise ValueError,"Unsupported protocol"
    	for k,v in self.__protocols.iteritems():
    		if v == value:
    			self.type = k

    @property
    def length(self):
    	return 14

    @property
    def iscorrupted(self):
    	return False
