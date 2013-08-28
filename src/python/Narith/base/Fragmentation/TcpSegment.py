'''
[Narith]
File: TcpSegment.py
Author: Saad Talaat
Date: 28th August 2013
brief: Abstraction for Tcp segment
'''
class TcpSegment(object):

	def __init__(self, packet):
		assert type(packet).__name__ == 'Packet',"Fragmentation/TcpSegment.py"
		self.tcp = self._isTcp(packet)
		self.tcp
		self.__data = self._hasData(packet)
		self.__seq  = self.tcp.sequence
		self.__ip  = self._isIP(packet)


	def _isTcp(self, packet):
		for p in packet:
			if type(p).__name__ == 'Tcp':
				return p
		return False

	def _isIP(self, packet):
		for p in packet:
			if type(p).__name__ == 'IP':
				return p
		return False

	def _hasData(self, packet):
		for p in packet:
			if type(p).__name__ == 'ProtData':
				return p
		return False

	@staticmethod
	def isTcpSegment(packet):
		data = None
		tcp = None
		for p in packet:
			if type(p).__name__ == 'ProtData':
				data = p
			if type(p).__name__ == 'Tcp':
				tcp = p
		if data and tcp:
			return True
		else:
			return False

	@property
	def data(self):
		return self.__data

	@property
	def sequence(self):
		return self.__seq

	@property
	def isInitial(self):
		return len(self.data.data) >= 1460

	@property
	def isFinal(self):
		return self.tcp.isPsh

	@property
	def srcdst(self):
		return (self.__ip.src, self.tcp.src),(self.__ip.dst, self.tcp.dst)
