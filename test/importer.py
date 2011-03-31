#!/bin/env python
from framenet import *


print "Testing framenet import"
fn = framenet.FrameNet()

print "Printing fn's methods"

print dir(fn)

buy = fn.lookupLexicalUnit('buy','v') 
print buy 

cb = fn.lookupFrame('Commerce_buy')

fg = fn.getFrameGraph('Commerce_buy')