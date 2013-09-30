
from Narith.base.Packet.Packet import Packet
from Narith.base.Protocols.Http import Http

class BrowseExtractor(object):

	def __init__(self, packets):

		self.__packets = packets
		self.hosts = []
		self.rqs = []
		self.requests = {}
		self.responses = []
		self.extract()

	def extract(self):

		for p in self.__packets:
			http = self._Http(p)
			if not http or http.truncated: 
				continue

			if http.type == 'request':
				req = {}
				req['host'] = http.host
				req['method'] = http.method
				req['path'] = http.path
				req['headers'] = http.requestHeaders
				if http.method == "POST":
					req['body'] = http.requestBody

				self.rqs.append(req)

				self.hosts.append({http.host: http.method})
				try:
					self.requests[http.host]['times'] += 1
				except:
					self.requests[http.host] = {'times': 1}
				try:
					self.requests[http.host][http.method] += 1
				except:
					self.requests[http.host][http.method] = 1
			elif http.type == 'response':
				res = {}
				res['status'] = http.status
				res['headers'] = http.responseHeaders

				self.hosts.append({'response': http.status})
				




	def _Http(self, packet):
		for protocol in packet:
			if type(protocol).__name__ == 'Http':
				return protocol

