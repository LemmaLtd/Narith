'''
[Narith]
File: Tcp.py [Test]
Author: Saad Talaat
Date: 28th July 2013
brief: Structure to hold Tcp info
'''
from Narith.base.Protocols.Tcp import *
from Narith.tests.TestDecorator import istest
import unittest,random

@istest
class TcpTest(unittest.TestCase):

	def setUp(self):
		b = "\x00\x50\x09\xa5\x60\xbf\xb7\xe1\x9b\xaf\xef\xd1\x60\x12\x1f\xfe\x01\x85\x00\x00\x02\x04\x05\xb4"
		self.t = Tcp(b)

	def tearDown(self):
		self.t = None

	def testProperties(self):
		self.assertEquals(self.t.src , 80)
		self.assertEquals(self.t.dst , 2469)
		self.assertEquals(self.t.flags ,['ack','syn'])
