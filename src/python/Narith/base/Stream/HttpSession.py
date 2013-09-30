#! /usr/bin/env python

'''
[Narith]
File: HttpSession.py
Author: Mohammad Samir @mohammadsamir
brief: Http session implementation
'''

from Narith.base.Stream.TcpSession import TcpSession

class HttpSession(TcpSession):

	def __init__(self, session):

		self.session = session
		self.nestedPackets = []

		for sessionPackets in self.session.sessions.values():
			self.nestedPackets.append([])
			for p in sessionPackets:
				if p.hasProt('Http'):
					self.nestedPackets[-1].append(p)
					
		self.data = []

		for sessionPackets in self.nestedPackets:
			self.data.append([])
			for packet in sessionPackets:
				pData = packet.hasProt('ProtData')
				if pData:
					self.data[-1].append(pData.data)


