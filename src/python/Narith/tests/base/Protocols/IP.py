'''
[Narith]
File: IP.py [Test]
Author: Saad Talaat
Date: 18th July 2013
brief: Structure to hold IP
'''
from Narith.base.Protocols.IP import *
import unittest,random

class IPTest(unittest.TestCase):


	def setUp(self):
		b = "\x45\x00\x00\x30\x7d\xa0\x40\x00\x80\x06\xe8\xa9\xc0\xa8\xf5\x0c\x0c\x81\xd2\x47"
		self.ip = IP(b)

	def tearDown(self):
		self.ip = None

	def testFormat(self):
		assert self.ip.getDstSrc() == ("12.129.210.71","192.168.245.12"), "IP Pair did not match [IP(Test)]"
		assert self.ip.getProtocol() == 'tcp', "Protocol type did not match [IP(Test)]"
		assert (self.ip.getLen()) == 48 , "Packet Length did not match [IP(Test)]"
