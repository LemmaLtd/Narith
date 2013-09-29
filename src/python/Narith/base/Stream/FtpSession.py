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
        dataList = []
        for packets in self.sessions.itervalues():
            data.append([])
            for packet in packets:
                if packet.hasProt('Ftp'):
                    data[len(data)-1].append(packet)

        for packets in data:
            for packet in packets:
                ftp = packet.hasProt('Ftp')
                if ftp:
                    if ftp.data:
                        dataList.append(ftp.FtpData)
        self.data = dataList

    @classmethod
    def fromTcpSession(cls, session):
        for packet in session.packets:
            if packet.hasProt('Tcp'):
                if packet.size > 3 and packet.hasProt('Ftp'):
                    return cls(session)
