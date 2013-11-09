'''
[Narith]
File:   Session.py
Author: Saad Talaat
Date:   6th September 2013
brief:  Interface to session module
'''
from Narith.user.termcolor import cprint
from Narith.design.Meta import Patterns

class SessionInterface(object):

    __metaclass__ = Patterns.Singleton
    def __init__(self, pcap, packets, extractor):
        from Narith.base.Analysis.Classifier import Classifier
        from Narith.core.Extraction.Session import SessionExtractor
        self.__commands = \
        {
        'all'    : self.all,
        'search' : self.search,
        'www'    : self.www,
        'protocol': self.protocol
        }
        self.__pcap =  pcap
        self.__se = SessionExtractor(packets,pcap.records, extractor)

    def executer(self, commands):
        if commands[0] not in self.__commands:
            cprint("[!] Command not found",'red')
            return
        self.__commands[commands[0]](commands[1:])

    def all(self, commands):
        count = 0
        for host,session in self.__se.sessions.iteritems():
            cprint ("Host:\t\t"+session.hostname,'green')
            cprint ("Packets no.:\t"+str(session.count),'green')
            cprint ("Date:\t\t"+session.start+" ~ "+session.end,'green')
            cprint ("Bytes:\t\t"+str(session.bytes),'green')
            print ""
            count +=1
        cprint("Total sessions: "+str(count),'magenta')
    def search(self, commands):
        count = 0
        for session in self.__se.search(commands[0]):
            cprint ("Host:\t\t"+session.hostname,'green')
            cprint ("Packets no.:\t"+str(session.count),'green')
            cprint ("Date:\t\t"+session.start+" ~ "+session.end,'green')
            cprint ("Bytes:\t\t"+str(session.bytes),'green')
            print ""
            count +=1
        cprint("Total sessions: "+str(count),'magenta')

    def www(self, commands):
        count = 0
        for session in self.__se.prefix("www"):
            cprint ("Host:\t\t"+session.hostname,'green')
            cprint ("Packets no.:\t"+str(session.count),'green')
            cprint ("Date:\t\t"+session.start+" ~ "+session.end,'green')
            cprint ("Bytes:\t\t"+str(session.bytes),'green')
            print ""
            count +=1
        cprint("Total sessions: "+str(count),'magenta')


    def protocol(self, commands):
            pass
    

