'''
[Narith]
File: Files.py
Author: Saad Talaat
Date: 31th August 2013
brief: Extracting Files
'''
from Narith.core.Integration.TcpIntegrator import TcpIntegrator

class FileExtractor(object):

	def __init__(self, packets):
		integrator = TcpIntegrator(packets)
		integrator.integrate()
		integrator.verify()
		self.__as = integrator.assemblies

	def extract(self):
		import md5, datetime, os
		for a in self.__as:
			encoder = md5.new()
			d = datetime.datetime.now().strftime("%Y-%m-%d:%H")
			data = "".join(map(lambda x: x.data.data,a))
			encoder.update(data)
			code = encoder.digest()
			try:
				fd = open("Data/Files (" + d + ")/" + str(a[0].srcdst) + " - " + code.encode('hex'),'w')
			except:
				os.makedirs("Data/Files (" + d + ")/")
				fd = open("Data/Files (" + d + ")/" + str(a[0].srcdst) + " - " + code.encode('hex'),'w')
			fd.write(data)
			fd.close()

	# Size is not accurate since we're reckoning that any exchanged data is a file
	@property
	def size(self):
		return len(self.__as)
