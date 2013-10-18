'''
[Narith]
File:   HttpResponse.py
Author: Anwar Mohamed
Date:   16th Oct 2013
brief:  Http response object
'''

class HttpResponse(object):

	def __init__(self, responseData):
		self._data = responseData
		self._status = self._data.split('\r\n')[0].split(' ')[1];

		header = self._data.split('\r\n\r\n')[0].replace('\r\n', ': ').split(': ')[1:]
		self._headers = {}
		i = 0
		while i < len(header):
			try:
				if len(header[i]) > 0 and len(header[i+1]) > 0:
					self._headers[header[i]] = header[i+1]
			except:
				pass
			i = i + 2


	@property
	def status(self):
 	    return self._status

	@property
	def length(self):
 	    return len(self._data)

	def getField(self, filter):
		try:
			return self._headers[filter]
		except:
			return None

	@property
	def body(self):
		if self._status == '200' or self._status == '302':
			parts = '\r\n\r\n'.join(self._data.split('\r\n\r\n')[1:])
			if len(parts) > 1:
				return parts[1:]
		return None
	
	@property  
	def bodyLength(self):
		if self.body:
			return len(self.body)
		return 0

	@property  
	def fields(self):
		return self._headers

	@property
	def fieldsCount(self):
	    return len(self._headers)

	@property
	def header(self):
		return self._data.split('\r\n\r\n')[0]
	
	def encodedBody(self, enc = 'plain'):
		if enc == 'plain':
			return self.body
		elif enc == 'hex':
			return self.body.encode("hex")
		elif enc == 'byte':
			return bytearray(self.body)
		else:
			return self.body
