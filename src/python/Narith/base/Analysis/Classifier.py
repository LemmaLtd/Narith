'''
[Narith]
File:     Classifier.py
Author: Saad Talaat
Date:    16th August 2013
brief:    Classifies raw packet wireframes into Protocols and packets
'''
import threading
import time
from Narith.base.Pcap.Pcap import Pcap
from Narith.base.Protocols import Eth, ProtData
from Narith.base.Packet.Packet import Packet
from Narith.design.Concurrency.ThreadPool import TaskPool


class Classifier(object):

    def __init__(self, packets, records=None):
        if type(packets) != list:
            raise TypeError("Unexpected type")
        self.__packets = []
        self.__rawPackets = packets
        self.__records = records
        self.__corrupted = 0
        self.__flag = False
        self.pool = TaskPool(4)
        self.alive = []

    def single(self, packet, index):
        pack = Packet()
        parent = Eth.Eth(packet[:14])
        packet = packet[14:]
        while parent != None or packet != '':
                pack.attach(parent)
                prot = parent.nextProtocol
                if prot == None:
                    packet = packet[parent.length:]
                    break
                parent = prot(packet)
                packet = packet[parent.length:]
        self.__packets[index].append(pack)
        if packet != '':
            pack.attach(ProtData.ProtData(packet))

    def par_classify(self, factor):
        unit = len(self.__rawPackets) / factor
        for x in xrange(factor):
            self.__packets.append([])

        for x in xrange(factor):
            r = self.__rawPackets[unit * x: unit * (x + 1)]
            self.pool.add_task(self.__classify, (r, x))

        time.sleep(1)
        while self.alive:
            continue
        self.__packets = sum(self.__packets, [])

    def __classify(self, ri):
        raw, index = ri
        count = 0
        corrupted = 0
        self.alive.append(True)
        for p in raw:
            self.single(p, index)
        self.alive.pop()

    def verify(self):
        count = 0
        for p in self.__packets:
            invalid = 0
            for prot in p:
                if type(prot).__name__ == 'ProtData':
                    continue
                prot.verify()
                if prot.corrupted:
                    invalid = 1
                    continue

            count += invalid
        self.__corrupted = count

    @property
    def packets(self):
        while self.alive:
            continue
        return self.__packets

    @property
    def records(self):
        return self.__records

    @property
    def size(self):
        return len(self.__packets)

    @property
    def corrupted(self):
        return self.__corrupted

    def classify(self):
        count = 0
        corrupted = 0
        for p in self.__rawPackets:
            count += 1
            packet = Packet()
            parent = Eth.Eth(p[:14])
            p = p[14:]
            invalid = 0

            while parent != None or p != '':
                packet.attach(parent)
                prot = parent.nextProtocol
                if prot == None:
                    p = p[parent.length:]
                    break
                parent = prot(p)
                p = p[parent.length:]
            self.__packets.append(packet)

            if p != '':
                packet.attach(ProtData.ProtData(p))

        #for p in self.__packets:
    #        for protocol in p:
    #            if type(protocol).__name__ == 'Icmpv6':
    #                protocol.notify()
        self.__flag = True
        self.verify()
        self.pool.kill()
