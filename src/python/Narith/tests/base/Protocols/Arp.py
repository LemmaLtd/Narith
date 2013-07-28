'''
[Narith]
File: Arp.py [Test]
Author: Saad Talaat
Date: 19th July 2013
brief: Structure to hold ARP
'''
from Narith.base.Protocols.Arp import *
from Narith.tests.base.Protocols.TestDecorator import istest
import unittest,random

@istest
class ArpTest(unittest.TestCase):

	def setUp(self):
		b = "\x00\x01\x08\x00\x06\x04\x00\x02\x00\x0c\x29\x0d\x2b\xae\xc0\xa8\xf5\x0c\x30\x46\x9a\x06\x8b\x4b\xc0\xa8\xf5\xfe"
		self.a = Arp(b)

	def tearDown(self):
		self.a = None

	def testProperties(self):
		self.assertEquals(self.a.hardware_type, 'Ethernet')
		self.assertEquals(self.a.opcode, 'reply')
		self.assertEquals(self.a.src, ("00:0c:29:0d:2b:ae","192.168.245.12"))
		self.assertEquals(self.a.target, ("30:46:9a:06:8b:4b","192.168.245.254"))
		self.a.target = "12:34:56:78:90:11","192.168.111.111"
		self.assertEquals(self.a.target_mac,"12:34:56:78:90:11")
		self.assertEquals(self.a.target_ip, "192.168.111.111")

