'''
[Narith]
File: TcpSegment.py
Author: Saad Talaat
Date: 28th August 2013
brief: Integerating Tcp Segments into one thunk

How to define an integrated thunk of segments
to avoid memory usage, a thunk is a list of
ProtData which hold same reference as original
ProtData.
'''
from Narith.base.Fragmentation.TcpSegment import TcpSegment
class TcpIntegrator(object):

	def __init__(self, packets):
		if type(packets) != list:
			return
		elif type(packets[0]).__name__ != 'Packet':
			return

		self.__segments = []
		for packet in packets:
			if not TcpSegment.isTcpSegment(packet):
				continue
			self.__segments.append(TcpSegment(packet))

	def integrate(self):
		self.__assembled = [] # List of List of segments
		Temp = []
		init = None
		for segment in self.__segments:
			if segment.isInitial:
				init = segment
				Temp.append(segment)
				continue

			if init:
				if segment.srcdst == init.srcdst:
					if segment.isFinal:
						init = None
						Temp.append(segment)
						self.__assembled.append(Temp)
						Temp = []
						continue
					else:
						Temp.append(segment)


	def verify(self):
		import time
		invalid = 0
		for thunk in self.__assembled:
			target_pair = thunk[0].srcdst
			check_map = map(lambda x: x.srcdst == target_pair, thunk)
			time.sleep(3)
			if sum(check_map) != len(check_map):
				invalid += 1
		return invalid
