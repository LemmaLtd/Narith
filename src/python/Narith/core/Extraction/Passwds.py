'''
[Narith]
File: Passwds.py
Author: Diaa Diab @dia2diab
Review: Saad Talaat
brief: Extracting passwrods from packet sequence
'''

from Narith.base.Packet.Packet import Packet
from Narith.base.Protocols.Ftp import Ftp


class PasswdExtractor(object):
    class Token(object):
        def __init__(self, tupl):
            self.__tupl = list(tupl)
            if len(self.__tupl) < 4:
                raise(IndentationError, "Invalid arugment or list element type")

        @property
        def user(self):
            return self.__tupl[0]

        @property
        def passwd(self):
            return self.__tupl[1]

        @property
        def server(self):
            return self.__tupl[2]

        @property
        def client(self):
            return self.__tupl[3]

    def __init__(self, packets):

        if type(packets) != list and packets != [] and type(packets[0]) != Packet:
            raise TypeError("Invalid arugment or list element type")
        self.__packets = packets
        self.__data = []
        self.__ftps = []

    def extract(self):

        for packet in self.__packets:
            ftp = self.__hasFtp(packet)
            if not ftp or ftp.iscorrupted:
                continue

            else:
                self.__ftps.append(ftp)
                if ftp.type == 'response' and ftp.code == 230:
                    local = self.destination(ftp)
                    remote = self.source(ftp)
                    prev = self.__ftps[self.__ftps.index(ftp) - 1]
                    if prev.type == 'request' and 'PASS' in prev.cmd:
                        passwd = prev.arg.replace('\r\n', '')
                        prev_prev = self.__ftps[self.__ftps.index(prev) - 2]
                        if prev_prev.type == 'request' and 'USER' in prev_prev.cmd:
                            user = prev_prev.arg.replace('\r\n', '')
                            self.__data.append(self.Token((user, passwd, remote, local)))
        return self.__data

    def destination(self, packet):
        return packet.prev.prev.src

    def source(self, packet):
        return packet.prev.prev.dst

    def __hasFtp(self, packet):

        for protocol in packet:
            if type(protocol).__name__ == 'Ftp':
                return protocol

            else:
                continue
        return False

    @property
    def data(self):
        return self.__data
