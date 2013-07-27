'''
[Narith]
File:   IP.py
Author: Saad Talaat
Date:   15th July 2013
brief:  Structure to hold IP info
'''
''' SUPPORT VERSION 6 '''

from Exceptions.Exceptions import *

class IP(object):

	# Version, Header Length, DSF, Total Length
	# Identification, Flags, Fragment Offset, Ttl
	# Protocol, checksum, Src, Dst
	# and I like the dictionary more..
	def __init__(self, bs):
		self.__ip = {
			'version'	: None, 
#			One field is enough to initalize dict.
			}
		self.__sip = {
			'version'	: None
			}
		self.__protocols = {
			6		: 'tcp',
			17		: 'udp'
			}
		self.ISSTRING = False
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

		# if inserted bytes less than 20 bytes then its not ip
		if len(bs) < 20:
			raise BytesStreamError,"Given bytes array is too short"

		#pcap files are in big endian, too bad that iterator doesn't seem handy
		self.__ip['version'] 	= (  int(bs[0].encode( 'hex'),16) & 0xf0) >> 4
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
		self._formatted()


	def _formatted(self):
		if self.ISSTRING:
			return self.__sip
		#on the contrary, iterators seems handy here \o/
		for i,v in self.__ip.iteritems():
			# are we formatting protocol?
			if( i == 'protocol'):
				self.__sip[i] = self.__protocols[v]
				continue
			elif ((i == 'src') or (i == 'dst')) and (self.__ip['version'] == 4):
				self.__sip[i]= ""

				for l in range(0,4)[::-1]:
					self.__sip[i] += str((self.__ip[i] >> l*8) & 0xff) + "."
				self.__sip[i] = self.__sip[i][:len(self.__sip[i])-1]

				continue
			else:
				self.__sip[i] = str(v)
		self.ISSTRING = True
		return self.__sip

	@property
	def raw(self):
		return self.__ip

	@property
	def src(self):
		return self.__sip['src']

	@src.setter
	def src(self, val):
		if (type(val) != str):
			raise ValueError,"Malformed value"
		elif (len(val.split(".")) != 4):
			raise ValueError, "Malformed value"
		self.__sip['src'] =  val
		self.__ip['src'] = int("".join([chr(int(j)) for j in val.split(".")]).encode('hex'),16)
	@property
	def dst(self):
		return self.__sip['dst']

	@dst.setter
	def dst(self, val):
		if (type(val) != str):
			raise ValueError,"Malformed value"
		elif (len(val.split(".")) != 4):
			raise ValueError,"Malformed value"
		self.__sip['dst'] = val
		self.__ip['dst'] = int("".join([chr(int(j)) for j in val.split(".")]).encode('hex'),16)
	
	@property
	def protocol(self):
		return self.__sip['protocol']

	@protocol.setter
	def protocol(self,val):
		if val not in self.__protocols.values():
			raise ValueError,"Invalid Protocol"
		self.__sip['protocol'] = val
		for k,v in self.__protocols.iteritems():
			if v == val:
				self.__ip['protocol'] = k

	@property
	def len(self):
		return self.__ip['len']

	@len.setter
	def len(self,value):
		if type(value) != int:
			raise ValueError, "Malformed Value"
		self.__ip['len'] = value
		self.__sip['len']  = str(value)

	def getDstSrc(self):
		return self.__sip['dst'],self.__sip['src']

	def getRawDstSrc(self):
		return self.__ip['dst'],self.__ip['src']
