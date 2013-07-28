'''
[Narith]
File: Dns.py [Test]
Author: Saad Talaat
Date: 27th July 2013
brief: Structure to hold Dns
'''
from Narith.base.Protocols.Dns import *
from Narith.tests.base.Protocols.TestDecorator import istest
import unittest,random

@istest
class DnsTest(unittest.TestCase):
	def setUp(self):
		ans = "\x0f\x9a\x81\x80\x00\x01\x00\x03\x00\x00\x00\x00\x01\x64\x04\x61\x67\x6b\x6e\x03\x63\x6f\x6d\x00\x00\x01\x00\x01\xc0\x0c\x00\x05\x00\x01\x00\x00\x02\x54\x00\x07\x04\x64\x61\x74\x61\xc0\x0e\xc0\x28\x00\x05\x00\x01\x00\x00\x02\x54\x00\x0a\x07\x73\x6a\x63\x70\x6f\x6f\x6c\xc0\x28\xc0\x3b\x00\x01\x00\x01\x00\x00\x00\x38\x00\x04\x08\x15\x18\x23"
		self.a = Dns(ans)
	def tearDown(self):
		self.a = None

	def testProperties(self):

		self.assertEquals(self.a.type,'response')
		self.assertEquals(self.a.identity,0xf9a)
		self.assertEquals(self.a.queryCount, 1)
		self.assertEquals(self.a.answerCount ,3)
