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
		xstr = ""
		istr = "012456ABCDEF"
		istr = random.sample(istr,len(istr))
		for i in range(0,len(istr)):
			xstr += istr[i]
			if (i%2 !=0):
				xstr+=":"
		xstr = xstr[:len(xstr)-1]
		self.s = xstr[::-1]
		self.d = xstr
		self.t = random.sample(['\x80\x00','\x80\x06'],2)[random.randint(0,1)]
		self.eth = Eth(xstr,xstr[::-1],self.t)
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
