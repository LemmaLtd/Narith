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
		'pcap': self.pcap,
		'domains': self.domain,
		'local': self.local,
                #'var': self.var,
                }
        self.level = None
        self.levels = ['core', 'high', 'low']
        self.ext_msg = "\n[+] Thanks for using 'Narith', have a nice day"

    def pcap(self,x):
	print x

    def domain(self,x):
	print x

    def local(self,x):
	print x

    def executer(self):
        #from environment import complete
        #complete.tab()
        while True:
            command = raw_input(colored("Narith: >", 'blue', attrs=['underline']) + " ").lower()
            command_list = command.split()
            if command == 'exit':
                exit(colored(self.ext_msg, 'red'))
            else:
                try:
                   try:
                      self.commands[command_list[0]](command_list)
                   except IndexError:
                      pass
                except KeyError:
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
                            command = raw_input(cli).lower()
                        except KeyboardInterrupt:
                            print ""
                            break

                        command_list = command.split()
                        if command == 'back':
                            self.module = None
                            break
                        elif command == 'exit':
                            exit(colored(self.ext_msg, 'red'))
                        else:
                            try:
                                try:
                                    self.commands[command_list[0]](command_list)
                                except IndexError:
                                    pass
                            except KeyError:
                                cprint('[!] Command not found, run "help" to get available commands', 'red')
                else:
                    cprint("[!] Module not found run list modules to get available modules", 'red')

            elif command[1] == 'level':
                if command[2] in self.levels:
                    self.level = command[2]
                    self.module = None
                    while True:
                        cli = colored('Narith: level({0}) > ',
                                      attrs=['underline']).format(colored(self.level, 'yellow'))
                        command = raw_input(cli).lower()
                        command_list = command.split()
                        if command == 'back':
                            self.level = None
                            self.module = None
                            break
                        elif command == 'exit':
                            exit(colored(self.ext_msg, 'red'))
                        else:
                            try:
                                try:
                                    self.commands[command_list[0]](command_list)
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
	    print "CURRENT:",self.module
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
        except Exception as e:
	    print e
            cprint("[!] Use a module first or run 'list'", 'red')

    def list(self, command):
        if len(command) == 2:
            if command[1] == 'levels':
                cprint('[+] Available levels are [Base, Core, High]', 'green')
            elif command[1] == 'modules':
                if self.level:
                    if self.level == 'core':
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

interpreter = RabbitInterpreter()

