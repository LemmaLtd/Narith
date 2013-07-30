'''
[Narith]
File:   Ftp.py
Author: Saad Talaat
Date:   30th July 2013
brief:  Structure to hold Ftp info
'''

from Narith.base.Packet.Protocol import Protocol

#TODO:
#determine type using tcp src,dst port

class Ftp(Protocol):

	def __init__(self,b):
		super( Ftp, self).__init__()
		self._ftp = {   'type':None,
				'arg' :None,
				'cmd' :None,
				'code':None,
			    }
		b.strip("\x0d\x0a")

		#determine first element type
		# 1 slot? definitely request
		# 1st slot is integer? response code!

		self._ftp['cmd'] = b.split("\x20")[0]
		if (len(b) - len(self._ftp['cmd'])) < 3:
			self._ftp['type'] = 'request'
			return

		try:
			self._ftp['code'] = int(self._ftp['cmd'])
			self._ftp['cmd'] = None
			self._ftp['type'] = 'response'
		except ValueError:
			pass
		self._ftp['arg'] = " ".join(b.split("\x20")[1:])

	##############
	# properties
	@property
	def cmd(self):
		return self._ftp['cmd']

	@property
	def type(self):
		return self._ftp['type']

	@property
	def code(self):
		return self._ftp['code']
