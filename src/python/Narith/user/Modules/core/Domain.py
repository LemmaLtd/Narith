'''
[Narith]
File:   Domain.py
Author: Saad Talaat
Date:   6th September 2013
brief:  Interface to Domain module
'''
from Narith.user.termcolor import cprint
from Narith.design.Meta import Patterns


class DomainInterface(object):

    __metaclass__ = Patterns.Singleton

    def __init__(self, pcap, packets):
        from Narith.base.Analysis.Classifier import Classifier
        from Narith.core.Extraction.Domains import DomainExtractor

        self.__commands = \
        {
        'www'    : self.www,
        'all'    : self.all,
        'search': self.search,
        }
        self.__domain = None
        self.__pcap = pcap
        self.__packets = packets
        self.__de = DomainExtractor(self.__packets)
        
    def executer(self, commands):
        if commands[0] not in self.__commands:
            return
        self.__commands[commands[0]](commands[1:])

    def www(self, commands):
        for domain,ip in self.__de.wwwExtract():
            cprint("[*] " + domain + " -> " + ip,'green')

    def all(self, commands):
        for domain,ip in self.__de.domains(''):
            cprint("[*] " + domain + " -> " + ip,'green')

    def search(self, commands):
        for domain,ip in  self.__de.domains(commands[0]):
            cprint("[*] " + domain + " -> " + ip, 'green')
    @property
    def pcap(self):
        return self.__pcap

    @property
    def extractor(self):
        return self.__de
