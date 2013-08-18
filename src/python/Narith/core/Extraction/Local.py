'''
[Narith]
File:	Local.py
Author:	Saad Talaat
Date:	17th August 2013
brief: Extracts info about local user
'''
from Narith.core.Extraction.Domains import DomainExtractor
class LocalInfo(object):

	def __init__(self, packets,dom):
		if type(packets) != list and packets != [] and type(packets[0]) != Packet:
			raise TypeError, "Invalid argument or list element type"
		#self.__dom = DomainExtractor(packets)
		self.__dom = dom
		self.__info = dict()
		
		self.__info['addr'] 	= self.__dom.host
		self.__info['dns']	= self.__dom.servers
		for packet in packets:
			prot = self._hasIP(packet)
			if prot:
				if self._isLocal(prot):
					self.__info['mac'] = packet.get(0).src
					break


	def _hasIP(self, packet):
		for protocol in packet:
			if type(protocol).__name__ == 'IP':
				return protocol
		return False

	def _isLocal(self, prot):
		return prot.src == self.__info['addr']

	@property
	def info(self):
		return self.__info

	@property
	def host(self):
		return self.__info['addr']

	@property
	def dns_servers(self):
		return self.__info['dns']

	@property
	def mac_address(self):
		return self.__info['mac']
