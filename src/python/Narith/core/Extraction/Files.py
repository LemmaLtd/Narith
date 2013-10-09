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
from Narith.base.Stream.HttpSession import HttpSession
from Narith.base.Encoders.Gzip import GzipDecoder
import os,datetime

class FileExtractor(object):
    __decoder = {
            None    : lambda x: x,
            'gzip'  : GzipDecoder.decodeRaw,
                }

    def __init__(self, d="Data/"):
        self.d = d
        self.d = self.d + datetime.datetime.now().strftime("%H %d-%m-%y/")
        try:
            os.makedirs(self.d+"Ftp/")
            os.makedirs(self.d+"Http/")
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
                if not ftpsession or not ftpsession.data:
                    continue
                fd = open(self.d+"Ftp/"+str(id(ftpsession)),'w')
                fd.write("".join(ftpsession.data))
                fd.close()
                written +=1
        return written
    def extractHttp(self, sessions):
        written = 0
        for ip_session in sessions:
            s = TcpSession.fromSession(ip_session)
            h = [HttpSession.fromTcpSession(tcp_session) for tcp_session in s]
            for httpsession in h:
                if not httpsession or not httpsession.data2:
                    continue
                for data in httpsession.data2:
                    if not data:
                        continue
                    fd = open(self.d+"Http/"+str(id(httpsession)),'w')
                    try:
                        decoder = self.__decoder[httpsession.encoding2[httpsession.data2.index(data)]]
                        fd.write(decoder("".join(data)))
                    except Exception as e:
                        #print data
                        pass
                    fd.close()
                    written +=1
        return written
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


