'''
[Narith]
File: interpreter.py
Author: Saad Talaat
Date: 17th August 2013
brief: interepets and execute user commands
########################
# Disclaimer:
# part of this code is part of webhandler software
# author: Ahmed Shawky aka lnxg33k
########################
'''

from Narith.user.termcolor import colored, cprint
from Narith.user.modules import Modules
from Narith.base.Analysis.Classifier import Classifier

class RabbitInterpreter(Modules):
    """
    The following class is the core of the interpreter
    """
    def __init__(self):
        Modules.__init__(self)  # calling the constructor method from the base class
        self.commands = {
                'help': self.help,
                'list': self.list,
                'info': self.info,
                'set': self.set,
                #'var': self.var,
                }

        self.level = None
        self.levels = ['core', 'high', 'low']
        self.ext_msg = "\n[+] Thanks for using 'Narith', have a nice day"
	######
	# Module related variables
	##########################
	self.__pcap = None
	self.__local = None
	self.__domain = None
	self.__session = None

	#######
	# Aiding modules
	######################
	self.__classifier = None
    def executer(self):
        #from environment import complete
        #complete.tab()
        while True:
            command = raw_input(colored("Narith: >", 'blue', attrs=['underline']) + " ")
            command_list = command.split()
            if command == 'exit':
                exit(colored(self.ext_msg, 'red'))
            else:
                try:
                   try:
                      self.commands[command_list[0]](command_list)
                   except IndexError:
			pass
                except KeyError, TypeError:
                   cprint('[!] Command not found, run "help" to get available commands', 'red')

    def set(self, command):
        '''
        Sets a module to use if it is within
        the list of modules of the level

        :param command: the module to be used
        '''
        if len(command) != 3:
            cprint("[!] Use set command to set either a module or a level", 'red')
        else:
            if command[1] == 'module':
                self.assign_modules()
                if self.modules and command[2] in self.modules:
                    self.module = command[2]
                    while True:
                        try:
                            cli = colored(
                                          'Narith: level({0}): module({1}) > ',
                                          attrs=['underline']).format(
                                                                      colored(self.level, 'yellow'),
                                                                      colored(self.module, 'yellow'))
                            command = raw_input(cli)
                        except KeyboardInterrupt:
                            print ""
                            break

                        command_list = command.split()
			command_list[0] = command_list[0].lower()
                        if command == 'back':
                            self.module = None
                            break
                        elif command == 'exit':
                            exit(colored(self.ext_msg, 'red'))
                        else:
                            try:
                                try:
				    import datetime, time
				    start_time = datetime.datetime.fromtimestamp(time.time()).strftime("%M:%S")
                                    self.commands[command_list[0]](command_list)
				    end_time = datetime.datetime.fromtimestamp(time.time()).strftime("%M:%S")
				    cprint("[%] Time elapsed: "+start_time+" ~ "+end_time,"white","on_red")
                                except IndexError:
                                    pass
                            except KeyError:
                                cprint('[!] Command not found, run "help" to get available commands', 'red')
                else:
                    cprint("[!] Module not found run list modules to get available modules", 'red')

            elif command[1] == 'level':
                if command[2] in self.levels:
                    self.level = command[2]
		    self.update_commands(self.level)
                    self.module = None
                    while True:
                        cli = colored('Narith: level({0}) > ',
                                      attrs=['underline']).format(colored(self.level, 'yellow'))
                        command = raw_input(cli)
                        command_list = command.split()
			command_list[0] = command_list[0].lower()
                        if command == 'back':
                            self.level = None
                            self.module = None
			    self.update_commands()
                            break
                        elif command == 'exit':
                            exit(colored(self.ext_msg, 'red'))
                        else:
                            try:
                                try:
				    import datetime, time
				    start_time = datetime.datetime.fromtimestamp(time.time()).strftime("%M:%S")
                                    self.commands[command_list[0]](command_list)
				    end_time = datetime.datetime.fromtimestamp(time.time()).strftime("%M:%S")
				    print ""
				    cprint("[%] Time elapsed: "+start_time+" ~ "+end_time+"","white","on_red")
                                except IndexError:
                                    pass
                            except KeyError:
                                cprint('[!] Command not found, run "help" to get available commands', 'red')
                else:
                    cprint('[!] Unknown level, run "list levels" to get available levels', 'red')
            else:
                pass


    def info(self, command):
        try:
            if self.module:
                self.assign_modules()
                # get the used module in case single arg provided 'info'
                if len(command) == 1:
                    try:
                        self.modules[self.module]()
                    except AttributeError:
                        cprint("[!] Use a module first or run 'list'", 'red')
                else:
                    module = command[1]
                    if module in list(self.modules):
                        self.modules[module]()
                    else:
                        cprint("[!] Module not found run 'list modules' to get available modules", 'red')
            else:
                cprint("[!] Use a module first or run 'list'", 'red')
        except Exception:
            cprint("[!] Use a module first or run 'list'", 'red')

    def list(self, command):
        if len(command) == 2:
            if command[1] == 'levels':
                cprint('[+] Available levels are [Base, Core, High]', 'green')
            elif command[1] == 'modules':
                if self.level:
                    if self.level   == 'core':
                        self.core()
                    elif self.level == 'high':
                        self.high()
                    elif self.level == 'base':
                        self.low()
                else:
                    cprint('[!] Set level before listing modules', 'red')
        else:
            err_msg = "[!] List is used to show either levels or modules\n"
            err_msg += "eg) list modules"
            cprint(err_msg, 'red')

    def assign_modules(self):
        '''
        the following method assigns the instance
        self.modules to it's appropriate value
        depends on the choosed level
        '''
        if self.level == 'core':
            self.modules = self.core_modules
        elif self.level == 'high':
            self.modules = self.high_modules
	elif self.level == 'base':
	    self.modules = self.base_modules
	else:
	    self.modules = None


    def help(self, command):
        print ""
        print "General Commands"
        print "================\n"
        print "     command                      Description"
        print "     -------                      -----------"
        print "     help                         Brings you this help"
        print "     level core/low/high          Select level of modules to work on"
        print "     list /func                   Lists modules/functions withina  level <modules/functions>"
        print "     use <module>                 Loads a module to use"
        print "     var <var> <value>            Sets a variable to a value"
        print "     commit                       Commits updates"
        print "     info /<function>             Infos about module or a specified function"
        print "     exit                         exits the current task (module)"
        print "     quit                         Not yet implemented but you can try it"
        print ""

    '''
    Update commands functions:
	On level transation, commands are injected and ejected
	from the commands dictionary.. to govern this we should
	make active commands exclusive to active level
    '''

    def update_commands(self, level=None):
	if level == 'core':
		self.update_core(1)
		self.update_base(0)
		self.update_high(0)
	else:
		self.update_core(0)
		self.update_base(0)
		self.update_high(0)

    def update_core(self, flag):
        if flag:
            self.commands['pcap']   = self.pcap
            self.commands['local']  = self.local
            self.commands['domain'] = self.domain
            self.commands['browse'] = self.browse
            self.commands['session'] = self.session
        else:
            self.commands['pcap']   = None
            self.commands['local']  = None
            self.commands['domain'] = None
            self.commands['browse'] = None
            self.commands['session']= None

    def update_base(self, flag):
	pass
    def update_high(self, flag):
	pass


    '''
     Module interfaces:
	Each module is responsible for processing its arguments

    '''
    def pcap(self,command):
	from Narith.user.modules import PcapInterface
	if not self.__pcap or command[1] == 'read':
		cprint("[>] Initializing pcap module",'blue')
		self.__pcap = PcapInterface()
		self.__classifier = None
		self.__domain     = None
		self.__local      = None
		self.__session    = None

	self.__pcap.executer(command[1:])
	import threading
	if not self.__classifier:
		cprint("[>] Classifying raw packets",'blue')
		self.__classifier = Classifier(self.__pcap.pcap[0].packets[0:])
		threading.Thread(target=self.__classifier.classify).start()
		self.__packets    = self.__classifier.packets
		cprint("[>] Verifying structured packets",'blue')
		#self.__corrupted  = threading.Thread(target=self.__classifier.verify).start()
		if self.__classifier.corrupted:
			cprint("[!] corrupted packets: " + str(self.__classifier.corrupted),'red')


    def domain(self,command):
	from Narith.user.modules import DomainInterface
	if not self.__pcap:
		cprint('[!] No file read','red')
		return

	if not self.__domain or not self.__domain.pcap == self.__pcap.pcap[0]:
		cprint("[>] Initializing domain module",'blue')
		self.__domain = DomainInterface(self.__pcap.pcap[0], self.__packets[0:])

	self.__domain.executer(command[1:])

    def browse(self, command):
        from Narith.user.modules import BrowseInterface

        if not self.__pcap:
            cprint('[!] No file read','red')
            return

        self.__browser = BrowseInterface(self.__pcap.pcap[0], self.__packets[0:])
        self.__browser.executer(command[1:])



    def local(self,command):
	from Narith.user.modules import DomainInterface
	from Narith.user.modules import LocalInterface

	if not self.__pcap:
		cprint('[!] No file read','red')
		return

	if not self.__domain or not self.__domain.pcap == self.__pcap.pcap[0]:
		self.__domain = DomainInterface(self.__pcap.pcap[0], self.__packets[0:])

	if not self.__local:
		cprint("[>] Initializing localinfo module",'blue')
		self.__local = LocalInterface(self.__pcap.pcap[0], self.__packets[0:],self.__domain.extractor)

	self.__local.executer(command[1:])


    def session(self, command):
	from Narith.user.modules import DomainInterface
	from Narith.user.modules import SessionInterface
	if not self.__pcap:
		cprint ('[!] No file read','red')
		return

	if not self.__domain or not self.__domain.pcap == self.__pcap.pcap[0]:
		self.__domain = DomainInterface(self.__pcap.pcap[0], self.__packets[0:])

	if not self.__session:
		cprint("[>] Initializing session module",'blue')
		self.__session = SessionInterface(self.__pcap.pcap[0], self.__packets[0:], self.__domain.extractor)
	self.__session.executer(command[1:])

interpreter = RabbitInterpreter()

