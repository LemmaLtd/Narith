
from Narith.base.Packet.Protocol import Protocol


class Http(Protocol):


    def __init__(self, b):
        self._binary = b
        self._length = len(b)
        self.corrupted = 0
        # self.type = None
        self.__verbs = ['OPTIONS', 'GET', 'HEAD', 'POST', 'PUT', 'DELETE', 'TRACE', 'CONNECT']


    @property
    def data(self):
        if self._binary and 'HTTP' not in self._binary:
            return self._binary
        elif self._binary and 'HTTP' not in self._binary:
            return '\r\n\r\n'.join(self._binary.split('\r\n\r\n')[1:])
        return False

    @property
    def length(self):
        return self._length

    @property
    def type(self):
        if 'HTTP' not in self._binary:
            return 'data'
        verbPart = self._binary.split('HTTP')[0]
        for v in self.__verbs:
            if v in verbPart:
                return 'request'
        return 'response'


    #######################
    # Request properties
    #######################

    @property
    def method(self):
        if self.type != 'request':
            return False
        verbPart = self._binary.split('HTTP')[0]
        for v in self.__verbs:
            if v in verbPart:
                return v

    @property
    def host(self):
        if self.type != 'request':
            return False
        return self._binary.split('Host: ')[1].split('\n')[0]

    @property
    def path(self):
        if self.type != 'request':
            return False
        method = self.method
        requestLine = method + ''.join(self._binary.split('\r\n')[0].split(method)[1:])
        return requestLine.split(' ')[1]

    @property
    def requestBody(self):
        if self.type != 'request':
            return False
        method = self.method
        b = self._binary
        requestLine = method + ''.join(b.split('\r\n')[0].split(method)[1:])
        b = b.split(requestLine)[1]
        if method == 'POST':
            return '\r\n\r\n'.join(b.split('\r\n\r\n')[1:])

    @property
    def requestHeaders(self):
        if self.type != 'request':
            return False
        method = self.method
        b = self._binary
        requestLine = method + ''.join(b.split('\r\n')[0].split(method)[1:])
        b = b.split(requestLine)[1]
        b = b.split('\r\n\r\n')[0]
        header = b.replace('\r\n', ': ').split(': ')[1:]
        headers = {}
        i = 0
        while i < len(header):
            try:
                headers[header[i]] = header[i+1]
            except:
                pass
            i = i + 2
        return headers

    ########################
    # Response properties
    ########################

    @property
    def status(self):
        if self.type != 'response':
            return False
        b = self._binary
        return (b.split('HTTP')[1].split(' ')[1], ' '.join(b.split('HTTP')[1].split(' ')[2:]).split('\r')[0])

    @property
    def responseHeaders(self):
        if self.type != 'response':
            return False
        b = self._binary
        responseLine = 'HTTP' + b.split('\r\n')[0].split('HTTP')[1]
        b = b.split(responseLine)[1]

        header = b.replace('\r\n', ': ').split(': ')[1:]
        headers = {}
        i = 0
        while i < len(header):
            try:
                headers[header[i]] = header[i+1]
            except:
                pass
            i = i + 2

        return headers
    @property
    def responseBody(self):
        if self.type != 'response':
            return False
        b = self._binary
        status = self.status
        if status[0] == '200' or status[0] == '302':
            return '\r\n\r\n'.join(b.split('\r\n\r\n')[1:])
        return False
