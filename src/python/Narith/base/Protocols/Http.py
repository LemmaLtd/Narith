
from Narith.base.Packet.Protocol import Protocol
from Narith.base.Protocols.HttpOpts.HttpRequest import HttpRequest
from Narith.base.Protocols.HttpOpts.HttpResponse import HttpResponse


class Http(Protocol):


    def __init__(self, b):
        self._binary = b
        self._length = len(b)
        self.corrupted = 0
        self.b = b
        # self.type = None
        self.__verbs = ['OPTIONS', 'GET', 'HEAD', 'POST', 'PUT', 'DELETE', 'TRACE', 'CONNECT']

    @property
    def header(self):
        return self._binary.split('\r\n\r\n')[0]

    @property
    def data(self):
        if self._binary and 'HTTP' not in self._binary:
            return self._binary
        elif self._binary and 'HTTP' in self._binary:
            return '\r\n\r\n'.join(self._binary.split('\r\n\r\n')[1:])
        return None

    @property
    def length(self):
        return self._length

    @property
    def type(self):
        if 'HTTP' not in self.header:
            return 'data'
        verbPart = self.header.split('HTTP')[0]
        for v in self.__verbs:
            if verbPart.startswith(v):
                return 'request'
        return 'response'

    @property
    def response(self):
        if self.type != 'response':
            return None
        return HttpResponse(self._binary)


    @property
    def request(self):
        if self.type != 'request':
            return None
        return HttpRequest(self._binary)

    @property
    def status(self):
        if self.type != 'response':
            return None
        b = self._binary
        return (b.split('HTTP')[1].split(' ')[1], ' '.join(b.split('HTTP')[1].split(' ')[2:]).split('\r')[0])
