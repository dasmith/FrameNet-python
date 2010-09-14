#!/bin/env python
import framenet


print "Testing framenet import"
fn = framenet.FrameNet()

print "Printing fn's methods"

print dir(fn)

buy = fn.lookupLexicalUnit('buy','v')
print buy 
