'''
[Narith]
File: Files.py
Author: Saad Talaat
Date: 31th August 2013
brief: Extracting Files
'''
from Narith.core.Integration.TcpIntegrator import TcpIntegrator
from Narith.base.Stream.TcpSession import TcpSession
from Narith.base.Stream.FtpSession import FtpSession
import os,datetime

class FileExtractor(object):

    def __init__(self, d="Data/Ftp/"):
        self.d = d
        self.d = self.d + datetime.datetime.now().strftime("%T %d-%m-%y/")
        try:
            os.makedirs(self.d)
        except:
            pass
        return

    def extractFtp(self, sessions):
        written = 0
        for ip_session in sessions:
            s = TcpSession.fromSession(ip_session)
            f = [FtpSession.fromTcpSession(tcp_session) for tcp_session in s]
            #print "FTP",sum(map(lambda x: x != None, f))
            for ftpsession in f:
                if not ftpsession:
                    continue
                fd = open(self.d+str(id(ftpsession)),'w')
                fd.write("".join(ftpsession.data))
                fd.close()
                written +=1
        print "Written:",written,"Files."
'''
class FileExtractor(object):
   def __init__(self, packets):
        integrator = TcpIntegrator(packets)
        integrator.integrate()
        integrator.verify()
        self.__as = integrator.assemblies

    def extract(self):
        import md5, datetime, os
        for a in self.__as:
            encoder = md5.new()
            d = datetime.datetime.now().strftime("%Y-%m-%d:%H")
            data = "".join(map(lambda x: x.data.data,a))
            encoder.update(data)
            code = encoder.digest()
            try:
                fd = open("Data/Files (" + d + ")/" + str(a[0].srcdst) + " - " + code.encode('hex'),'w')
            except:
                os.makedirs("Data/Files (" + d + ")/")
                fd = open("Data/Files (" + d + ")/" + str(a[0].srcdst) + " - " + code.encode('hex'),'w')
            fd.write(data)
            fd.close()

    # Size is not accurate since we're reckoning that any exchanged data is a file
    @property
    def size(self):
        return len(self.__as)

'''
class FtpFileExtractor(object):

    class Sorted(object):

        def __init__(self, tupl):
            self.__tupl = list(tupl)
            if len(self.__tupl) < kaza:
                raise(TypeError, 'Package length error!!')

        @property
        def server(self):
            return

        @property
        def client(self):
            return

        @property
        def data(self):
            return

        @property
        def auth(self):
            return

    def __init__(self, packets):
        if type(packets) != list and packets != [] and type(packets[0]) != Packet:
            raise(TypeError, 'Invalid arugment or list element type')
        self.__packets = packets
        self.__ftpData = []
        self.__ftps = []

    def file(self):
        for packet in self.__packets:
            ftp = self.__hasFtp(packet)
            if not ftp or ftp.iscorrupted:
                continue

            else:
                self.__ftps.append(ftp)

    def source(self, packet):
        return packet.prev.prev.dst

    def destination(self, packet):
        return packet.prev.prev.src

    def __hasFtp(self, packet):
        for protocol in packet:
            if type(protocol).__name__ == 'Ftp':
                return protocol
            else:
                continue
        return False


