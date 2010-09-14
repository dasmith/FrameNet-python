#!/usr/bin/env python

""" FrameNet-Python is a library for reading and accessing FrameNet data. 
It was created by Patrick Ye and is maintained by Dustin Smith.

For more information, see:  http://github.com/dasmith/FrameNet-python

"""
VERSION = "1.3a"

import sys
import os
import os.path
import cPickle
import xml 
import xml.dom.minidom

FRAMENET_PATH = os.environ.get('FRAMENET_HOME')
                     
LU_DIR_ENV = 'luXML'
FRAME_DIR_ENV = 'frXML'
FRAME_FILE = 'frames.xml'
FRAME_RELATION_FILE = 'frRelation.xml'

PICKLED_FRAME_FILE = 'frames.pickled'
PICKLED_FRAME_RELATIONS_FILE = 'frRelation.pickled'
PICKLED_LU_FILE='lu.pickled'

def initialize():
    """
    """

    fn = FrameNet()
    fn.initialize()

    pass

#----------------------------------------------------------------------------

if __name__ == '__main__':
    #testLU(sys.argv[1])
    initialize()
