#!/usr/bin/env python

#
# Generated Fri Apr 15 16:01:00 2011 by generateDS.py version 2.4c.
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

class headerTypeSub(supermod.headerType):
    def __init__(self, corpus=None, frame=None):
        super(headerTypeSub, self).__init__(corpus, frame, )
supermod.headerType.subclass = headerTypeSub
# end class headerTypeSub


class frameSub(supermod.frame):
    def __init__(self, FE=None):
        super(frameSub, self).__init__(FE, )
supermod.frame.subclass = frameSub
# end class frameSub


class FESub(supermod.FE):
    def __init__(self, bgColor=None, abbrev=None, type_=None, name=None, fgColor=None, valueOf_=None):
        super(FESub, self).__init__(bgColor, abbrev, type_, name, fgColor, valueOf_, )
supermod.FE.subclass = FESub
# end class FESub


class corpDocTypeSub(supermod.corpDocType):
    def __init__(self, ID=None, name=None, document=None):
        super(corpDocTypeSub, self).__init__(ID, name, document, )
supermod.corpDocType.subclass = corpDocTypeSub
# end class corpDocTypeSub


class documentSub(supermod.document):
    def __init__(self, ID=None, description=None, valueOf_=None):
        super(documentSub, self).__init__(ID, description, valueOf_, )
supermod.document.subclass = documentSub
# end class documentSub


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
        rootTag = 'headerType'
        rootClass = supermod.headerType
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
        rootTag = 'headerType'
        rootClass = supermod.headerType
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
        rootTag = 'headerType'
        rootClass = supermod.headerType
    rootObj = rootClass.factory()
    rootObj.build(rootNode)
    # Enable Python to collect the space used by the DOM.
    doc = None
    sys.stdout.write('#from ??? import *\n\n')
    sys.stdout.write('import ??? as model_\n\n')
    sys.stdout.write('rootObj = model_.headerType(\n')
    rootObj.exportLiteral(sys.stdout, 0, name_="headerType")
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


