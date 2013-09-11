'''
[Narith]
File:   Dns.py
Author: Saad Talaat
Date:   27th July 2013
brief:  Structure to hold DNS info
'''

''' Note to self:
    register this code in code obfuscation competition
'''
from Narith.base.Packet.Protocol import Protocol
import threading

class Dns(Protocol):

    #raw
    ''' 
    queries are structured in order of
    (name - type - class)
    answers are structured in this order
    (name - type - class - ttl - data len - addr)
    '''

    def __init__(self,b):
    	super( Dns, self).__init__()
    	self.__dns =  {'id' : None, 'queries': [],'answers':[]}
    	self.__answers = []
    	self.corrupted = False

    	try:
    		#self.__dns['id'] 	= int(b[:2].encode('hex'),16)
    		#self.__dns['flags'] 	= int(b[2:4].encode('hex'),16)
    		#self.__dns['nqs'] 	= int(b[4:6].encode('hex'),16)
    		#self.__dns['ansrr'] 	= int(b[6:8].encode('hex'),16)
    		#self.__dns['authrr'] 	= int(b[8:10].encode('hex'),16)
    		#self.__dns['addrr'] 	= int(b[10:12].encode('hex'),16)
    		self.__dns['len'] 	= len(b)
    		self.__b = b[:self.length]
    		self.__binary = b[:self.length]

    	except:
    		self.corrupted = True
    		return



    def _names(self,b,answers):
    	if len(answers) == 0:
    		return
    	ans = []
    	for answer in answers:
    		off = int(answer[0][1].encode('hex'),16)
    		answer[0] = ".".join(self.extract_name(b[off:].split('\x00')[0]))

    		# Host address?? IP: leave it
    		if answer[1] == 1:
    			ans.append(answer)
    			continue
    		# Cname? domain: construct it
    		elif answer[1] == 5:
    			
    			answer[5] = ".".join(self.extract_name(answer[5]))
    			ans.append(answer)

    	return ans

    def extract_name(self,y):
    	if len(y) == 0:
    		return []

    	length = int(y[0].encode('hex'),16)

    	if(length == 0xc0):
    		off 	= int(y[1].encode('hex'),16)
    		tokens 	= self.extract_name(self.__b[off:].split('\x00')[0])
    		return tokens

    	y = y[1:]
    	return [y[:length]] + self.extract_name(y[length:])


    ##############################
    # Properties

    @property
    def identity(self):
    	return int(self.__binary[:2].encode('hex'),16)

    @property
    def type(self):
        flags = int(self.__binary[2:4].encode('hex'),16)
    	return ['query','response'][flags >> 15]

    @property
    def queryCount(self):
    	return int(self.__binary[4:6].encode('hex'),16)

    @property
    def answerCount(self):
    	return int(self.__binary[6:8].encode('hex'),16)

    @property
    def queries(self):
        qrs = []
    	queries = self.__binary[12:]
        self.qindex = 12

    	try:
    	    for i in range(0,self.queryCount):
                qrs.append([])
    		# Name
                qrs[i].append(".".join(self.extract_name(queries.split('\x00')[0])))
                # Type
                length = len(qrs[i][0]) + 1
                qrs[i].append(int(queries[length:][:3].encode('hex'),16)) 
                # Class
                qrs[i].append(int(queries[length:][3:5].encode('hex'),16))
                self.qindex += len(qrs[i][0]) + 6
                queries = queries[len(qrs[i][0])+6:]
        except:
            self.corrupted = True
        return qrs

    @property
    def answers(self):
        ans = []
        qrs = self.queries
        queries = self.__binary[self.qindex:]
        for i in range(0,self.answerCount):
    		ans.append([])
    		# Name
    		ans[i].append(queries[:2])
    		# Type
    		ans[i].append(int(queries[2:4].encode('hex'),16))
    		# Class
    		ans[i].append(int(queries[4:6].encode('hex'),16))
    		# TTL
    		ans[i].append(str(int(queries[6:10].encode('hex'),16) / 60)+":" +\
    					str(int(queries[6:10].encode('hex'),16) % 60))
    		# Data Length
    		ans[i].append(int(queries[10:12].encode('hex'),16))
 		if len(queries[12:12+ans[i][4]]) == 4:
   			ans[i].append( ".".join(\
    				[str(int(j.encode('hex'),16)) for j in queries[12:16]]) )
    		elif len(queries[12:12+ans[i][4]]) > 4:
    			ans[i].append( queries[12:12+ans[i][4]] )
    		else:
    			#SHOULD DO SOMETHING
    			return
    	return self._names(self.__binary, ans)

    @property
    def length(self):
    	return self.__dns['len']

    @property
    def iscorrupted(self):
    	return self.corrupted
