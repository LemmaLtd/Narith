'''
[Narith]
File	: Arp.py
Author	: Saad Talaat
Date	: 19th July 2013
brief	: Structure to hold ARP
'''

from Narith.base.Packet.Protocol import Protocol
class Arp(Protocol):

	'''
	Fields:
	Hardware Type.
	Protocol type.
	Hardware size.
	Protocol size.
	Opcode.
	sender mac.
	sender ip.
	target mac.
	target ip.
	'''
	__htypes = {1 : 'Ethernet'}
	__ptypes = { 0x800 : 'IP' }
	__opcodes = {
			1: 'request',
			2: 'reply',
			3: 'request-reserve',
			4: 'reply-reserve'}
	def __init__(self,y):
		super(Arp, self).__init__()
		self.__arp = { 'htype'  : None }
		self.__sarp = {'htype' : None}

		
		self.__arp['htype'] = int(y[:2].encode('hex'),16)
		self.__arp['ptype'] = int(y[2:4].encode('hex'),16)
		self.__arp['hsize'] = int(y[4:5].encode('hex'),16)
		self.__arp['psize'] = int(y[5:6].encode('hex'),16)
		self.__arp['opcode'] = int(y[6:8].encode('hex'),16)
		self.__arp['src_mac'] = y[8:14]
		self.__arp['src_ip'] = y[14:18]
		self.__arp['dst_mac'] = y[18:24]
		self.__arp['dst_ip'] = y[24:28]

		self.__sarp['htype'] = self.__htypes[self.__arp['htype']]
                self.__sarp['ptype'] = self.__ptypes[self.__arp['ptype']]
                self.__sarp['hsize'] = str(self.__arp['hsize'])
                self.__sarp['psize'] = str(self.__arp['psize'])
                self.__sarp['opcode'] = self.__opcodes[self.__arp['opcode']]
                self.__sarp['src_mac'] = map(hex, map(ord, self.__arp['src_mac']))
                self.__sarp['src_ip'] = ".".join( map(str, map(ord, self.__arp['src_ip'])))
                self.__sarp['dst_mac'] = map(hex,map(ord,self.__arp['dst_mac']))
                self.__sarp['dst_ip'] = ".".join(map(str,map(ord,self.__arp['dst_ip'])))

		''' Fix string macs '''
		self.__macFix('src_mac')
		self.__macFix('dst_mac')
	def __macFix(self,key):
		tmp = []
		for i in self.__sarp[key]:
			if(len(i) == 3):
				i = '0x0'+i[2]
			tmp.append(i)
		self.__sarp[key] = ":".join("".join(tmp).split("0x")[1:])
	##########################
	# Properties
	@property
	def src(self):
		return self.src_mac,self.src_ip
	@src.setter
	def src(self,val):
		if type(val) != tuple:
			raise ValueError, "Malformed Value"
		elif len(val) != 2:
			raise ValueError, "Malformed Value"
		self.src_mac = val[0]
		self.src_ip = val[1]

	@property
	def src_mac(self):
		return self.__sarp['src_mac']

	@src_mac.setter
	def src_mac(self,val):
		if (type(val) != str) or ( len(val.split(":")) != 6):
			raise ValueError, "Malformed value"
		self.__sarp['src_mac'] = val
		self.__arp['src_mac'] = "".join([chr(j) for j in  [int(c,base=16) for c in self.__sarp['src_mac'].split(":")]])


	@property
	def src_ip(self):
		return self.__sarp['src_ip']

	@src_ip.setter
	def src_ip(self,val):
		if (type(val) != str) or ( len(val.split(".")) != 4):
			raise ValueError, "Malformed value"
		self.__sarp['src_ip'] = val
		self.__arp['src_ip'] = "".join([chr(int(j)) for j in val.split(".")])


	@property
	def target(self):
		return self.target_mac, self.target_ip

	@target.setter
	def target(self,val):
		if type(val) != tuple:
			raise ValueError, "Malformed Value"
		elif len(val) != 2:
			raise ValueError, "Malformed Value"
		self.target_mac = val[0]
		self.target_ip = val[1]

	@property
	def target_mac(self):
		return self.__sarp['dst_mac']

	@target_mac.setter
	def target_mac(self,val):
		if (type(val) != str) or ( len(val.split(":")) != 6):
			raise ValueError, "Malformed value"
		self.__sarp['dst_mac'] = val
		self.__arp['dst_mac'] = "".join([chr(j) for j in  [int(c,base=16) for c in self.__sarp['src_mac'].split(":")]])

	@property
	def target_ip(self):
		return self.__sarp['dst_ip']

	@target_ip.setter
	def target_ip(self,val):
		if (type(val) != str) or ( len(val.split(".")) != 4):
			raise ValueError, "Malformed value"
		self.__sarp['dst_ip'] = val
		self.__arp['dst_ip'] = "".join([chr(int(j)) for j in val.split(".")])


	@property
	def hardware_type(self):
		return self.__sarp['htype']
	@property
	def opcode(self):
		return self.__sarp['opcode']

	@opcode.setter
	def opcode(self,val):
		if (type(val) is not str) or val not in self.__opcodes.values():
			raise ValueError, "Malformed value"
		self.__sarp['opcode'] = val
		for k,v in self.__opcodes.iteritems():
			if v == val:
				self.__arp['opcode'] = k

	@property
	def length(self):
		return  8 + self.__arp['hsize']*2 + self.__arp['psize']*2

	@property
	def iscorrupted(self):
		return False
