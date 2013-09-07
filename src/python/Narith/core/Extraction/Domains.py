'''
[Narith]
File: Domains.py
Author: Saad Talaat
Date: 16th August 2013
brief: Extracting domains from packet sequence
'''
from Narith.base.Packet.Packet import Packet
from Narith.base.Protocols.Dns import Dns

class DomainExtractor(object):
    def __init__(self, packets):
        if type(packets) != list and packets != [] and type(packets[0]) != Packet:
            raise TypeError,"Invalid arugment or list element type"
        self.__packets = packets
        self.__domains = []
        self.__servers = []
        self.extract()

    def extract(self):
        qa = []
        if self.__domains:
            return self.__domains

        for packet in self.__packets:
            dns = self._hasDns(packet)
            if not dns:
                continue
            try:
                a = []
                for answer in dns.answers:
                    a.append([answer[0],answer[len(answer)-1]])
                for answer in dns.answers:
                    if answer and (dns.prev.prev.src not in self.__servers):
                        self.__servers.append(dns.prev.prev.src)
                        self.__host = dns.prev.prev.dst
                qa.append(a)
            except:
                pass
        self.__domains = qa
        return qa
                
    def wwwExtract(self):
        qa = []
        for domains in self.__domains:
            for domain in domains:
                if domain and ("www" in domain[0]) and (domain not in qa) and self._isIP(domain[1]):
                    domip = domain[0],domain[1]
                    qa.append(domip)
        return qa

    def _hasDns(self, packet):
        for protocol in packet:
            if type(protocol).__name__ == 'Dns':
                return protocol
            else:
                continue
        return False        
    def _isIP(self,ip):
        if type(ip) != str:
            return False
        octets = ip.split(".")
        if len(octets) != 4:
            return False
        for octet in octets:
            try:
                int(octet)
            except:
                return False
        return True

    def domains(self, infix=''):
        qa = []
        for domains in self.__domains:
            for domain in domains:
                if domain and (infix in domain[0]) and (domain not in qa) and self._isIP(domain[1]):
                    domip = domain[0],domain[1]
                    qa.append(domip)
        return qa

    def lookup(self, ip):
        for domains in self.__domains:
            for domain in domains:
                if ip == domain[1] and 'www' == domain[0].split(".")[0]:
                    return domain[0]
        return ip

    @property
    def domainlist(self):
        return self.__domains

    @property
    def servers(self):
        return self.__servers

    @property
    def host(self):
        try:
            return self.__host
        except:
            return ''
