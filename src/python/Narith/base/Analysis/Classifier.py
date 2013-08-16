'''
[Narith]
File: 	Classifier.py
Author: Saad Talaat
Date:	16th August 2013
brief:	Classifies raw packet wireframes into Protocols and packets
'''
from Narith.base.Pcap.Pcap import Pcap
from Narith.base.Protocols import Eth#, Arp, IP, Dns, Tcp, Udp, Ftp
from Narith.base.Packet.Packet import Packet
class Classifier(object):

	def __init__(self, packets, records=None):
		if type(packets) != list:
			raise TypeError, "Unexpected type"
		self.__packets = []
		self.__rawPackets = packets
		self.__records = records

	def classify(self):
		for p in self.__rawPackets:
			packet = Packet()
			parent = Eth.Eth(p[:14])
			p = p[14:]
			while parent != None:
				packet.attach(parent)
				prot = parent.nextProtocol
				if prot == None:
					break
				parent = prot(p)
				p = p[parent.length:]
			self.__packets.append(packet)
		return self.__packets
	@property
	def packets(self):
		return self.__packets
	@property
	def records(self):
		return self.__records
	@property
	def size(self):
		return len(self.__packets)
	
