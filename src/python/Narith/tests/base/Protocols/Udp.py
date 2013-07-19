'''
[Narith]
File: Udp.py [Test]
Author: Saad Talaat
Date: 19th July 2013
brief: Structure to hold Udp
'''
from Narith.base.Protocols.Udp import *
from Narith.tests.base.Protocols.TestDecorator import istest
import unittest,random

@istest
class UdpTest(unittest.TestCase):

	def setUp(self):
		b = "".join([chr(random.randint(0,0xff)) for i in range(0,8)])
		self.u = Udp(b)

	def tearDown(self):
		self.u = None

	def testBoundaries(self):
		self.assertRaises(ValueError,self.u.src, 'pew pew')
