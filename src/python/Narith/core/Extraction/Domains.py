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
				q = dns.queries[0][0]
				a = dns.answers[0][0]
				#if ("www" in q) and (q not in qa):
				qa.append(q)
				#if ("www" in a) and (a not in qa):
				qa.append(a)
			except:
				pass
		self.__domains = qa
		return qa
				
	def wwwExtract(self):
		qa = []
		for domain in self.__domains:
			if ("www" in domain) and (domain not in qa):
				qa.append(domain)
		return qa

	def _hasDns(self, packet):
		for protocol in packet:
			if type(protocol).__name__ == 'Dns':
				return protocol
			else:
				return False
		return False		
