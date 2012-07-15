#!/usr/bin/python

from setuptools import setup

import syscollect.static as static

setup(name=static.name,
      version='%s.%s.%s' % (static.major, static.minor, static.patch),
      author='William Tisäter',
      author_email='william@defunct.cc',
      description=('Cross-platform server for distributing '
                   'graph and system data.'),
      license='BSD',
      keywords='syscollect monitoring monitor data collect collector info',
      url='https://github.com/tiwilliam/syscollect',
      packages=['syscollect'],
      classifiers=[
          'Development Status :: 4 - Beta',
          'License :: OSI Approved :: BSD License',
          'Operating System :: MacOS :: MacOS X',
          'Operating System :: POSIX :: Linux',
          'Operating System :: POSIX :: BSD :: FreeBSD',
          'Operating System :: POSIX :: BSD :: OpenBSD',
          'Operating System :: Microsoft :: Windows',
          'Topic :: System :: Monitoring',
          'Topic :: System :: Networking :: Monitoring',
          'Topic :: System :: Systems Administration'
      ])
