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
class Dns(object):

	#raw
	''' 
	queries are structured in order of
	(name - type - class)
	answers are structured in this order
	(name - type - class - ttl - data len - addr)
	'''

	def __init__(self,b):
		self.__dns = {'id' : None, 'queries': [],'answers':[]}
		self.__answers = []
		self.__dns['id'] = int(b[:2].encode('hex'),16)
		self.__dns['flags'] = int(b[2:4].encode('hex'),16)
		self.__dns['nqs'] = int(b[4:6].encode('hex'),16)
		self.__dns['ansrr'] = int(b[6:8].encode('hex'),16)
		self.__dns['authrr'] = int(b[8:10].encode('hex'),16)
		self.__dns['addrr'] = int(b[10:12].encode('hex'),16)
		self.__b = b
		queries = b[12:]

		for i in range(0,self.__dns['nqs']):
			self.__dns['queries'].append([])
			# Name
			self.__dns['queries'][i].append(".".join(self.extract_name(queries.split('\x00')[0])))
			# Type
			length = len(self.__dns['queries'][i][0]) + 1
			self.__dns['queries'][i].append(int(queries[length:][:3].encode('hex'),16)) 
			# Class
			self.__dns['queries'][i].append(int(queries[length:][3:5].encode('hex'),16))
			queries = queries[len(self.__dns['queries'][i][0])+6:]

		for i in range(0,self.__dns['ansrr']):
			self.__dns['answers'].append([])
			# Name
			self.__dns['answers'][i].append(queries[:2])
			# Type
			self.__dns['answers'][i].append(int(queries[2:4].encode('hex'),16))
			# Class
			self.__dns['answers'][i].append(int(queries[4:6].encode('hex'),16))
			# TTL
			self.__dns['answers'][i].append(str(int(queries[6:10].encode('hex'),16) / 60)+":" +\
							str(int(queries[6:10].encode('hex'),16) % 60))
			# Data Length
			self.__dns['answers'][i].append(int(queries[10:12].encode('hex'),16))

			if len(queries[12:12+self.__dns['answers'][i][4]]) == 4:
				self.__dns['answers'][i].append( ".".join(\
					[str(int(j.encode('hex'),16)) for j in queries[12:16]]) )
			elif len(queries[12:12+self.__dns['answers'][i][4]]) > 4:
				self.__dns['answers'][i].append( queries[12:12+self.__dns['answers'][i][4]] )
			else:
				raise ValueError,"DNS name empty"

			queries = queries[12+self.__dns['answers'][i][4]:]

		self._names(b)

	def _names(self,b):
		if len(self.__dns['answers']) == 0:
			return
		ans = []
		for answer in self.__dns['answers']:
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

		self.__answers = ans

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
		return self.__dns['id']

	@property
	def type(self):
		return ['query','response'][self.__dns['flags'] >> 15]

	@property
	def queryCount(self):
		return self.__dns['nqs']

	@property
	def answerCount(self):
		return self.__dns['ansrr']

	@property
	def queries(self):
		return self.__dns['queries']
	@property
	def answers(self):
		return self.__answers
