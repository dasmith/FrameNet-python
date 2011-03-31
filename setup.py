from distutils.core import setup, Extension
from distutils.unixccompiler import *
from distutils.sysconfig import *
import sys
import os

setup(name='framenet',
    version='1.3a',
    packages=['framenet'],
    ext_modules = [],
    )

#  The code below is for checking to see if the framenet data files
# exist.  It first looks for the files at the path defined
# by the environment variable FRAMENET_HOME.  If this is 
# undefined, it prompts the user to enter their own path
# or accept the default path, /usr/share/framenet1.3, to 
# search for the files.
#
# It will not install unless the files are available, since
# the library is useless without them.
#
# Finally, it asks the user to permanently add the FRAMENET_HOME
# variable to their default shell.  (What to do for Windows 
# machines?)

frameNetFiles = ['luXML','frXML','frXML/frames.xml', 'frXML/frRelation.xml']

frameNetPath = os.environ.get('FRAMENET_HOME')
if frameNetPath == None:
    frameNetPath = "/usr/share/framenet1.3"
    entry = raw_input("Please enter the directory where you store FrameNet\
 data [default=%s]: " % (frameNetPath))
    if entry.strip() != "":
        frameNetPath = entry.strip()
for fnFile in frameNetFiles:
    print "Checking for file %s/%s..." % (frameNetPath,fnFile),
    if os.path.exists("%s/%s" % (frameNetPath,fnFile)):
        print "OK!"
    else:
        print "FAILED"
        print "Please obtain FrameNet data and set your path properly."
        sys.exit(1)
    # set environmental variable
    os.putenv('FRAMENET_HOME',frameNetPath)

print "-"*100
print "Please add environment variable FRAMENET_HOME to your shell file. e.g."
print 'echo "FRAMENET_HOME=%s" >> ~/.bashrc ' % (frameNetPath)
print "-"*100

