'''
[Narith]
File:	IPv6.py
Author:	Saad Talaat
Date: 	20 August 2013
Brief:	Holds info of IPv6 protocol
'''
'''
                       1                   2                   3
   0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2
   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
   |Version| Traffic Class |           Flow Label                  |
   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
   |         Payload Length        |  Next Header  |   Hop Limit   |
   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
   +                         Source Address                        +
   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
   +                      Destination Address                      +
   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
'''

from Narith.base.Packet.Protocol import Protocol
from Narith.base.Protocols import Icmp, Tcp, Udp, Icmpv6
import threading

class IPv6(Protocol):

	__protocols = \
		{
		1	: Icmp.Icmp,
		6	: Tcp.Tcp,
		17	: Udp.Udp,
		58	: Icmpv6.Icmpv6
		}
	def __init__(self, binary):
		super(IPv6, self).__init__()
		self.__ip = {}
		self.__ip['version']	= ord(binary[0]) >> 4
		self.__ip['tc']		= ((int(binary[:2 ].encode('hex'),16) >> 4) & 0xff)
		self.__ip['flow']	= ( int(binary[1:4].encode('hex'),16) & 0xfff)
		self.__ip['f-len']	=   int(binary[4:6].encode('hex'),16)		# Following data length
		self.__ip['protocol']	=   int(binary[6  ].encode('hex'),16)
		self.__ip['hop-lim']	=   int(binary[7  ].encode('hex'),16)
		self.__ip['src']	=   self._formatIP(binary[8:24 ])
		self.__ip['dst']	=   self._formatIP(binary[24:40])
		self.__ip['len']	= 40
		self.corrupted = False

		if not self.nextProtocol:
			self.__ip['data'] = binary[40:]
			self.__ip['len']  = len(binary)


	def _formatIP(self, binary):
		if len(binary) < 16:
			return ''
		ip = []
		for i in range(0,16,2):
			ip.append( binary[i].encode('hex') + binary[i+1].encode('hex') )
		return ":".join(ip)

	def verify(self):
		next_len = self.__ip['f-len']
		real_len = 0
		node = self.next
		for node != None:
			real_len += node.length
			node = node.next
		if real_len != next_len:
			self.corrupted = True

	###################
	# Properties
	###################
	@property
	def src(self):
		return self.__ip['src']

	@property
	def dst(self):
		return self.__ip['dst']

	@property
	def length(self):
		return self.__ip['len']

	@property
	def nextProtocol(self):
		return self.__protocols[self.__ip['protocol']]
