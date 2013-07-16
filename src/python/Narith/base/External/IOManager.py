'''
[Narith]
File: 	IOManager.py
Author: Saad Talaat
Date: 	14th July 2013
brief: 	extensible abstraction for IO Ops
'''
import datetime


class IOManager():
	__file_used__ = None
	__session_info__ = None
	__mode__	= None
	__handle__	= None
	def __init__(self, fname, mode):
		assert fname != ""
		self.__file_used__ = fname
		self.__session_info__ = "%x" % datetime.date.today()
		self.__mode__ = mode
		try:
			self.__handle__ = file(self.__file_used__, self.__mode__)
		except:
			print "File %s does not exist" % self.__file_used__

	def Read(self, *args):
		if len(args) > 0:
			return self.__handle__.read(args[0])
		else:
			return self.__handle__.read()

	def getHandle(self):
		return self.__handle__		
	def close(self):
		close(self.__handle__)
