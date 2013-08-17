'''
[Narith]
File: completer.py
Author: Saad Talaat
Date: 17th August 2013
brief: autocompletes and keeps record of user commands
########################
# Disclaimer:
# part of this code is part of webhandler software
# author: Ahmed Shawky aka lnxg33k
########################
'''
from Narith.user.interpreter import interpreter
from Narith.user.banner import banner
try:
	import readline
except:
	print "[*] 'readline' module is needed to provide line completion and history"

class ARLCompleter:
    def __init__(self,logic):
        self.logic = logic

    def traverse(self,tokens,tree):
        if tree is None:
            return []
        elif len(tokens) == 0:
            return []
        if len(tokens) == 1:
            return [x+' ' for x in tree if x.startswith(tokens[0])]
        else:
            if tokens[0] in tree.keys():
		try:
                	return self.traverse(tokens[1:],tree[tokens[0]])
		except:
			return []
            else:
                return []
        return []

    def complete(self,text,state):
        try:
            tokens = readline.get_line_buffer().split()
            if not tokens or readline.get_line_buffer()[-1] == ' ':
                tokens.append(text)
            results = self.traverse(tokens,self.logic) + [None]
            return results[state]
        except Exception,e:
            print e

commands = {
	'list':
		{
		'levels'	:
				{
				'core':None,
				'base':None,
				'high':None,
				},
		'modules'	:None,
		},
	'help': None,
	'info': interpreter.all_modules,
	'set' :
		{
		'level'		:None,
		'module'	:None,
		},
	'pcap':
		{
		'read'		:None,
		'count'		:None,
		'interface'	:None,
		},
	'domain':
		{
		'www'		:None,
		'all'		:None,
		'search'	:None,
		},
	'local':
		{
		'info'		:None,
		'host'		:None,
		'dns-servers'	:None,
		'mac-addr'	:None,
		},
	}
readline.set_completer_delims(' \t\n;')
readline.parse_and_bind("tab: complete")
#completer = ARLCompleter(commands)
completer = ARLCompleter(commands)
readline.set_completer(completer.complete)
