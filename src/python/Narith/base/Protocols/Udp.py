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
    	53 : Dns.Dns
    	}

    # Raw
    def __init__(self,b):
    	super( Udp, self).__init__()
    	self._udp = {'src':None}
    	self.corrupted = False
    	try:
    		self._udp['src'] = int(b[:2].encode('hex'),16)
    		self._udp['dst'] = int(b[2:4].encode('hex'),16)
    		self._udp['len'] = int(b[4:6].encode('hex'),16)
    		self._udp['checksum'] = int(b[6:8].encode('hex'),16)
    	except:
    		self.__corrupted = True
    		return

    ###################
    # Properties

    @property
    def src(self):
    	return self._udp['src']
    @src.setter
    def src(self,val):
    	if (type(val) != int) or ( val > 0xffff) or (val < 0):
    		raise ValueError,"Malformed Value"
    	self._udp['src'] = val

    @property
    def dst(self):
    	return self._udp['dst']

    @dst.setter
    def dst(self,val):
    	if (type(val) != int) or ( val > 0xffff) or (val < 0):
    		raise ValueError,"Malformed Value"
    	self._udp['dst'] = val

    @property
    def len(self):
    	return self._udp['len']

    @property
    def length(self):
    	return 8
    @property
    def nextProtocol(self):
    	if self._udp['src'] < 1024:
    		try:
    			return self.__protocols[self._udp['src']]
    		except:
    			return None
    	elif self._udp['dst'] < 1024:
    		try:
    			return self.__protocols[self._udp['dst']]
    		except:
    			return None
    	else:
    		return None

    @property
    def iscorrupted(self):
    	return self.__corrupted
