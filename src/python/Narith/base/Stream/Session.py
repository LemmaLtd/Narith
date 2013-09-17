'''
[Narith]
Author: Saad Talaat
Date: 17th Sept 2013
Brief:  Session class
'''


class Session(object):
    def __init__(self):
        self.__ip = None
        self.__start = None
        self.__end = None
        self.__count = 1
        self.__bytes = 0
        self.__host = None
        self.packets = []

    @property
    def hostname(self):
        return self.__host

    @hostname.setter
    def hostname(self, val):
        self.__host = val

    @property
    def host(self):
        return self.__ip

    @host.setter
    def host(self,val):
        self.__ip = val

    @property
    def start(self):
        return self.__start

    @start.setter
    def start(self, val):
        self.__start = val

    @property
    def end(self):
        return self.__end

    @end.setter
    def end(self,val):
        self.__end = val

    @property
    def count(self):
        return self.__count

    @count.setter
    def count(self,val):
        self.__count = val

    @property
    def bytes(self):
        return self.__bytes

    @bytes.setter
    def bytes(self, val):
        self.__bytes = val

