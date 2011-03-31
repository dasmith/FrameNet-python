#!/usr/bin/env python

""" FrameNet-Python is a library for reading and accessing FrameNet data. 
It was created by Patrick Ye and is maintained by Dustin Smith. For more 
information, see:  http://github.com/dasmith/FrameNet-python

This Python library is covered under the MIT/Expat license.  FrameNet data
must be obtained separately and is subject to a different license:
http://framenet.icsi.berkeley.edu/
"""

VERSION = "1.3a"

import sys
import os
import os.path
import cPickle
import xml 
import xml.dom.minidom
                     
LU_DIR_ENV = 'luXML'
FRAME_DIR_ENV = 'frXML'
FRAME_FILE = 'frames.xml'
FRAME_RELATION_FILE = 'frRelation.xml'

PICKLED_FRAME_FILE = 'frames.pickled'
PICKLED_FRAME_RELATIONS_FILE = 'frRelation.pickled'
PICKLED_LU_FILE='lu.pickled'

pth = os.environ.get('FRAMENET_HOME')
if pth != None:
    FRAMENET_PATH = pth
else:
    # try the default
    FRAMENET_PATH = "/usr/share/framenet1.3"

print FRAMENET_PATH+"/"+FRAME_DIR_ENV+"/"+FRAME_FILE
if not (os.path.exists(FRAMENET_PATH+"/"+PICKLED_FRAME_FILE) or os.path.exists(FRAMENET_PATH+"/"+FRAME_DIR_ENV+"/"+FRAME_FILE)):
    raise Exception("Error, could not open data directory. Set environment variable, FRAMENET_HOME, to data path.")

def initialize():
    """ 
    """

    fn = FrameNet()
    fn.initialize()

#----------------------------------------------------------------------------

if __name__ == '__main__':
    initialize()
