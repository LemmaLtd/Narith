'''
[Narith]
File:   Ftp.py
Author: Saad Talaat
Date:   30th July 2013
brief:  Structure to hold Ftp info
'''

from Narith.base.Packet.Protocol import Protocol
import threading

#TODO:
#determine type using tcp src,dst port

class Ftp(Protocol):

    def __init__(self,b, isdata=False):
    	super( Ftp, self).__init__()
    	self.__length = len(b)
    	self.corrupted = False
    	self._ftp = {   'type':None,
    			'arg' :None,
    			'cmd' :None,
    			'code':None,
    		    }

        if isdata:
            self.__data = b
            self._ftp['type'] = 'data'
            return


    	b.strip("\x0d\x0a")
    	#determine first element type
    	# 1 slot? definitely request
    	# 1st slot is integer? response code!
    	self._ftp['cmd'] = b.split("\x20")[0]
#    	if (len(b) - len(self._ftp['cmd'])) < 3:
#    		self._ftp['type'] = 'request'
#    		return

    	try:
    		self._ftp['code'] = int(self._ftp['cmd'])
    		self._ftp['type'] = 'response'
    		self._ftp['cmd'] = None

    	except ValueError:
    		self._ftp['type'] = 'request'
    	try:
    		self._ftp['arg'] = " ".join(b.split("\x20")[1:])
    	except:
    		self.corrupted = True
    		return

    @classmethod
    def FtpData(cls, binary):
	return cls(binary, True)

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
    @property
    def length(self):
    	return self.__length
    @property
    def iscorrupted(self):
    	return self.corrupted
    @property
    def arg(self):
    	try:
    		return self._ftp['arg']
    	except:
    		return None
    @property
    def data(self):
        try:
            return self.__data
        except:
            return None
