'''
[Narith]
File:   Local.py
Author: Saad Talaat
Date:   6th September 2013
brief:  Interface to Local module
'''

from Narith.user.termcolor import cprint
from Narith.design.Meta import Patterns

class LocalInterface(object):

    __metaclass__ = Patterns.Singleton


    def __init__(self, pcap, packets, extractor):
        from Narith.base.Analysis.Classifier import Classifier
        from Narith.core.Extraction.Local import LocalInfo

        self.__commands = \
            {
            'dns-servers'   : self.dns,
            'info'   : self.info,
            'host': self.host,
        'mac': self.mac,
            }
            self.__local = None
            self.__pcap = pcap
            self.__li = LocalInfo(packets,extractor)

    def executer(self, commands):
        if commands[0] not in self.__commands:
            return
        self.__commands[commands[0]](commands[1:])

    def dns(self, commands):
        cprint('[*] DNS Servers:','green')
        for server in self.__li.dns_servers:
            cprint('\tServer: %s' % server, 'green')

    def host(self, commands):
        cprint('[*] Host: %s' % self.__li.host, 'green')

    def mac(self, commands):
        cprint('[*] Mac address: %s' % self.__li.mac_address, 'green')

    def info(self, commands):
        self.dns(commands)
        self.mac(commands)
        self.host(commands)
    @property
    def pcap(self):
        return self.__pcap

