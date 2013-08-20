'''
[Narith]
File:   Icmpv6.py
Author: Saad Talaat
Date:   20th August 2013
Brief:  Holds info of Icmp protocol
'''

from Narith.base.Packet.Protocol import Protocol
import threading

class Icmpv6(Protocol):

	_options = \
		{
		1 : 'Source Link-Layer Address',
		2 : 'Target Link-Layer Address',
		3 : 'Prefix Information',
		4 : 'Redirected Header',
		5 : 'MTU'
		}

	def __init__(self, binary):

		_data = {
			1  : self._fail,
			2  : self._toobig,
			3  : self._fail,
			4  : self._failWithPointer,
			128: self._echo,
			129: self._echo,
			133: self._rsolicitation,
			134: self._radvertisement,
			135: self._nsolicitation,
			136: self._nsolicitation,
			137: self._redirect,
			
			}
		super(Icmpv6, self).__init__()
		self._icmp = {}
		self._icmpp = {}
		self.corrupted = False

		self._icmp['type'] 	= ord(binary[0])
		self._icmp['code'] 	= ord(binary[1])
		self._icmp['checksum']	= int(binary[2:4].encode('hex'),16)
		_data[self._icmp['type']](binary[4:])

	'''
	Auxiliary header completers
	'''

	def _fail(self,binary):
		self._icmpp['unused'] 	= binary[:4]
		self._icmpp['len']	= 4
		self._icmp['len']	= 8

	def _toobig(self,binary):
		self._icmpp['mtu']	= int(binary[:4].encode('hex'),16)
		self._icmpp['len']	= 4
		self._icmp['len']	= 8

	def _failWithPointer(self,binary):
		self._icmpp['pointer']	= int(binary[:4].encode('hex'),16)
		self._icmpp['len']	= 4
		self._icmp['len']	= 8

	def _echo(self, binary):
		self._icmpp['id'] 	= int(binary[ :2].encode('hex'),16)
		self._icmpp['seq'] 	= int(binary[2:4].encode('hex'),16)
		self._icmpp['data']	= binary[4:]
		self._icmpp['len']	= len(binary)
		self._icmp['len']	= len(binary) + 4

	def _rsolicitation(self, binary):
		self._icmpp['reserved'] = binary[0:4]
		self._icmpp['options'] = []
		self._icmpp['len']	= 4
		option_off = binary[4:]

		option = self._option(option_off)
		while option != {}:
			self._icmpp['options'].append(option)
			option_off = option_off[option['len']*8:]
			option = self._option(option_off)

		self._icmp['len'] = len(binary) + 4


	def _radvertisement(self, binary):
		self._icmpp['curlim']	= ord(binary[0])
		# XXX : Isolate flags when needed
		self._icmpp['reserved']	= binary[1]
		self._icmpp['lifetime'] = int(binary[2:4 ].encode('hex'),16)
		self._icmpp['rchtime']	= int(binary[4:8 ].encode('hex'),16)
		self._icmpp['trnstime']	= int(binary[8:12].encode('hex'),16)
		self._icmpp['len']	= 12
		self._icmpp['options'] = []
		option_off = binary[12:]

		option = self._option(option_off)
		while option != {}:
			self._icmpp['options'].append(option)
			option_off = option_off[option['len']*8:]
			option = self._option(option_off)

		self._icmp['len'] = len(binary) + 4


	def _nsolicitation(self, binary):
		self._icmpp['reserved'] = binary[0:4 ]
		self._icmpp['targaddr'] = self._formatIP(binary[4:20])
		self._icmpp['len']	= 20
		self._icmpp['options'] = []
		option_off = binary[20:]
		option = self._option(option_off)
		while option != {}:
			self._icmpp['options'].append(option)
			option_off = option_off[option['len']*8:]
			option = self._option(option_off)
		self._icmp['len'] = len(binary) + 4

	def _redirect(self, binary):
		self._icmpp['reserved']	= binary[0:4 ]
		self._icmpp['targaddr']	= self._formatIP(binary[4:20])
		self._icmpp['destaddr']	= self._formatIP(binary[20:36])
		self._icmpp['len']	= 36
		self._icmpp['options'] = []
		option_off = binary[36:]

		option = self._option(option_off)
		while option != {}:
			self._icmpp['options'].append(option)
			option_off = option_off[option['len']*8:]
			option = self._option(option_off)

		self._icmp['len'] = len(binary) + 4

	'''
	Helping functions
	'''
	def _formatIP(self, binary):
	        if len(binary) < 16:
	                return ''
	        ip = []
	        for i in range(0,16,2):
	                ip.append( binary[i].encode('hex') + binary[i+1].encode('hex') )
	        return ":".join(ip)

	def _option(self, binary):
		if binary == '':
			return {}
		opt =	{
			'type' 	: None,
			'name' 	: None,
			'len'	: None,
			'data'	: None
			}
		opt['type']	= ord(binary[0])
		opt['name']	= self._options[opt['type']]
		opt['len']	= ord(binary[1])
		data_delim = opt['len'] * 8
		opt['data']	= binary[2:data_delim]
		return opt


	'''
	Structure verification and completion
	post-classification
	'''
	def verify(self):
		'''
		Verifications
		- Length
		'''
		#self.cond.acquire()
		#self.cond.wait()
		### Start Verification ###
		stor_len = self._icmp['len']
		calc_len = 4
		calc_len += self._icmpp['len']
		try:
			calc_len += sum([x['len']*8 for x in self._icmpp['options']])
		except:
			pass
		if calc_len != stor_len:
			self.corrupted = True
		### End   Verification ###

		#self.cond.release()

	def notify(self):
		self.cond.acquire()
		self.cond.notify()
		self.cond.release()

	'''
	Properties
	'''
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
