'''
[Narith]
File:   Tcp.py
Author: Saad Talaat
Date:   28th July 2013
brief:  Structure to hold Tcp info
'''
from Narith.base.Packet.Protocol import Protocol
from Narith.base.Protocols import Ftp
import threading

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
		21 : Ftp.Ftp,
		}

	def __init__(self,b):
		super( Tcp, self).__init__()
		self._tcp = dict()
		self.corrupted = False
		self.__binary = b
		self._activeFlags = []

		self._tcp['src']      = int(b[:2   ].encode('hex'),16)
		self._tcp['dst']      = int(b[2:4  ].encode('hex'),16)
		self._tcp['seqn']     = int(b[4:8  ].encode('hex'),16)
		self._tcp['ackn']     = int(b[8:12 ].encode('hex'),16)
		self._tcp['hlen']     = (int(b[12:13].encode('hex'),16) >> 4) *4
		self._tcp['flags']    = int(b[12:14].encode('hex'),16) & 0xfff
		self._tcp['winsize']  = int(b[14:16].encode('hex'),16)
		self._tcp['checksum'] = int(b[16:18].encode('hex'),16)
		#TODO: pad and options
		remaining = self._tcp['hlen'] - 18
		self._tcp['pad'] = b[18:18+remaining]
		#self._tcp['c-checksum'] = self._checksum(b[:16] + '\x00\x00' + b[18:])


	def _checksum(self, tcp):
		checksum = 0
		count = 0
		size = len(tcp)
		while size > 1:
			checksum += int(( str("%02x" % ord(tcp[count])) + str("%02x" % ord(tcp[count + 1]))), 16)
			size -=2
			count +=2
		if size:
			checksum += ord(tcp[count])
		checksum = (checksum >> 16) + (checksum & 0xffff)
		checksum += (checksum >> 16)
		return (~checksum) & 0xffff


	################
	# Properties
	################
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
	def sequence(self):
		return self._tcp['seqn']

	@property
	def nextProtocol(self):
		if self._tcp['hlen'] == len(self.__binary):
			return None

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

