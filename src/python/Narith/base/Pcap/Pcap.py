'''
[Narith]
File:   Pcap.py
Author: Saad Talaat
Date:   14th August 2013
brief:  Libpcap file format
'''
import threading,thread,time
from Narith.base.Exceptions.Exceptions import PcapError, PcapStructureError


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

	class PcapWorker(threading.Thread):
		rec = []
		pac = []
		__par = None
		def __init__(self, records, packets, binary,parse):
			threading.Thread.__init__(self)
			self.__bin = binary
			self.__par = parse

		def run(self):
			if self.__bin == '':
				return
			b = self.__bin
			pr = self.PacketRecord(b[:16],self.__par)
			b = b[16:]
			print ".",
			p = b[:pr.length]
			self.rec.append(pr)
			self.pac.append(p)

		class PacketRecord(object):
			def __init__(self, binary, parse):
				self.__timestampSec 	= int(parse(binary[:4   ]).encode('hex'),16)
				self.__timestampMicro	= int(parse(binary[4:8  ]).encode('hex'),16)
				self.__includedLength	= int(parse(binary[8:12 ]).encode('hex'),16)
				self.__originalLength	= int(parse(binary[12:16]).encode('hex'),16)

			@property
			def length(self):
				return self.__includedLength
			@property
			def origLength(self):
				return self.__originalLength

	class PacketRecord(object):
		def __init__(self, binary, parse):
			self.__timestampSec 	= int(parse(binary[:4   ]).encode('hex'),16)
			self.__timestampMicro	= int(parse(binary[4:8  ]).encode('hex'),16)
			self.__includedLength	= int(parse(binary[8:12 ]).encode('hex'),16)
			self.__originalLength	= int(parse(binary[12:16]).encode('hex'),16)

		@property
		def length(self):
			return self.__includedLength
		@property
		def origLength(self):
			return self.__originalLength
			
	def __init__(self, binary):
		self.__binary = binary
		self.__global_header =  self.GlobalHeader(binary[:24])
		self.__records = []
		self.__packets = []
		'''		
		b = binary[24:]
		workers = []
		count = 0
		print "Starting threads.."
		while True:
			if b == '':
				break
			worker = self.PcapWorker(self.__records, self.__packets, b, self.__global_header.parse)
			worker.start()
			print ".",
			b = b[16+worker.rec[len(self.__records)-1].length:]
			workers.append(worker)
		'''
		(self.__packet_headers, self.__packets) = self._parseRecords(binary[24:], self.__global_header.parse)

	def _parseRecords(self, binary,parse):
		records = []
		packets = []
		b = binary
		count = 0
		print "LOOPS:", len(b)/60
		while True:
			print ".",
			if b == '':
				break
			count +=1
			pr = self.PacketRecord(b[:16],parse)
			b = b[16:]
			p = b[:pr.length]
			b = b[pr.length:]
			#records.append(pr)
			#packets.append(p)
		self.__packet_count = count
		return records,packets

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
