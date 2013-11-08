from importlib import import_module
from os import listdir, path

coreModules = {}

for module in listdir(path.dirname(path.realpath(__file__))):
	if module[-3:] == '.py' and "__init__" not in module and module[-4:] != '.pyc':
		#print module
		coreModules[module[:-3]] = import_module('Narith.user.Modules.base.%s' % module[:-3])

def desc():
	return "Contains base level modules"

def modules():
	return coreModules

def list():
	return coreModules.keys()