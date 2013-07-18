'''
[Narith]
File: narith.py
Author: Saad Talaat
Date: 18th July 2013
brief: origin python code
'''
import unittest

#Run tests for now
from Narith.tests.base.Protocols import IP,Eth
tests = [ IP.IPTest,Eth.EthTest]
loader = unittest.TestLoader()
def runTests():
	suite = unittest.TestSuite()
	for case in tests:
		t = loader.loadTestsFromTestCase(case)
		suite.addTests(t)
	runner = unittest.TextTestRunner()
	runner.run(suite)

if __name__ == "__main__":
	runTests()
