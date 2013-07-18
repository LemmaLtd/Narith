'''
[Narith]
Author: Saad Talaat
Date: 16th July 2013
brief: Protocols Exceptions
'''

class ProtError(Exception):

	pass

class MacAddrError(ProtError):

	pass

class BytesStreamError(ProtError):

	pass
