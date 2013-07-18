#!/usr/bin/env python


from distutils.core import setup
from os.path import abspath, dirname, join

dir = dirname(abspath(__file__))
description = "Anything Goes here, not now at least"

setup(	name="Narith",
	version="0.0.1",
	description=description,
	author="Saad Talaat and Mahmoud Magdy",
	author_email="saadtalaat[at]gmail[dot]com and hard.man179[dot]gmail[dot]com",
	url="https://github.com/SaadTalaat/Narith/",
	packages=[join(dir,"Narith")],
	classifiers=(
		'License :: OSI Approved :: GNU General Public License (GPL)',
		'Natural Language :: English',
		'Programming Language :: Python'
		),
	license="GPL",
	platforms="Posix")
