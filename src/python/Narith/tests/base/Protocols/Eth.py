'''
[Narith]
File: Eth.py [Test]
Author: Saad Talaat
Date: 15th July 2013
brief: Structure to hold Ethernet info
'''
from Narith.base.Protocols.Eth import *
from Narith.tests.TestDecorator import istest
import unittest,random

@istest
class EthTest(unittest.TestCase):



	def setUp(self):
		self.eth = Eth("\x00\x0c\x29\x0d\x2b\xae\x30\x46\x9a\x06\x8b\x4b\x08\x00")
		self.t = '\x08\x00'
		self.d = "00:0c:29:0d:2b:ae"
		self.s = "30:46:9a:06:8b:4b"
	def tearDown(self):
		self.eth = None

	def testType(self):
		assert self.t == self.eth.__type__,"Types unmatched [Eth(Test)]"
		if self.t == '\x80\x00':
			assert self.eth.isIP(),"Invalid Internal type bool function [Eth(Test)]"
		elif self.t == '\x80\x06':
			assert self.eth.isARP(),"Invalid Internal type bool function [Eth(Test)]"
	
	def testStr(self):
		assert self.s == self.eth.strDstSrc()[1],"Invalid internal source string [Eth(Test)]"
		assert self.d == self.eth.strDstSrc()[0],"Invalid internal destination string [Eth(Test)]"


if __name__ == "__main__":
	unittest.main()
