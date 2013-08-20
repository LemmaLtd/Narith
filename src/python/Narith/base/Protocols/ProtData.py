'''
[Narith]
File:	ProtData.py
Author:	Saad Talaat
Date:   19th August 2013
brief:	Represents data in protocol manner to be attachable to packet
'''
from Narith.base.Packet.Protocol import Protocol

class ProtData(Protocol):

	def __init__(self, data):
		self.__data = data

	@property
	def data(self):
		return self.__data

