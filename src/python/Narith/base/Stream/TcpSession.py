'''
[Narith]
Author: Saad Talaat
Date:   17th Sept 2013
Brief:  implementation for a tcp sesssion
'''
from Narith.base.Stream.Session import Session

class TcpSession(Session):
    def __init__(self, packets=[]):
        super(TcpSession, self).__init__()
        self.packets = packets
        initseqs = []
        srcdst = []
        for packet in packets:
            a = packet.hasProt('Tcp')
            if 'syn' in a.flags:
                initseqs.append(a.sequence)
                p = packet.hasProt('IP')
                srcdst.append((p.src,p.dst))

        self.sequences = initseqs
        ###
        # Sequence numbers over session
        # represent incoming and outgoing
        # which makes only two numbers
        ###
#        seqs = []
#        for s in initseqs:
#            seqs.append(s & 0xfff00000)
#        byseq = {}
#        for packet in packets:
#            a = packet.hasProt('Tcp')
#            p = packet.hasProt('IP')
#            if (a.sequence & 0xfff00000) in seqs:
#                if (a.sequence & 0xfff00000) not in byseq:
#                    byseq[a.sequence & 0xfff00000] = []
#                byseq[a.sequence & 0xfff00000].append(packet)

        byip = {}
        for packet in packets:
            a = packet.hasProt('Tcp')
            p = packet.hasProt('IP')
            if (p.src,p.dst) in srcdst:
                if (p.src,p.dst) not in byip:
                    byip[(p.src,p.dst)] = []
                byip[(p.src, p.dst)].append(packet)
        byseq = {}
        for sequence in initseqs:
            if sequence not in byseq:
                byseq[sequence] = byip.values[initseqs.index(sequence)]

        self.sessions = byseq

    @classmethod
    def fromSession(cls, session):
        packets = []
        sessions = {}

        for packet in session.packets:
            p = packet.hasProt('Tcp')
            if p:
                if p.dst > 1024:
                    if p.dst not in sessions:
                        sessions[p.dst] = []
                    sessions[p.dst].append(packet)
                elif p.src > 1024:
                    if p.src not in sessions:
                        sessions[p.src] = []
                    sessions[p.src].append(packet)

        for k,v in sessions.iteritems():
            packets.append(v)
        c = []
        for p in packets:
            c.append(cls(p))
        return c
