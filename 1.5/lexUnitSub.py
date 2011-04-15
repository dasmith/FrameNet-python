#!/usr/bin/env python

#
# Generated Fri Apr 15 16:02:02 2011 by generateDS.py version 2.4c.
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

class lexUnitSub(supermod.lexUnit):
    def __init__(self, status=None, name=None, frame=None, POS=None, frameID=None, incorporatedFE=None, totalAnnotated=None, ID=None, header=None, definition=None, lexeme=None, semType=None, valences=None, subCorpus=None):
        super(lexUnitSub, self).__init__(status, name, frame, POS, frameID, incorporatedFE, totalAnnotated, ID, header, definition, lexeme, semType, valences, subCorpus, )
supermod.lexUnit.subclass = lexUnitSub
# end class lexUnitSub


class valencesTypeSub(supermod.valencesType):
    def __init__(self, governor=None, FERealization=None, FEGroupRealization=None):
        super(valencesTypeSub, self).__init__(governor, FERealization, FEGroupRealization, )
supermod.valencesType.subclass = valencesTypeSub
# end class valencesTypeSub


class subCorpusTypeSub(supermod.subCorpusType):
    def __init__(self, name=None, sentence=None):
        super(subCorpusTypeSub, self).__init__(name, sentence, )
supermod.subCorpusType.subclass = subCorpusTypeSub
# end class subCorpusTypeSub


class governorTypeSub(supermod.governorType):
    def __init__(self, lemma=None, type_=None, annoSet=None):
        super(governorTypeSub, self).__init__(lemma, type_, annoSet, )
supermod.governorType.subclass = governorTypeSub
# end class governorTypeSub


class FERealizationTypeSub(supermod.FERealizationType):
    def __init__(self, total=None, FE=None, pattern=None):
        super(FERealizationTypeSub, self).__init__(total, FE, pattern, )
supermod.FERealizationType.subclass = FERealizationTypeSub
# end class FERealizationTypeSub


class patternSub(supermod.pattern):
    def __init__(self, total=None, valenceUnit=None, annoSet=None):
        super(patternSub, self).__init__(total, valenceUnit, annoSet, )
supermod.pattern.subclass = patternSub
# end class patternSub


class FEGroupRealizationTypeSub(supermod.FEGroupRealizationType):
    def __init__(self, total=None, FE=None, pattern=None):
        super(FEGroupRealizationTypeSub, self).__init__(total, FE, pattern, )
supermod.FEGroupRealizationType.subclass = FEGroupRealizationTypeSub
# end class FEGroupRealizationTypeSub


class annoSetTypeSub(supermod.annoSetType):
    def __init__(self, ID=None, valueOf_=None):
        super(annoSetTypeSub, self).__init__(ID, valueOf_, )
supermod.annoSetType.subclass = annoSetTypeSub
# end class annoSetTypeSub


class FEValenceTypeSub(supermod.FEValenceType):
    def __init__(self, name=None, valueOf_=None):
        super(FEValenceTypeSub, self).__init__(name, valueOf_, )
supermod.FEValenceType.subclass = FEValenceTypeSub
# end class FEValenceTypeSub


class valenceUnitTypeSub(supermod.valenceUnitType):
    def __init__(self, GF=None, FE=None, PT=None, valueOf_=None):
        super(valenceUnitTypeSub, self).__init__(GF, FE, PT, valueOf_, )
supermod.valenceUnitType.subclass = valenceUnitTypeSub
# end class valenceUnitTypeSub


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


class sentenceTypeSub(supermod.sentenceType):
    def __init__(self, docID=None, sentNo=None, paragNo=None, aPos=None, corpID=None, ID=None, text=None, annotationSet=None):
        super(sentenceTypeSub, self).__init__(docID, sentNo, paragNo, aPos, corpID, ID, text, annotationSet, )
supermod.sentenceType.subclass = sentenceTypeSub
# end class sentenceTypeSub


class annotationSetTypeSub(supermod.annotationSetType):
    def __init__(self, status=None, cxnID=None, luID=None, frameID=None, cDate=None, frameName=None, luName=None, cxnName=None, ID=None, layer=None):
        super(annotationSetTypeSub, self).__init__(status, cxnID, luID, frameID, cDate, frameName, luName, cxnName, ID, layer, )
supermod.annotationSetType.subclass = annotationSetTypeSub
# end class annotationSetTypeSub


class layerTypeSub(supermod.layerType):
    def __init__(self, name=None, rank=None, label=None):
        super(layerTypeSub, self).__init__(name, rank, label, )
supermod.layerType.subclass = layerTypeSub
# end class layerTypeSub


class labelTypeSub(supermod.labelType):
    def __init__(self, itype=None, name=None, bgColor=None, feID=None, start=None, end=None, cBy=None, fgColor=None, valueOf_=None):
        super(labelTypeSub, self).__init__(itype, name, bgColor, feID, start, end, cBy, fgColor, valueOf_, )
supermod.labelType.subclass = labelTypeSub
# end class labelTypeSub



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
        rootTag = 'lexUnit'
        rootClass = supermod.lexUnit
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
        rootTag = 'lexUnit'
        rootClass = supermod.lexUnit
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
        rootTag = 'lexUnit'
        rootClass = supermod.lexUnit
    rootObj = rootClass.factory()
    rootObj.build(rootNode)
    # Enable Python to collect the space used by the DOM.
    doc = None
    sys.stdout.write('#from ??? import *\n\n')
    sys.stdout.write('import ??? as model_\n\n')
    sys.stdout.write('rootObj = model_.lexUnit(\n')
    rootObj.exportLiteral(sys.stdout, 0, name_="lexUnit")
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


