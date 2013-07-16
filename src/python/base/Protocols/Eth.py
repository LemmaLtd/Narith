'''
[Narith]
File:   IOManager.py
Author: Saad Talaat
Date:   15th July 2013
brief:  Structure to hold Ethernet info
'''

class Eth():

	# FLAGS
	
	#type of data rep of input
	ISSTRING = False
	
	#packet type flags
	ISIP = False
	ISARP = False

	def __init__(self, dst, src, t):

		# Check if in binary stream format or seperated format
		if(type(dst) == str):
			try:
				assert len(dst.split(":")) == 6 
				assert len(src.split(":")) == 6
				self.__sdst__ = dst
				self.__ssrc__ = src
				self.ISSTRING = True
				self.rawDstSrc()
			except:
				pass

		# if not then assign them to raw variables
		# and conduct string initalization
		self.__dst__ = dst
		self.__src__ = src
		self__type__ = t
		self.srcDstSrc()

		self.__initFlags()


	def __initFlags(self):
		if self.__type__ == '\x08\x06':
			self.ISARP = True
		elif self.__type__ == '\x80\x00':
			self.ISIP = True


	def rawDstSrc(self):
		self.__dst__ = "".join([chr(j) for j in  [int(c,base=16) for c in self.__sdst__.split(":")]])
		self.__src__ = "".join([chr(j) for j in  [int(c,base=16) for c in self.__ssrc__.split(":")]])
		return (self.__dst__, self.__src__)


	#return pair or (dst,src) in seperated representation
	def strDstSrc(self):
		if self.ISSTRING:
			return (self.__sdst__, self.__ssrc__)
		dst = ""
		src = ""
		for c in self.__dst__:
			dst += c.encode('hex')
			dst += ":"
		dst = dst[:len(dst)-1]
		for c in self.__src__:
			src += c.encode('hex')
			src += ":"
		src = src[:len(src)-1]
		self.__sdst__ = dst
		self.__ssrc__ = src
		self.ISSTRING = True
		return (dst,src)

	############################
	# Boolean Packet type checks

	def isIP(self):
		return self.ISIP
	def isARP(self):
		return self.ISARP
