#! /usr/bin/env python

'''
[Narith]
File: HttpSession.py
Author: Mohammad Samir @mohammadsamir
brief: Http session implementation
'''

from Narith.base.Stream.TcpSession import TcpSession
from Narith.base.Encoders.Gzip import GzipDecoder
import time
class HttpSession(TcpSession):

    def __init__(self, session):

        self.session = session
        self.nestedPackets = []
        self.encoding = None
        self.encoding2 = []
        self.packets = session.packets
        for sessionPackets in self.session.sessions.values():
            self.nestedPackets.append([])
            for p in sessionPackets:
                if 'syn' in p.hasProt('Tcp').flags or 'fin' in p.hasProt('Tcp').flags:
                    continue
                if p.hasProt('Http'):
                    try:
                        self.encoding = p.hasProt('Http').responseHeaders['Content-Encoding']
                    except:
                        pass

                    self.nestedPackets[-1].append(p)

        self.data = []

        for sessionPackets in self.nestedPackets:
            for packet in sessionPackets:
                pData = packet.hasProt('Http')
                #if packet.hasProt('Tcp').src == 2724 or packet.hasProt('Tcp').dst == 2724:
                #    print "BINGO"
                #    print repr(pData.data)
                #    print "="*100
                #    print pData.b
                if pData and (pData.type == 'data' or pData.type == 'response'):
                    pData = pData.data
                    if pData:
                        self.data.append(pData)
        stack = []
        seqstack = []
        self.data2 = []
        for sessionPackets in self.nestedPackets:
            size = 0
            stack = []
            seqstack = []
            cur_length = 0
            for packet in sessionPackets:
                pData = packet.hasProt('Http')
                encoding = None
                p_type = None
                if pData:
                    if pData.type != 'data':
                        p_type = pData.type
                        try:
                            cur_length = int(pData.responseHeaders['Content-Length'])
                        except:
                            cur_length = 0
                        try:
                            encoding = pData.responseHeaders['Content-Encoding']
                        except:
                            encoding = None

                    if 'push' not in packet.hasProt('Tcp').flags or (cur_length > 0 and (sum([len(x) for x in stack]) + len(pData.data)) < cur_length):
                        seq = packet.hasProt('Tcp').sequence
                        if seqstack and (seq == seqstack[-1] or seq - seqstack[-1] != len(pData.data)):
                            stack.pop()
                            seqstack.pop()
                        seqstack.append(packet.hasProt('Tcp').sequence)
                        stack.append(pData.data)
                        size += 1
                    elif p_type != 'request' and cur_length != 0:
                        stack.append(pData.data)
                        #print cur_length,":::::",sum([len(x) for x in stack])
                        self.encoding2.append('gzip' if GzipDecoder.isGzip(stack[0]) else None)
                        self.data2.append(stack)
                        cur_length = 0
                        encoding = None
                        stack = []
                        seqstack = []
                        size = 0
        #print "WHAT",self.encoding2


    @classmethod
    def fromTcpSession(HttpSessionClass, session):
        for packet in session.packets:
            if packet.hasProt('Tcp'):
                if packet.size > 3 and packet.hasProt('Http'):
                    return HttpSessionClass(session)
                    