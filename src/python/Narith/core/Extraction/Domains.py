'''
[Narith]
File: Domains.py
Author: Saad Talaat
Date: 16th August 2013
brief: Extracting domains from packet sequence
'''
from Narith.base.Packet.Packet import Packet
from Narith.base.Protocols.Dns import Dns

class DomainExtractor(object):

	def __init__(self, packets):
		if type(packets) != list and packets != [] and type(packets[0]) != Packet:
			raise TypeError,"Invalid arugment or list element type"
		self.__packets = packets
		self.__domains = []
	def extract(self):
		qa = []
		if self.__domains:
			return self.__domains

		for packet in self.__packets:
			dns = self._hasDns(packet)
			if not dns:
				continue
			try:
				a = []
				for answer in dns.answers:
					a.append([answer[0],answer[len(answer)-1]])
				qa.append(a)
			except:
				pass
		self.__domains = qa
		return qa
				
	def wwwExtract(self):
		qa = []
		for domains in self.__domains:
			for domain in domains:
				if domain and ("www" in domain[0]) and (domain not in qa) and self._isIP(domain[1]):
					domip = domain[0],domain[1]
					qa.append(domip)
		return qa

	def _hasDns(self, packet):
		for protocol in packet:
			if type(protocol).__name__ == 'Dns':
				return protocol
			else:
				return False
		return False		
	def _isIP(self,ip):
		if type(ip) != str:
			return False
		octets = ip.split(".")
		if len(octets) != 4:
			return False
		for octet in octets:
			try:
				int(octet)
			except:
				return False
		return True
