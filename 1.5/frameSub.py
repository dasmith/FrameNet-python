#!/usr/bin/env python

#
# Generated Fri Apr 15 16:00:26 2011 by generateDS.py version 2.4c.
#

import sys

import ??? as supermod

etree_ = None
Verbose_import_ = False
(   XMLParser_import_none, XMLParser_import_lxml,
    XMLParser_import_elementtree
    ) = range(3)
XMLParser_import_library = None
try:
    # lxml
    from lxml import etree as etree_
    XMLParser_import_library = XMLParser_import_lxml
    if Verbose_import_:
        print("running with lxml.etree")
except ImportError:
    try:
        # cElementTree from Python 2.5+
        import xml.etree.cElementTree as etree_
        XMLParser_import_library = XMLParser_import_elementtree
        if Verbose_import_:
            print("running with cElementTree on Python 2.5+")
    except ImportError:
        try:
            # ElementTree from Python 2.5+
            import xml.etree.ElementTree as etree_
            XMLParser_import_library = XMLParser_import_elementtree
            if Verbose_import_:
                print("running with ElementTree on Python 2.5+")
        except ImportError:
            try:
                # normal cElementTree install
                import cElementTree as etree_
                XMLParser_import_library = XMLParser_import_elementtree
                if Verbose_import_:
                    print("running with cElementTree")
            except ImportError:
                try:
                    # normal ElementTree install
                    import elementtree.ElementTree as etree_
                    XMLParser_import_library = XMLParser_import_elementtree
                    if Verbose_import_:
                        print("running with ElementTree")
                except ImportError:
                    raise ImportError("Failed to import ElementTree from any known place")

def parsexml_(*args, **kwargs):
    if (XMLParser_import_library == XMLParser_import_lxml and
        'parser' not in kwargs):
        # Use the lxml ElementTree compatible parser so that, e.g.,
        #   we ignore comments.
        kwargs['parser'] = etree_.ETCompatXMLParser()
    doc = etree_.parse(*args, **kwargs)
    return doc

#
# Globals
#

ExternalEncoding = 'ascii'

#
# Data representation classes
#

class frameSub(supermod.frame):
    def __init__(self, cDate=None, cBy=None, ID=None, name=None, definition=None, semType=None, FE=None, FEcoreSet=None, frameRelation=None, lexUnit=None):
        super(frameSub, self).__init__(cDate, cBy, ID, name, definition, semType, FE, FEcoreSet, frameRelation, lexUnit, )
supermod.frame.subclass = frameSub
# end class frameSub


class FEcoreSetSub(supermod.FEcoreSet):
    def __init__(self, memberFE=None):
        super(FEcoreSetSub, self).__init__(memberFE, )
supermod.FEcoreSet.subclass = FEcoreSetSub
# end class FEcoreSetSub


class FETypeSub(supermod.FEType):
    def __init__(self, name=None, abbrev=None, fgColor=None, bgColor=None, cDate=None, coreType=None, cBy=None, ID=None, definition=None, semType=None, requiresFE=None, excludesFE=None):
        super(FETypeSub, self).__init__(name, abbrev, fgColor, bgColor, cDate, coreType, cBy, ID, definition, semType, requiresFE, excludesFE, )
supermod.FEType.subclass = FETypeSub
# end class FETypeSub


class internalFrameRelationFETypeSub(supermod.internalFrameRelationFEType):
    def __init__(self, ID=None, name=None, valueOf_=None):
        super(internalFrameRelationFETypeSub, self).__init__(ID, name, valueOf_, )
supermod.internalFrameRelationFEType.subclass = internalFrameRelationFETypeSub
# end class internalFrameRelationFETypeSub


class relatedFramesTypeSub(supermod.relatedFramesType):
    def __init__(self, type_=None, relatedFrame=None):
        super(relatedFramesTypeSub, self).__init__(type_, relatedFrame, )
supermod.relatedFramesType.subclass = relatedFramesTypeSub
# end class relatedFramesTypeSub


class frameLUTypeSub(supermod.frameLUType):
    def __init__(self, status=None, name=None, POS=None, cDate=None, incorporatedFE=None, cBy=None, lemmaID=None, ID=None, definition=None, sentenceCount=None, lexeme=None, semType=None):
        super(frameLUTypeSub, self).__init__(status, name, POS, cDate, incorporatedFE, cBy, lemmaID, ID, definition, sentenceCount, lexeme, semType, )
supermod.frameLUType.subclass = frameLUTypeSub
# end class frameLUTypeSub


class sentenceCountSub(supermod.sentenceCount):
    def __init__(self, total=None, annotated=None, valueOf_=None):
        super(sentenceCountSub, self).__init__(total, annotated, valueOf_, )
supermod.sentenceCount.subclass = sentenceCountSub
# end class sentenceCountSub


class lexemeTypeSub(supermod.lexemeType):
    def __init__(self, order=None, headword=None, breakBefore=None, name=None, POS=None, valueOf_=None):
        super(lexemeTypeSub, self).__init__(order, headword, breakBefore, name, POS, valueOf_, )
supermod.lexemeType.subclass = lexemeTypeSub
# end class lexemeTypeSub


class semTypeRefTypeSub(supermod.semTypeRefType):
    def __init__(self, ID=None, name=None, valueOf_=None):
        super(semTypeRefTypeSub, self).__init__(ID, name, valueOf_, )
supermod.semTypeRefType.subclass = semTypeRefTypeSub
# end class semTypeRefTypeSub



def get_root_tag(node):
    tag = supermod.Tag_pattern_.match(node.tag).groups()[-1]
    rootClass = None
    if hasattr(supermod, tag):
        rootClass = getattr(supermod, tag)
    return tag, rootClass


def parse(inFilename):
    doc = parsexml_(inFilename)
    rootNode = doc.getroot()
    rootTag, rootClass = get_root_tag(rootNode)
    if rootClass is None:
        rootTag = 'frame'
        rootClass = supermod.frame
    rootObj = rootClass.factory()
    rootObj.build(rootNode)
    # Enable Python to collect the space used by the DOM.
    doc = None
    sys.stdout.write('<?xml version="1.0" ?>\n')
    rootObj.export(sys.stdout, 0, name_=rootTag,
        namespacedef_='')
    doc = None
    return rootObj


def parseString(inString):
    from StringIO import StringIO
    doc = parsexml_(StringIO(inString))
    rootNode = doc.getroot()
    rootTag, rootClass = get_root_tag(rootNode)
    if rootClass is None:
        rootTag = 'frame'
        rootClass = supermod.frame
    rootObj = rootClass.factory()
    rootObj.build(rootNode)
    # Enable Python to collect the space used by the DOM.
    doc = None
    sys.stdout.write('<?xml version="1.0" ?>\n')
    rootObj.export(sys.stdout, 0, name_=rootTag,
        namespacedef_='')
    return rootObj


def parseLiteral(inFilename):
    doc = parsexml_(inFilename)
    rootNode = doc.getroot()
    rootTag, rootClass = get_root_tag(rootNode)
    if rootClass is None:
        rootTag = 'frame'
        rootClass = supermod.frame
    rootObj = rootClass.factory()
    rootObj.build(rootNode)
    # Enable Python to collect the space used by the DOM.
    doc = None
    sys.stdout.write('#from ??? import *\n\n')
    sys.stdout.write('import ??? as model_\n\n')
    sys.stdout.write('rootObj = model_.frame(\n')
    rootObj.exportLiteral(sys.stdout, 0, name_="frame")
    sys.stdout.write(')\n')
    return rootObj


USAGE_TEXT = """
Usage: python ???.py <infilename>
"""

def usage():
    print USAGE_TEXT
    sys.exit(1)


def main():
    args = sys.argv[1:]
    if len(args) != 1:
        usage()
    infilename = args[0]
    root = parse(infilename)


if __name__ == '__main__':
    #import pdb; pdb.set_trace()
    main()


