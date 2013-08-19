'''
[Narith]
File:	Icmp.py
Author:	Saad Talaat
Date:	19th August 2013
Brief:	Holds info of Icmp protocol
'''
from Narith.base.Packet.Protocol import Protocol

class Icmp(Protocol):


	'''
	Start by reading the primitive header
	RFC: 792
	http://www.ietf.org/rfc/rfc792.txt
	'''
	def __init__(self, binary):

		_data = {
		3 : self._failMtu,
		11: self._fail,
		4 : self._fail,
		12: self._failWithPointer,
		5 : self._redirect,
		8 : self._echo,
		0 : self._echo,
		13: self._timestamp,
		14: self._timestamp,
		15: self._information,
		16: self._information,
		17: self._addrMask,
		18: self._addrMask,
		30: self._traceroute,
		37: self._domrequest,
		38: self._domreply,				
		}
		super(Icmp, self).__init__()
		self._icmp 	= {}
		self._icmpp	= {}

		self._icmp['type'] 	= int(binary[0  ].encode('hex'),16)
		self._icmp['code'] 	= int(binary[1  ].encode('hex'),16)
		self._icmp['checksum']	= int(binary[2:4].encode('hex'),16)
		_data[self._icmp['type']](binary[4:])


	'''
	Auxiliary Header completers
	'''

	''' 
	RFC 1191 Routers fragmentation issues
	http:/www.ietf.org/rfc/rfc1191.txt - Section 4
	'''
	def _failMtu(self, binary):
		self._icmpp['unused'] 	= binary[0:2]
		self._icmpp['n-mtu']	= int(binary[2:4].encode('hex'),16)
		# Ip + Datagram
		self._icmpp['data']	= binary[4:]
		self._icmp['len']	= len(binary) + 4


	def _fail(self, binary):
		self._icmpp['unused'] 	= binary[0:4]
		self._icmpp['data']	= binary[4: ]
		self._icmp['len']	= len(binary) + 4

	def _failWithPointer(self, binary):
		self._icmpp['pointer']	= binary[0  ]
		self._icmpp['unused']	= binary[1:4]
		self._icmpp['data']	= binary[4: ]
		self._icmp['len']	= len(binary) + 4

	def _redirect(self, binary):
		self._icmpp['gateway'] 	= binary[0:4]
		self._icmpp['data']	= binary[4: ]
		self._icmp['len']	= len(binary) + 4

	def _echo(self, binary):
		self._icmpp['id']	= binary[0:2].encode('hex')
		self._icmpp['seq']	= binary[2:4].encode('hex')
		self._icmpp['data']	= binary[4:]
		self._icmp['len']	= len(binary) + 4

	def _timestamp(self, binary):
		import datetime
		self._icmpp['id']	= binary[0:2].encode('hex')
		self._icmpp['seq']	= binary[2:4].encode('hex')
		self._icmpp['o-tstmp']	= int(binary[4:8].encode('hex'),16)
		self._icmpp['r-tstmp']	= int(binary[8:12].encode('hex'),16)
		self._icmpp['t-tstmp']	= int(binary[12:16].encode('hex'),16)
		self._icmp['len']	= 20 # len(binary[:16]) + 4

	def _information(self, binary):
		## Obsolete ##
		self._icmpp['id']	= binary[0:2].encode('hex')
		self._icmpp['seq']	= binary[2:4].encode('hex')
		self._icmp['len']	= 8 # len(binary[:4]) + 4

	'''
	RFC 950 Requesting mask from gateway
	Appendix I, II
	'''
	def _addrMask(self, binary):
		self._icmpp['id']	= binary[0:2].encode('hex')
		self._icmpp['seq']	= binary[2:4].encode('hex')
		self._icmpp['mask']	= ".".join([ord(x) for x in binary[4:8]])
		self._icmp['len']	= 12 # len(binary[:8]) + 4

	'''
	RFC 1256 Message formats
	Section 3
	'''
	def _advertisement(self, binary):
		self._icmpp['count'] 	= int(binary[0  ].encode('hex'),16)
		self._icmpp['size']	= int(binary[1  ].encode('hex'),16)
		self._icmpp['lifetime']	= int(binary[2:4].encode('hex'),16)
		self._icmpp['routaddr']	= []
		count = 4
		for i in range(0,self._icmpp['count']):
			raddr = binary[count:count+4]
			plvl = binary[count+4:count+8]
			self._icmpp['routaddr'].append( (raddr,plvl) )
			count+=8 # 8 octets
		self._icmp['len'] = count

	def _solicitation(self, binary):
		self._icmpp['reserved'] = binary[:4]
		self._icmp['len']	= 8


	'''
	RFC 1393 ICMP Traceroute Message format
	Section 2.3
	'''	
	def _traceroute(self, binary):
		self._icmpp['id-num'] 	= int(binary[  : 2].encode('hex'),16)
		self._icmpp['unused'] 	= binary[2:4]
		self._icmpp['out-hop']	= int(binary[4 : 6].encode('hex'),16)
		self._icmpp['ret-hop']	= int(binary[6 : 8].encode('hex'),16)
		self._icmpp['link-speed']\
					= int(binary[8 :12].encode('hex'),16)
		self._icmpp['link-mtu']	= int(binary[12:16].encode('hex'),16)
		self._icmp['len']	= 20 # len(binary[:16]) + 4

	'''
	RFC 1788 Domain Name request
	Section 2
	'''
	def _domrequest(self, binary):
		self._icmpp['id']	= int(binary[  : 2].encode('hex'),16)
		self._icmpp['seq']	= int(binary[2 : 4].encode('hex'),16)
		self._icmp['len']	= 8

	'''
	RFC 1788 Domain Name reply
	Section 3
	'''
	def _domreply(self, binary):
		self._icmpp['id']	= int(binary[  : 2].encode('hex'),16)
		self._icmpp['seq']	= int(binary[2 : 4].encode('hex'),16)
		self._icmpp['ttl']	= int(binary[4 : 8].encode('hex'),16)
		self._icmpp['names']	= binary[8:]
		self._icmp['len']	= len(binary) + 4




	##############################
	# Properties
	##############################
	@property
	def type(self):
		return self._icmp['type']

	@property
	def code(self):
		return self._icmp['code']

	@property
	def length(self):
		return self._icmp['len']

	@property
	def aux_header(self):
		return self._icmpp
