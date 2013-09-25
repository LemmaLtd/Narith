#! /usr/bin/env python

'''
[Narith]
File: Passwds.py
Author: Diaa Diab @dia2diab
Review: Saad Talaat
brief: implementation for a Ftp sesssion
'''

from Narith.base.Stream.TcpSession import TcpSession

class FtpSession(TcpSession):
    def __init__(self, session):
        self.base_session = session
        self.packets = session.packets
        self.sessions = session.sessions
        data = []
        for packets in sessions.itervalues():
            data.append([])
            for packet in packets:
                if packet.hasProt('Ftp'):
                    data[len(data)-1].append(packet)
        self.data = data

    @classmethod
    def fromTcpSession(cls, session):
        for packet in session.packet:
            if packet.hasProt('Tcp'):
                if packet.size > 3 and packet.hasProt('Ftp'):
                    return cls(session)

