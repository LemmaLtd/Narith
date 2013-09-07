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

    def verify(self):
    	pass

    @property
    def next(self):
    	if type(self.__next).__name__ != 'Protocol':
    		return self.__next
    	else:
    		return None
    @next.setter
    def next(self,n):
    	self.__next = n

    @property
    def prev(self):
    	if type(self.__prev).__name__ != 'Protocol':
    		return self.__prev
    	else:
    		return None
    @prev.setter
    def prev(self,p):
    	self.__prev = p

    @property
    def protocol(self):
    	return self
    @property
    def nextProtocol(self):
    	return None
