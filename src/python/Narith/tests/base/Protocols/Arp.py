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
		b = "\xa8\xf5\x65\x00\x00\x00\x00\x00\x00\xc0\xa8\xf5\x64"
		self.a = Arp(b)

	def tearDown(self):
		self.a = None

	def testProperties(self):
		assertEqual(self.a.hardware_type, 'Ethernet')
		assertEqual(self.a.opcode, 'request')
		assertEqual(self.a.src, ("1c:65:9d:77:0f:4b","192.168.245.101"))
		assertEqual(self.a.dst, ("00:00:00:00:00:00","192.168.245.100"))
		self.dst = "12:34:56:78:90:11","192.168.111.111"
		assertEqual(self.src_mac,"12:34:56:78:90:11")
		assertEqual(self.src_ip, "192.168.111.111")

