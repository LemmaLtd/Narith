'''
[Narith]
File:   Pcap.py
Author: Saad Talaat
Date:   6th September 2013
brief:  Interface to pcap module
'''

from Narith.user.termcolor import cprint
from Narith.base.Pcap.Pcap import Pcap
from Narith.design.Meta import Patterns

class PcapInterface(object):
    __interfaces = \
    {
    0 : 'Undefined',
    1 : 'Ethernet'
    }
    __metaclass__ = Patterns.Singleton

    def __init__(self):
        self.__commands = \
        {
        'read' : self.read,
        'count' : self.count,
        'interface' : self.interface,
        }
        self.__pcap = None

    def executer(self, commands):
        if commands[0] not in self.__commands:
            return
        self.__commands[commands[0]](commands[1:])

    def read(self, files):
        p = []
        for f in files:
            pp = Pcap(f)
            p.append(pp)
            if pp.length:
                cprint(('[*] file %s read' % f),'green')
        self.__pcap = p

    def count(self, files):
        for p in self.__pcap:
            if p.file and p.length:
                cprint('[*] file %s: %d packets' % (p.file,p.length),'green')
            else:
                cprint('[!] Invalid file','red')
                
    def interface(self, files):
        for p in self.__pcap:
            try:
                cprint('[*] file %s: %s' %(p.file, self.__interfaces[p.interface]),'green')
            except:
                cprint('[!] Invalid file','red')
    def has(self, f):
        for p in self.__pcap:
            if p.file == f:
                return True
            else:
                False
    @property
    def pcap(self):
        return self.__pcap
    @pcap.setter
    def pcap(self, value):
        self.__pcap = value
