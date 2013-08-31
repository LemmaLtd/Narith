'''
[Narith]
File: 	Classifier.py
Author: Saad Talaat
Date:	16th August 2013
brief:	Classifies raw packet wireframes into Protocols and packets
'''
import threading
from Narith.base.Pcap.Pcap import Pcap
from Narith.base.Protocols import Eth, ProtData #, Arp, IP, Dns, Tcp, Udp, Ftp
from Narith.base.Packet.Packet import Packet
class Classifier(object):

	def __init__(self, packets, records=None):
		if type(packets) != list:
			raise TypeError, "Unexpected type"
		self.__packets = []
		self.__rawPackets = packets
		self.__records = records
		self.__corrupted = 0
	def classify(self):
		count = 0
		corrupted = 0
		for p in self.__rawPackets:
			count +=1
			packet = Packet()
			parent = Eth.Eth(p[:14])
			p = p[14:]
			invalid = 0

			while parent != None or p != '':
				packet.attach(parent)
				prot = parent.nextProtocol
				if prot == None:
					p = p[parent.length:]
					break
				parent = prot(p)
				p = p[parent.length:]

			self.__packets.append(packet)
	
			if p != '':
				packet.attach(ProtData.ProtData(p))

		#for p in self.__packets:
	#		for protocol in p:
	#			if type(protocol).__name__ == 'Icmpv6':
	#				protocol.notify()
		self.verify()

	def verify(self):
		count = 0
		for p in self.__packets:
			invalid = 0
			for prot in p:
				if type(prot).__name__ == 'ProtData':
					continue
				prot.verify()
				if prot.corrupted:
					invalid  = 1
					continue

			count += invalid
		self.__corrupted = count

	@property
	def packets(self):
		return self.__packets
	@property
	def records(self):
		return self.__records
	@property
	def size(self):
		return len(self.__packets)
	@property
	def corrupted(self):
		return self.__corrupted
