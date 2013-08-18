'''
[Narith]
File:   Pcap.py
Author: Saad Talaat
Date:   14th August 2013
brief:  Libpcap file format
'''
import threading,thread,time
from Narith.base.Exceptions.Exceptions import PcapError, PcapStructureError
from Narith.base.External.IOManager import IOManager
from Narith.user.termcolor import cprint
import datetime
class Pcap(object):
	''' 
	Pcap object should receive pcap binary
	as parameter. Then, extract file format
	related information.
	'''


	class GlobalHeader(object):
		def __init__(self, header_bin):
			if len(header_bin) < 24:
				raise PcapStructureError,"Binary is too short"

			self.__magic = header_bin[:4]
			if self.__magic == '\xA1\xB2\xC3\xD4':
				# Not swapped!
				self.__versionMj	= int(header_bin[4:6  ].encode('hex'),16)
				self.__versionMn	= int(header_bin[6:8  ].encode('hex'),16)
				self.__timeZone		= int(header_bin[8:12 ].encode('hex'),16) # We don't really care at the moment
				self.__sigfigs		= int(header_bin[12:16].encode('hex'),16) # 0 anyway..
				self.__snaplen		= int(header_bin[16:20].encode('hex'),16)
				self.__network		= int(header_bin[20:24].encode('hex'),16)
				self.parse		= lambda x: x
			elif self.__magic == '\xD4\xC3\xB2\xA1':
				#Swapped
				self.__versionMj	= int(header_bin[4:6  ][::-1].encode('hex'),16)
				self.__versionMn	= int(header_bin[6:8  ][::-1].encode('hex'),16)
				self.__timeZone		= int(header_bin[8:12 ][::-1].encode('hex'),16)
				self.__sigfigs		= int(header_bin[12:16][::-1].encode('hex'),16)
				self.__snaplen		= int(header_bin[16:20][::-1].encode('hex'),16)
				self.__network		= int(header_bin[20:24][::-1].encode('hex'),16)
				self.parse		= lambda x: x[::-1]
			else:
				raise PcapStructureError, "Magic signature is Invalid"

		### Only getters
		@property
		def versionMajor(self):
			return self.__versionMj
		@property
		def versionMinor(self):
			return self.__versionMn
		@property
		def timeZone(self):
			return self.__timeZone
		@property
		def sigfigs(self):
			return self.__sigfigs
		@property
		def length(self):
			return self.__snaplen
		@property
		def network(self):
			return self.__network


	class PacketRecord(object):
		def __init__(self, binary, parse):
			self.__timestampSec 	= int(parse(binary[:4   ]).encode('hex'),16)
			self.__timeSec	 	= datetime.datetime.fromtimestamp(self.__timestampSec).strftime("%M-%d %H:%M:%S")
			self.__timestampMicro	= int(parse(binary[4:8  ]).encode('hex'),16)
			self.__timeMicro	= datetime.datetime.fromtimestamp(self.__timestampMicro).strftime("%M-%d %H:%M:%S:%U")
			self.__includedLength	= int(parse(binary[8:12 ]).encode('hex'),16)
			self.__originalLength	= int(parse(binary[12:16]).encode('hex'),16)

		@property
		def length(self):
			return self.__includedLength
		@property
		def origLength(self):
			return self.__originalLength

		@property
		def time(self):
			return self.__timeMicro
		@property
		def timestamp(self):
			return self.__timestampMicro
	def __init__(self, filename=None,binary=None):
		self.__records = []
		self.__packets = []

		if filename and ( type(filename) is str ) and ( len(filename) < 256):
			self.__packet_count = 0
			self.__interface = 0
			try:
				self.__file = IOManager(filename,'r')
			except:
				cprint ('[!] File %s does not exist' %filename,'red')
				return
			try:
				self.__global_header =  self.GlobalHeader(self.__file.read(24))
				(self.__packet_headers, self.__packets) = \
						self._parseFromFile(self.__global_header.parse)
			except:
				cprint('[!] Invalid pcap file format','red')
				return

		elif binary and (type(binary) is str):
			self.__binary = binary
			self.__global_header =  self.GlobalHeader(binary[:24])
			(self.__packet_headers, self.__packets) = \
						self._parseFromBin(binary[24:], self.__global_header.parse)

		else:
			
			raise ValueError,"Invalid filename length or binary data type"
	@classmethod
	def fromBinary(cls, binary):
		return cls(None,binary)

	@classmethod
	def fromFile(cls, filename):
		return cls(filename,None)
		
	def _parseFromBin(self, binary,parse):
		records = []
		packets = []
		b = binary
		count = 0
		while True:
			if b == '':
				break
			count +=1
			pr = self.PacketRecord(b[:16],parse)
			b = b[16:]
			p = b[:pr.length]
			b = b[pr.length:]
			records.append(pr)
			packets.append(p)
		self.__packet_count = count
		return records,packets
	def _parseFromFile(self, parse):
		p = "dummy"
		pdata = None
		count = 0
		recs, packs = [],[]
		while p != None:
			try:
				p = self.PacketRecord(self.__file.read(16),parse)
			except:
				break
			if p:
				pdata = self.__file.read(p.length)
				recs.append(p)
				packs.append(pdata)
				count +=1
		self.__packet_count = count
		return recs,packs
	def close(self):
		try:
			self.__file.close()
		except:
			pass
	## getters only
	@property
	def records(self):
		return self.__packet_headers
	@property
	def packets(self):
		return self.__packets
	@property
	def pairs(self):
		return zip(self.__packet_headers, self.__packets)
	@property
	def length(self):
		return self.__packet_count
	@property
	def interface(self):
		return self.__global_header.network
	@property
	def file(self):
		try:
			return self.__file.name
		except:
			return None
