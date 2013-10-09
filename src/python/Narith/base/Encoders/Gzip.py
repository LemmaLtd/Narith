'''
[Narith]
File: Gzip.py
Author: Saad Talaat
Date: 9th October 2013
brief: Gzip encoder/decoder
'''
from Narith.design.Meta import Patterns
from StringIO import StringIO
import gzip

class GzipDecoder(object):
    __metaclass__ = Patterns.Singleton

    @staticmethod
    def decodeRaw(data):
        stream = StringIO(data)
        gzipper = gzip.GzipFile(fileobj=stream)
        decompressed = gzipper.read()
        gzipper.close()
        stream.close()
        return decompressed

    @staticmethod
    def encodeRaw(data):
        stream = StringIO()
        gzipper = gzip.GzipFile(fileobj=stream, mode='w')
        gzipper.write(data)
        gzipper.close()
        compressed = stream.getvalue()
        stream.close()
        return compressed
    @staticmethod
    def isGzip(data):
        return '\x1f\x8b\x08' in data
