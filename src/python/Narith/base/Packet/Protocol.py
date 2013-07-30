'''
[Narith]
File:   Protocol.py
Author: Saad Talaat
Date:   30th July 2013
brief:  Protocol representing linkedlist element
'''


class Protocol(object):

	def __init__(self):
		self.__prev  = None
		self.__next  = None

	def attachBefore(self, prot):
		
		prot.next = self
		prot.prev = self.__prev
		self.__prev.next = prot
		self.__prev = prot

	def attachAfter(self,prot):

		prot.next = self.__next
		prot.prev = self
		self.__next.prev = prot
		self.__next = prot

	def detach(self):
		self.__prev.next = self.__next
		self.__next.prev = self.__prev
		self.prev = None
		self.next = None
		return self
	@property
	def next(self):
		return self.__next
	@next.setter
	def next(self,n):
		self.__next = n

	@property
	def prev(self):
		return self.__prev
	@prev.setter
	def prev(self,p):
		self.__prev = p

	@property
	def protocol(self):
		return self

