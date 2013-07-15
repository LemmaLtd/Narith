'''
[Narith]
File:   ArgManager.py
Author: Saad Talaat
Date:   14th July 2013
brief:  Less general purpose argument matching and retriving
'''
import sys,getopt

class ArgManager():
	__short_args__ = "hvi:"
	__long_args__ = ["ifile=","help"]
	__current__ = sys.argv[1:]
	#Flags
	__verbose__ = False
	def __init__(self):
		self.opts, self.args = getopt.getopt(self.__current__, 
					self.__short_args__, 
					self.__long_args__)
		for opt,val in self.opts:
			if '-v' == opt:
				self.__verbose__ = True
			elif '-h' == opt:
				self.printHelp()
				sys.exit(0)
			else:
				return
	def getOpts(self):
		return self.opts
	def getOptVal(self,opt):
		# support short args for now
		if (opt not in self.__short_args__ ):
			return

		for opt,val in self.opts:
			if ("-"+o) == opt:
				return val
	def printHelp(self):
		print "usage: narith [options] [flags]\n-h\t: view this output.\n-v\t: verbose mode on.\n-i\t: input file.\n-o\t: output file.\n\n\tBy:\n\t\tSaad Talaat<@Sa3dTalaat>\n\t\tMahmoud Hard<@HardMan179>"

