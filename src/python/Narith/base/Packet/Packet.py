'''
[Narith]
File: 	Packet.py
Author: Saad Talaat
Date: 	30th July 2013
brief:  Linking packet's protocols
'''
from Narith.base.Packet.Protocol import Protocol

class Packet(object):

	def __init__(self):
		self.__size = 0
		self.__headAndTail = Protocol()
		self.__headAndTail.next = self.__headAndTail
		self.__headAndTail.prev = self.__headAndTail
		self.index = 0

	def __iter__(self):
		self.index = 0
		return self

	def next(self):

		if self.index == self.__size:
			self.index = 0
			raise StopIteration
		prot = self.getProtocol(self.index)
		self.index = self.index + 1
		return prot

	def insertProtocol(self,index,prot):
		if (prot == None) or (not issubclass(type(prot),Protocol)):
			raise ValueError, "Malformed value"
		if (index < 0) or (index > self.__size):
			raise IndexError, "Index out of bound"
		e = self.getProtocol(index)
		e.attachAfter(prot)
		self.__size += 1

	def getProtocol(self,index):
		element = self.__headAndTail.next
		if (index < 0) or (index > self.__size):
			raise IndexError,"Index out of bound"
		for i in range(0,index):
			element = element.next
		return element

	def attach(self,prot):
		self.__headAndTail.attachBefore(prot)
		self.__size +=1

	def delete(self,index):
		if (index < 0) or ( index > self.__size):
			raise IndexError, "Index out of bound"
		self.__size -=1
		return self.getProtocol(index).detach().protocol

	def get(self,index):
		return self.getProtocol(index)

	def set(self,index,prot):
		self.getProtocol(index).detach()
		self.insertProtocol(index,prot)

	@property
	def empty(self):
		return self.__size == 0

	@property
	def size(self):
		return self.__size
