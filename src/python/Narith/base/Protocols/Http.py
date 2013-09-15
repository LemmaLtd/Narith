
from Narith.base.Packet.Protocol import Protocol


class Http(Protocol):

	def __init__(self, b):
		self.b = b
		self.length = len(b)
		self.corrupted = 0
		self.type = None
		self.__verbs = ['OPTIONS', 'GET', 'HEAD', 'POST', 'PUT', 'DELETE', 'TRACE', 'CONNECT']

		#truncated means it's a Continuation or non-HTTP traffic
		self.truncated = 0

		if 'HTTP' not in b:
			self.truncated = 1
			return

		verbPart = b.split('HTTP')[0]

		for v in self.__verbs:
			if v in verbPart:
				self.type = 'request'
				self.method = v
				self.host = b.split('Host: ')[1].split('\n')[0]
				self.requestLine = v + ''.join(b.split('\r\n')[0].split(v)[1:])
				self.path = self.requestLine.split(' ')[1]
				b = b.split(self.requestLine)[1]
				if self.method == 'POST':
					self.body = '\r\n\r\n'.join(b.split('\r\n\r\n')[1:])
					b = b.split('\r\n\r\n')[0]

				header = b.replace('\r\n', ': ').split(': ')[1:]
				self.headers = {}
				i = 0
				while i < len(header):
					try:
						self.headers[header[i]] = header[i+1]
					except:
						pass
					i = i + 2
				break

		if self.type == None:
			self.type = 'response'
			self.status = (b.split('HTTP')[1].split(' ')[1], ' '.join(b.split('HTTP')[1].split(' ')[2:]).split('\r')[0])
			self.responseLine = 'HTTP' + b.split('\r\n')[0].split('HTTP')[1]
			b = b.split(self.responseLine)[1]

			header = b.replace('\r\n', ': ').split(': ')[1:]
			self.headers = {}
			i = 0
			while i < len(header):
				try:
					self.headers[header[i]] = header[i+1]
				except:
					pass
				i = i + 2