'''
[Narith]
File:   IP.py
Author: Saad Talaat
Date:   15th July 2013
brief:  Structure to hold IP info
'''

from Exceptions.Exceptions import *

class IP():

	# Version, Header Length, DSF, Total Length
	# Identification, Flags, Fragment Offset, Ttl
	# Protocol, checksum, Src, Dst
	# and I like the dictionary more..
	__ip = {
		'version'	: None, #One field is enough to initalize dict.
		}
	__sip = {
		'version'	: None
		}
	__protocols = {
		6		: 'tcp',
		17		: 'udp'
		}
	ISSTRING = False
#		'h-len'		: None,
#		'dsf'		: None,
#		'len'		: None,
#		'id'		: None,
#		'flags'		: None,
#		'frag-off'	: None,
#		'ttl'		: None,
#		'protocol'	: None,
#		'checksum'	: None,
#		'src'		: None,
#		'dst'		: None

	def __init__(self, bs):
		# if inserted bytes less than 20 bytes then its not ip
		if len(bs) < 20:
			raise BytesStreamError,"Given bytes array is too short"

		#pcap files are in big endian, too bad that iterator doesn't seem handy
		self.__ip['version'] 	= (  int(bs[0].encode( 'hex'),16) & 0xf0)
		self.__ip['h-len']   	= (  int(bs[0].encode( 'hex'),16) & 0x0f)
		self.__ip['dsf']	= (  int(bs[1].encode( 'hex'),16))
		self.__ip['len']	= (( int(bs[2].encode( 'hex'),16)) << 8) + (int(bs[3].encode('hex'),16))
		self.__ip['id']		= (( int(bs[4].encode( 'hex'),16)) << 8) + (int(bs[5].encode('hex'),16))
		self.__ip['flags']	= (( int(bs[6].encode( 'hex'),16)) & 0xe0)
		self.__ip['frag-off']	= (((int(bs[6].encode( 'hex'),16)) << 8) & 0x1f) +(int(bs[7].encode('hex'),16))
		self.__ip['ttl']	= (  int(bs[8].encode( 'hex'),16))
		self.__ip['protocol']	= (  int(bs[9].encode( 'hex'),16))
		self.__ip['checksum']	= (( int(bs[10].encode('hex'),16)) << 8)  + (int(bs[11].encode('hex'),16))
		self.__ip['src']	= (( int(bs[12].encode('hex'),16)) << 24) + ((int(bs[13].encode('hex'),16)) << 16) +\
					  (( int(bs[14].encode('hex'),16)) << 8)  + (int(bs[15].encode('hex'),16))
		self.__ip['dst']	= (( int(bs[16].encode('hex'),16)) << 24) + ((int(bs[17].encode('hex'),16)) << 16) +\
					  (( int(bs[18].encode('hex'),16)) << 8)  + (int(bs[19].encode('hex'),16))

		self.formatted()

	def formatted(self):
		if self.ISSTRING:
			return self.__sip
		#on the contrary, iterators seems handy here \o/
		for i,v in self.__ip.iteritems():
			# are we formatting protocol?
			if( i == 'protocol'):
				self.__sip[i] = self.__protocols[v]
				continue
			elif(i == 'src') or (i == 'dst'):
				self.__sip[i] = str((self.__ip[i] >> 24)) + "." +\
						str((self.__ip[i] >> 16) & 0xff) + "." +\
						str((self.__ip[i] >> 8 ) & 0xff) + "." +\
						str((self.__ip[i]) & 0xff)
				continue
			else:
				self.__sip[i] = str(v)
		self.ISSTRING = True
		return self.__sip

	def raw(self):
		return self.__ip

	def getDstSrc(self):
		return self.__sip['dst'],self.__sip['src']

	def getRawDstSrc(self):
		return self.__ip['dst'],self.__ip['src']

	def getProtocol(self):
		return self.__sip['protocol']

	def getLen(self):
		return self.__ip['len']
