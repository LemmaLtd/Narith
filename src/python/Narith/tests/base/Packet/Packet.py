'''
[Narith]
File	: Packet.py [Test]
Author	: Saad Talaat
Date	: 30th July 2013
brief	: Linked Protocols via packet
'''

from Narith.base.Protocols import Eth,IP,Tcp,Ftp
from Narith.base.Packet.Packet import Packet
from Narith.base.Packet.Protocol import Protocol
from Narith.tests.TestDecorator import istest
import unittest,random

@istest
class PacketTest(unittest.TestCase):

	def setUp(self):
		self.p = Packet()
		l = [ Eth.Eth("00:0c:29:0d:2b:ae","c8:bc:c8:ec:be:e0","\x80\x00"),
		IP.IP("\x45\x00\x00\x3a\x1d\x30\x40\x00\x40\x06\xb2\x2c\xc0\xa8\xf5\x03\xc0\xa8\xf5\x0c"),
		Tcp.Tcp("\xcd\x86\x00\x15\x9e\x2c\x86\x14\xd0\xf9\x04\x6f\x80\x18\x20\x22\xe0\x6c\x00\x00\x01\x01\x08\x0a\x37\x5a\x6e\xd0\x00\x01\xf0\xa5"),
		Ftp.Ftp("\x4c\x49\x53\x54\x0d\x0a")]
		for i in l:
			self.p.attach(i)

	def tearDown(self):
		self.p = None

	def testSize(self):
		self.assertEquals(self.p.size,4)

	def testEmpty(self):
		self.p.delete(3)
		self.p.delete(2)
		self.p.delete(1)
		self.p.delete(0)
		self.assertTrue(self.p.empty)

	def testTypes(self):
		self.assertEquals(type(self.p.getProtocol(0)), Eth.Eth)
		self.assertEquals(type(self.p.getProtocol(1)), IP.IP)
		self.assertEquals(type(self.p.getProtocol(2)), Tcp.Tcp)
		self.assertEquals(type(self.p.getProtocol(3)), Ftp.Ftp)

	def testChain(self):
		#check forward chain
		self.assertEquals(self.p.getProtocol(0).next,\
				self.p.getProtocol(1))
		self.assertEquals(self.p.getProtocol(1).next,\
				self.p.getProtocol(2))
		self.assertEquals(self.p.getProtocol(2).next,\
				self.p.getProtocol(3))

		#check backward chain
		
		self.assertEquals(self.p.getProtocol(3).prev,\
				self.p.getProtocol(2))
		self.assertEquals(self.p.getProtocol(2).prev,\
				self.p.getProtocol(1))
		self.assertEquals(self.p.getProtocol(1).prev,\
				self.p.getProtocol(0))

	def testBoundaries(self):
		self.assertRaises(IndexError,self.p.insertProtocol,20,Protocol())
		self.assertRaises(ValueError,self.p.insertProtocol,3,2)
		self.assertRaises(IndexError, self.p.get, (20))
