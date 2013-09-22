#! /usr/bin/env python

'''
[Narith]
File: Passwds.py
Author: Diaa Diab @dia2diab
Review: Saad Talaat
brief: implementation for a Ftp sesssion
'''

from Narith.base.Stream.Session import Session

class FtpSession(Session):

    def __init__(self, session):
        self.__session = session
        self.seqs = []

    def check(self):
        ftps = self.__ftps()
        sessions = {}
        packets = []

        for ftp in ftps:
            prot = ftp.hasProt('Ftp')
            if prot:
                src = self.__TCP(prot).src
                dst = self.__TCP(prot).dst
                port = (src if src > 1024 else dst)

                if port not in sessions:
                    sessions[port] = []
                sessions[port].append(ftp)

        final = []
        for ses in sessions.itervalues():
            packets.append(ses)
        return


    def __IP(self, packet):
        return packet.prev.prev

    def __TCP(self, packet):
        return packet.prev

    def __ftps(self):
        ftps = []
        packets = self.__session.packets
        for packet in packets:
            if self.__hasFtp(packet):
                ftps.append(packet)
        return ftps

    def __hasFtp(self, packet):
        for protocol in packet:
            if type(protocol).__name__ == 'Ftp':
                return protocol
        return False
