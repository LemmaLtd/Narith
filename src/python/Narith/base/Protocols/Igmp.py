'''
[Narith]
File:   Igmp.py
Author: Saad Talaat
Date:   21th August 2013
brief:  store IGMP protocol info
'''
from Narith.base.Packet.Protocol import Protocol

''' Only IGMPv2 '''

class Igmp(Protocol):

    def __init__(self, binary):

    	super(Igmp, self).__init__()
    	self._igmp = {}
    	self._igmp['type'] 	= ord(binary[0])
    	self._igmp['xrestime']	= ord(binary[1])
    	self._igmp['checksum']	= int(binary[2:4].encode('hex'),16)
    	self._igmp['grp-addr']	= ".".join([str(ord(x)) for x in binary[4:8]])
    	self._igmp['len']	= 8
    	self.corrupted = False
    ###########
    # Properties
    ###########
    @property
    def type(self):
    	return self._igmp['type']

    @property
    def response(self):
    	return self._igmp['xrestime']

    @property
    def group_addr(self):
    	return self._igmp['grp-addr']
    @property
    def length(self):
    	return self._igmp['len']
