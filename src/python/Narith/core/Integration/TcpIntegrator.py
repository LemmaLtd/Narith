'''
[Narith]
File: TcpSegment.py
Author: Saad Talaat
Date: 28th August 2013
brief: Integerating Tcp Segments into one thunk

How to define an integrated thunk of segments
to avoid memory usage, a thunk is a list of
ProtData which hold same reference as original
ProtData.
'''
from Narith.base.Fragmentation.TcpSegment import TcpSegment
from Narith.base.Protocols.Tcp import Tcp


class TcpIntegrator2(object):

    def __init__(self, session):
        if type(session) != list:
            return
        if type(session[0]).__name__ != 'Packet':
            return

        self.session = session
        self.initseq = session[0].hasProt('Tcp').sequence

    def integrate(self):
        assembled = []
        prev = None

        for packet in self.session:
            curseq = packet.hasProt('Tcp').sequence
            if (curseq - self.initseq) > 1 and prev and prev.hasProt('ProtData') and packet.hasProt('ProtData'):
                print packet.hasProt('ProtData')
                print prev
                prev_len = curseq - self.initseq - packet.hasProt('Tcp').length - 1
                print "LENS",len(prev.hasProt('ProtData').data),prev_len
                if len(assembled) == 0:
                    assembled.append(prev.hasProt('ProtData').data)
                    assembled.append(packet.hasProt('ProtData').data)
                else:
                    assembled.append(packet.hasProt('ProtData').data)
            prev = packet

        return assembled


class TcpIntegrator(object):

    def __init__(self, packets):
        if type(packets) != list:
            return
        elif type(packets[0]).__name__ != 'Packet':
            return

        self.__segments = []
        for packet in packets:
            if not TcpSegment.isTcpSegment(packet):
                continue
            self.__segments.append(TcpSegment(packet))

    def integrate(self):
        self.__assembled = [] # List of List of segments
        Temp = []
        init = None
        for segment in self.__segments:
            if segment.isInitial:
                init = segment
                Temp.append(segment)
                continue

            elif init:
                if segment.srcdst == init.srcdst:
                    if segment.isFinal:
                        init = None
                        Temp.append(segment)
                        self.__assembled.append(Temp)
                        Temp = []
                    else:
                        Temp.append(segment)
                    continue
            else:
                self.__assembled.append([segment])
    def verify(self):
        import time
        invalid = 0
        for thunk in self.__assembled:
            target_pair = thunk[0].srcdst
            check_map = map(lambda x: x.srcdst == target_pair, thunk)
            if sum(check_map) != len(check_map):
                invalid += 1
        return invalid

    @property
    def assemblies(self):
        return self.__assembled
