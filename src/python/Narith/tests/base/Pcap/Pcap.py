'''
[Narith]
File:   Pcap.py(test)
Author: Saad Talaat
Date:   14th August 2013
brief:  Libpcap file format
'''
from Narith.base.Pcap.Pcap import Pcap
from Narith.tests.TestDecorator import istest
import unittest

@istest
class PcapTest(unittest.TestCase):

	def setUp(self):
		binary = (open('Aux/PcapTestFile','r')).read()
		self.p = Pcap(binary)

	def tearDown(self):
		self.p = None

	def testCount(self):
		self.assertEquals(self.p.length, 10)
		self.assertEquals(len(self.p.packets), 10)
		self.assertEquals(len(self.p.records), 10)
		self.assertEquals(len(self.p.pairs), 10)

	def testSize(self):
		count = 0
		for record, packet in self.p.pairs:
			count +=1
			self.assertEquals(len(packet), record.length)

	def testInterface(self):
		self.assertEquals(self.p.interface, 1)
