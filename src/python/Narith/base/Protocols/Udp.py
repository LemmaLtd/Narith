'''
[Narith]
File:   Udp.py
Author: Saad Talaat
Date:   19th July 2013
brief:  Structure to hold UDP info
'''

''' so far all reading from bytes,
    shall do classmethods soon '''
import random
class Udp(object):

	# Raw
	_udp = dict()
	_pop = []
	def __init__(self,b):
		
		self._udp['src'] = int(b[:2].encode('hex'),16)
		self._udp['dst'] = int(b[2:4].encode('hex'),16)
		self._udp['len'] = int(b[4:6].encode('hex'),16)
		self._udp['checksum'] = int(b[6:8].encode('hex'),16)
		self._pop = self._udp['src']
	def getPop(self):
		return self._pop
	def getDst(self):
		return self._udp['dst']
	###################
	# Properties

	@property
	def pop(self):
		return self._pop
	@property
	def src(self):
		return self._udp['src']
	@src.setter
	def src(self,val):
		if (type(val) != int) and ( val > 0xffff) and (val < 0):
			raise ValueError,"Malformed Value"
		self._udp['src'] = val

	@property
	def dst(self):
		return self._udp['dst']

	@dst.setter
	def dst(self,val):
		if (type(val) != int) and ( val > 0xffff) and (val < 0):
			raise ValueError,"Malformed Value"
		self._udp['dst'] = val

	@property
	def len(self):
		return self._udp['len']
