'''
[Narith]
File:   Udp.py
Author: Saad Talaat
Date:   19th July 2013
brief:  Structure to hold UDP info
'''

''' so far all reading from bytes,
    shall do classmethods soon '''

class Udp(object):

	# Raw
	__udp = {'src' : None}

	def __init__(self,b):
		
		self.__udp['src'] = int(b[:2].encode('hex'),16)
		self.__udp['dst'] = int(b[2:4].encode('hex'),16)
		self.__udp['len'] = int(b[4:6].encode('hex'),16)
		self.__udp['checksum'] = int(b[6:8].encode('hex'),16)


	###################
	# Properties

	@property
	def src(self):
		return self.__udp['src']
	@src.setter
	def src(self,val):
		if (type(val) != int) and ( val > 0xffff) and (val < 0):
			raise ValueError,"Malformed Value"
		self.__udp['src'] = val

	@property
	def dst(self):
		return self.__udp['dst']

	@dst.setter
	def dst(self,val):
		if (type(val) != int) and ( val > 0xffff) and (val < 0):
			raise ValueError,"Malformed Value"
		self.__udp['dst'] = val

	@property
	def len(self):
		return self.__udp['len']
