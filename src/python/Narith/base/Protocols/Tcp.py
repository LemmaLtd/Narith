'''
[Narith]
File:   Tcp.py
Author: Saad Talaat
Date:   28th July 2013
brief:  Structure to hold Tcp info
'''
from Narith.base.Packet.Protocol import Protocol
from Narith.base.Protocols import Ftp
class Tcp(Protocol):

	_flags = {
		#ECN
		'nonce': 0b100000000,
		'cwr'	  : 0b10000000,
		'ecn-echo': 0b1000000,

		'urgent': 0b100000,
		'ack'  : 0b10000,
		'push' : 0b1000,
		'reset': 0b100,
		'syn'  : 0b10,
		'fin'  : 0b1,
		}
	__protocols = {
		21 : Ftp.Ftp
		}
	def __init__(self,b):
		super( Tcp, self).__init__()
		self._tcp = dict()
		
		self._activeFlags = []

		self._tcp['src']      = int(b[:2   ].encode('hex'),16)
		self._tcp['dst']      = int(b[2:4  ].encode('hex'),16)
		self._tcp['seqn']     = int(b[4:8  ].encode('hex'),16)
		self._tcp['ackn']     = int(b[8:12 ].encode('hex'),16)
		self._tcp['hlen']     = (int(b[12:13].encode('hex'),16) >> 12) *4
		self._tcp['flags']    = int(b[12:14].encode('hex'),16) & 0xfff
		self._tcp['winsize']  = int(b[14:16].encode('hex'),16)
		self._tcp['checksum'] = int(b[16:18].encode('hex'),16)
		########
		# TODO:
		# Link packet's different protocols to obtain
		# information from parent protocol.
		########

	##########
	# Properties

	@property
	def src(self):
		return self._tcp['src']
	@src.setter
	def src(self,val):
		if (type(val) is not int) or (val > 0xffff) or (val < 0):
			raise ValueError, "Malformed value"
		self._tcp['src'] = val

	@property
	def dst(self):
		return self._tcp['dst']
	@dst.setter
	def dst(self,val):
		if (type(val) is not int) or (val > 0xffff) or (val < 0):
			raise ValueError, "Malformed value"
		self._tcp['dst'] = val

	@property
	def flags(self):
		if len(self._activeFlags) != 0:
			return self._activeFlags
		for k,v in self._flags.iteritems():
			if (v & self._tcp['flags']) != 0:
				self._activeFlags.append(k)
		return self._activeFlags

	@property
	def nextProtocol(self):
		if(self._tcp['src'] < 1024):
			try:
				return self.__protocols[self._tcp['src']]
			except:
				return None
		else:
			try:
				return self.__protocols[self._tcp['dst']]
			except:
				return None
	@property
	def length(self):
		return self._tcp['hlen']
