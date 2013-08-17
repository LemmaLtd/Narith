"""
[Narith]
File: modules.py
Author: Saad Talaat
Date: 17th August 2013
brief: help representation of provided modules
########################
# Disclaimer:
# part of this code is part of webhandler software
# author: Ahmed Shawky aka lnxg33k
########################
"""
from Narith.user.termcolor import cprint

class Modules(object):
    """
    The following class contains the used
    modules by br and some info about them
    """

    def __init__(self):
	self.high_modules = {}
	self.base_modules = {}
	self.core_modules = {'pcap': self.pcap_module,
	 'local': self.local_module,
	 'domain': self.domain_module}
	self.all_modules = {}
	all_modules = [ x for x in self.core_modules ] + [ x for x in self.base_modules ] + [ x for x in self.high_modules ]
	for module in all_modules:
	    self.all_modules[module] = None

    def pcap_module(self):
	print ''
	cprint('Pcap file module', 'green')
	print '=======================\n'
	print '    read <filename>              Reads a pcap file into narith from given filename'
	print '    count                        provides the number of packets in read pcap file'
	print '    interface                    provides the used interface in the on recorded session'

    def domain_module(self):
	print ''
	cprint('Domains module', 'green')
	print '=======================\n'
	print '     www                         prints out all remote hostnames'
	print '     all                         prints all occurances of all hostnames during session'
	print '     search <infix>              reads a substring and searches for domains that match'

    def local_module(self):
	print ''
	cprint('Local information module', 'green')
	print '=======================\n'
	print '     info                        Lists all information obtained about local host'
	print '     host                        Prints both the local ip and hostname if exists'
	print '     dns-servers                 Prints all dns servers used by local host'
	print '     mac-addr                    Prints the local host mac address'

    def core(self):
	print ''
	cprint('List of core modules', 'red')
	print '====================='
	print '    pcap                         Specialized in extracting data from pcap'
	print '    local                        Specialized in extracting data about local user'
	print '    domain                       Specialized in extracting data about domain names'

    def base(self):
	print ''
	cprint('List of base modules', 'red')
	print '=========================='
	print '    NOT YET                      No low level modules yet defined'

    def high(self):
	print ''
	cprint('List of high modules', 'red')
	print '==========================='
	print '    NOT YET                      No High level modules yet defined'


'''
Module interfaces definitions, each module with own executer.
'''
from Narith.base.Pcap.Pcap import Pcap

class PcapInterface(object):
	__interfaces = \
	{
	0 : 'Undefined',
	1 : 'Ethernet'
	}
	def __init__(self):
		self.__commands = \
		{
		'read' : self.read,
		'count' : self.count,
		'interface' : self.interface,
		}
		self.__pcap = None

	def executer(self, commands):
		if commands[0] not in self.__commands:
			return
		self.__commands[commands[0]](commands[1:])

	def read(self, files):
		p = []
		for f in files:
			pp = Pcap(f)
			p.append(pp)
			if pp.length:
			    cprint(('[*] file %s read' % f),'green')
		self.__pcap = p

	def count(self, files):
		for p in self.__pcap:
			if p.file and p.length:
				cprint('[*] file %s: %d packets' % (p.file,p.length),'green')
			else:
				cprint('[!] Invalid file','red')
				
	def interface(self, files):
		for p in self.__pcap:
			try:
				cprint('[*] file %s: %s' %(p.file, self.__interfaces[p.interface]),'green')
			except:
				cprint('[!] Invalid file','red')
	def has(self, f):
		for p in self.__pcap:
			if p.file == f:
				return True
			else:
				False
	@property
	def pcap(self):
		return self.__pcap

class DomainInterface(object):

	def __init__(self, pcap):
		from Narith.base.Analysis.Classifier import Classifier
		from Narith.core.Extraction.Domains import DomainExtractor

		self.__commands = \
		{
		'www'	: self.www,
		'all'	: self.all,
		'search': self.search,
		}
		self.__domain = None
		self.__pcap = pcap
		packets = Classifier(pcap.packets).classify()
		self.__de = DomainExtractor(packets)
		
	def executer(self, commands):
		if commands[0] not in self.__commands:
			return
		self.__commands[commands[0]](commands[1:])

	def www(self, commands):
		for domain,ip in self.__de.wwwExtract():
			cprint("[*] " + domain + " -> " + ip,'green')

	def all(self, commands):
		for domain,ip in self.__de.domains(''):
			cprint("[*] " + domain + " -> " + ip,'green')

	def search(self, commands):
		for domain,ip in  self.__de.domains(commands[0]):
			cprint("[*] " + domain + " -> " + ip, 'green')
	@property
	def pcap(self):
		return self.__pcap

class LocalInterface(object):

	def __init__(self, pcap):
		from Narith.base.Analysis.Classifier import Classifier
		from Narith.core.Extraction.Local import LocalInfo

		self.__commands = \
	        {
	        'dns-servers'   : self.dns,
	        'info'   : self.info,
	        'host': self.host,
		'mac': self.mac,
	        }
	        self.__local = None
	        self.__pcap = pcap
	        packets = Classifier(pcap.packets).classify()
	        self.__li = LocalInfo(packets)

	def executer(self, commands):
		if commands[0] not in self.__commands:
			return
		self.__commands[commands[0]](commands[1:])

	def dns(self, commands):
		cprint('[*] DNS Servers:','green')
		for server in self.__li.dns_servers:
			cprint('\tServer: %s' % server, 'green')

	def host(self, commands):
		cprint('[*] Host: %s' % self.__li.host, 'green')

	def mac(self, commands):
		cprint('[*] Mac address: %s' % self.__li.mac_address, 'green')

	def info(self, commands):
		self.dns(commands)
		self.mac(commands)
		self.host(commands)
	@property
	def pcap(self):
		return self.__pcap
