
class HttpRequest(object):

	def __init__(self, requestData):
		self._data = requestData
		self._type = self._data.split("\r\n")[0].split(' ')[0]

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

		self._host = self.getField("Host")
		self._uri = " ".join(self._data.split("\r\n")[0].split(' ')[1:-1])

	@property
	def length(self):
 	    return len(self._data)

	def getField(self, filter):
		try:
			return self._headers[filter]
		except:
			return 0

	@property
	def body(self):
		parts = '\r\n\r\n'.join(self._data.split('\r\n\r\n'))
		if len(parts) > 1:
			return parts[1:]
		return None
	
	@property  
	def bodyLength(self):
		return len(self.body)

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

	@property
	def host(self):
		return self._host

	@property
	def uri(self):
		return self._uri

	@property
	def url(self):
		try:
			return self.host + self.uri
		except:
			return None

	@property
	def type(self):
		return self._type