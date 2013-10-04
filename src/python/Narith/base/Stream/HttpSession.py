#! /usr/bin/env python

'''
[Narith]
File: HttpSession.py
Author: Mohammad Samir @mohammadsamir
brief: Http session implementation
'''

from Narith.base.Stream.TcpSession import TcpSession
import time
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
				pData = packet.hasProt('Http')
				if pData:
					pData = pData.data
					if pData:
						self.data[-1].append(pData)

	@classmethod
	def fromTcpSession(HttpSessionClass, session):
		for packet in session.packets:
            if packet.hasProt('Tcp'):
			    if packet.size > 3 and packet.hasProt('Http'):
				    return HttpSessionClass(session)


