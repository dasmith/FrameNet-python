from distutils.core import setup, Extension
from distutils.unixccompiler import *
from distutils.sysconfig import *
import sys

setup(name='framenet',
	  version='1.3a',
	  packages=['framenet'],
	  ext_modules = [],
	  )
