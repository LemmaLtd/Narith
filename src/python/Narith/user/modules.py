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
        print '     search <infix>\t\treads a substring and searches for domains that match'

    def local_module(self):
        print ''
        cprint('Local information module', 'green')
        print '=======================\n'
        print '     info                        Lists all information obtained about local host'
        print '     host\t\t\tPrints both the local ip and hostname if exists'
        print '     dns-servers\t\t\tPrints all dns servers used by local host'
        print '     mac-addr                    Prints the local host mac address'

    def core(self):
        print ''
        cprint('List of core modules', 'red')
        print '====================='
        print '    pcap\t\t\tSpecialized in extracting data from pcap'
        print '    local\t\tSpecialized in extracting data about local user'
        print '    domain\t\tSpecialized in extracting data about domain names'

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
