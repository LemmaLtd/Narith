'''
[Narith]
File: Session.py
Author: Saad Talaat
Date: 18th August 2013
brief: Extracting sessions from pcap
'''
from Narith.core.Extraction.Domains import DomainExtractor
from Narith.base.Stream.Session import Session
class SessionExtractor(object):

    def __init__(self, packets,records, dom=None):
        if type(packets) != list and packets != [] and type(packets[0]) != Packet:
            raise TypeError,"Invalid arugment or list element type"
        self.__packets = packets
        self.__sessions = []
        self.__de = dom
        self.__read = []
        self.__records = records
        self.__processed = 0
        self.extract()

    def extract(self):
        import datetime, time
        sessions = []
        host = self.__de.host
        times = {}
        recidx = 0
        for packet in self.__packets:
            ip = packet.hasProt('IP')
            try:
                record = self.__records[recidx]
            except:
                pass

            if not ip:
                recidx += 1
                continue
            # is the local a source address?
            if ip.src == host:

                if self._alreadyRead(ip.dst):
                    if ip.dst in times:
                    #if ip.dst in times:
                        times[ip.dst].count +=1
                        times[ip.dst].bytes += record.length
                        times[ip.dst].end = record.time
                        times[ip.dst].packets.append(packet)
                    recidx += 1
                    continue

                cur_host = ip.dst
#self.__de.lookup(ip.dst)
                self.__read.append(ip.dst)
                start = record.time
                times[ip.dst] = Session()
                times[ip.dst].host = ip.dst
                times[ip.dst].hostname = cur_host
                times[ip.dst].start = start
                times[ip.dst].bytes = record.length
                times[ip.dst].packets.append(packet)
            # is the local a destination address?
            elif ip.dst == host:
                if self._alreadyRead(ip.src):
                    if ip.src in times:
                        times[ip.src].count +=1
                        times[ip.src].bytes += record.length
                        times[ip.src].end = record.time
                        times[ip.src].packets.append(packet)
                    recidx +=1
                    continue
                cur_host = ip.src
#self.__de.lookup(ip.src)
                self.__read.append(ip.src)
                start = record.time
                times[ip.src] = Session()
                times[ip.src].host = ip.dst
                times[ip.src].hostname = cur_host
                times[ip.src].start = start
                times[ip.src].bytes = record.length
                times[ip.src].packets.append(packet)
            recidx +=1

        count = 0
        for ip, session in times.iteritems():
            count += session.count
        self.__processed = count
        self.__sessions = times

    def _alreadyRead(self, host):
        if host in self.__read:
            return True
        return False

    def search(self, infix=''):
        sessions = []

        for host,session in self.__sessions.iteritems():
            if infix in host or infix in session.hostname:
                sessions.append(session)
        return sessions
    def prefix(self, prefix=''):
        sessions = []
        for host, session in self.__sessions.iteritems():
            if prefix == session.hostname.split(".")[0]:
                sessions.append(session)
        return sessions
    @property
    def processed(self):
        return self.__processed
    @property
    def sessions(self):
        return self.__sessions
