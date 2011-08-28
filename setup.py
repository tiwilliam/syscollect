#!/usr/bin/python
# coding=utf8

from setuptools import setup

import graphd.static as static

setup(
	name = 'graphd',
	version = str(static.major) + '.' + str(static.minor) + '.' + str(static.patch),
	author = "William Tisäter",
	author_email = "william@defunct.cc",
	description = ("Cross-platform server for distributing graph and system data."),
	license = "BSD",
	keywords = "graphd graph monitoring monitor",
	url = "https://github.com/tiwilliam/graphd",
	packages = ['graphd'],
	classifiers = [
		"Development Status :: 4 - Beta",
		"License :: OSI Approved :: BSD License",
		"Operating System :: MacOS :: MacOS X",
		"Operating System :: POSIX :: Linux",
		"Operating System :: POSIX :: BSD :: FreeBSD",
		"Operating System :: POSIX :: BSD :: OpenBSD",
		"Operating System :: Microsoft :: Windows",
		"Topic :: System :: Monitoring",
		"Topic :: System :: Networking :: Monitoring",
		"Topic :: System :: Systems Administration"
	]
)
