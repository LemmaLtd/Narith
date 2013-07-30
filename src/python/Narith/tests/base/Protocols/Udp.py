'''
[Narith]
File: Udp.py [Test]
Author: Saad Talaat
Date: 19th July 2013
brief: Structure to hold Udp
'''
from Narith.base.Protocols.Udp import *
from Narith.tests.TestDecorator import istest
import unittest,random

@istest
class UdpTest(unittest.TestCase):

	def setUp(self):
		b = "".join([chr(random.randint(0,0xff)) for i in range(0,8)])
		self.u = Udp(b)

	def tearDown(self):
		self.u = None

	def testBoundaries(self):
		assert self.u.src != 0
		assert self.u.dst != 0
		assert self.u.len != 0
