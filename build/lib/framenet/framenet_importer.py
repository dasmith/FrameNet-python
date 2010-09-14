#----------------------------------------------------------------------------
# This module reads and loads framenet data
#----------------------------------------------------------------------------

import sys
import os
import os.path
import cPickle
import xml 
import xml.dom.minidom

FRAMENET_HOME = 'FRAMENET_HOME'
LU_DIR_ENV = 'luXML'
FRAME_DIR_ENV = 'frXML'
FRAME_FILE = 'frames.xml'
FRAME_RELATION_FILE = 'frRelation.xml'

PICKLED_FRAME_FILE = 'frames.pickled'
PICKLED_FRAME_RELATIONS_FILE = 'frRelation.pickled'
PICKLED_LU_FILE='lu.pickled'

#----------------------------------------------------------------------------
def loadXMLAttributes(d, attributes):
    """
    """
    for attr in attributes.keys():
        sattr = str(attr)
        val = attributes[attr].value
        try:
            sval = str(val)
            if sval.isdigit():
                d[sattr] = int(sval)
            else:
                d[sattr] = sval
        except:
            d[sattr] = val
    return d


def getNoneTextChildNodes(xmlNode):
    """
    """

    return filter(lambda x:x.nodeType != x.TEXT_NODE, xmlNode.childNodes)
                        
#----------------------------------------------------------------------------

class LexicalUnit(dict):
    """
    This class is for lexical unit
    """

    def __init__(self):
        """
        Initialise the lexical unit.
        """

        dict.__init__(self)

        self['ID'] = None
        self['name'] = None
        self['pos'] = None
        self['definition'] = None
        self['frame'] = None
        self['incorporatedFE'] = None

        self['subcorpora'] = {}

        self['annotationSets'] = {}

        self['layers'] = {}

        pass


    def loadXML(self, fileName):
        """
        Load an xml file.
        """
        try:
            doc = xml.dom.minidom.parse(fileName)
        except:
            print >> sys.stderr, 'Unable to parse the xml document:', fileName
            return False

        # Load the main attributes of the lexunit-annotation nodes
        self.loadMainAttributes(doc.childNodes[1])

        # Then filter out all the useless text nodes
        goodNodes =  filter(lambda x:x.nodeType != x.TEXT_NODE, doc.childNodes[1].childNodes)

        for node in goodNodes:
            if node.nodeName == 'definition':
                if not self.loadDefinition(goodNodes[0]):
                    print >> sys.stderr, 'Failed to load the definition node for document:', fileName
                    return False
            elif node.nodeName == 'subcorpus':
                if not self.loadSubcorpus(node):
                    print >> sys.stderr, 'Failed to load the subcorpus No.' + str(i)
                    return False
        return True


    def loadMainAttributes(self, doc):
        """
        Loads the ID, name, frame, POS and incorporateFE attributes of the main document node
        """

        # Load the ID
        if doc.attributes.has_key('ID'):
            self['ID'] = int(doc.attributes['ID'].value)
        else:
            print >> sys.stderr, 'Unable to load the ID node'
            return False

        # Load the HeadWord
        if doc.attributes.has_key('name'):
            n = doc.attributes['name'].value
            self['name'] = str(n)
        else:
            print >> sys.stderr, 'Unable to load the name'
            return False

        # Load the POS
        if doc.attributes.has_key('pos'):
            self['pos'] = str(doc.attributes['pos'].value)
        else:
            print >> sys.stderr, 'Unable to load the POS'
            return False

        # Load the frame
        if doc.attributes.has_key('frame'):
            self['frame'] = str(doc.attributes['frame'].value)
        else:
            print >> sys.stderr, 'Unable to load the frame'
            return False

        # Load the incorporatedFE
        if doc.attributes.has_key('incorporatedFE'):
            self['incorporatedFE'] = str(doc.attributes['incorporatedFE'].value)
        else:
            print >> sys.stderr, 'Unable to load the incorporatedFE'
            return False

        return True
        

    def loadDefinition(self, defNode):
        """
        Loads the definition node
        """
        if len(defNode.childNodes) > 0:
            try:
                self['definition'] = defNode.childNodes[0].nodeValue
            except:
                print >> sys.stderr, 'Unable to load the definition node of:', defNode
                return False
        return True


    def loadSubcorpus(self, subCorpusNode):
        """
        Loads the subcorpus node
        """

        try:
            corpusName = str(subCorpusNode.attributes['name'].value)
        except:
            print >> sys.stderr, 'Unable to load the name of the subcorpus node', 
            return False

        self['subcorpora'][corpusName] = {}

        annotationNodes = filter(lambda x:x.nodeType != x.TEXT_NODE, subCorpusNode.childNodes)

        for annoNode in annotationNodes:
            if not self.loadAnnotationSet(annoNode, corpusName):
                print >> sys.stderr, 'Unable to load an annotation set'
                return False
        return True


    def loadAnnotationSet(self, annoNode, corpusName):
        """
        Loads annotation set.
        """
        annotation = {}
        try:
            annotation['ID'] = int(annoNode.attributes['ID'].value)
        except:
            print >> sys.stderr, 'Unable to read the annoNode id'
            return False

        try:
            annotation['status'] = str(annoNode.attributes['status'].value)
        except:
            print >> sys.stderr, 'Unable to read the annoNode status'
            return False

        goodNodes = filter(lambda x:x.nodeType != x.TEXT_NODE, annoNode.childNodes)

        for node in goodNodes:
            if node.nodeName == 'layers':
                if annotation.has_key('layers'):
                    print >> sys.stderr, 'Already has a Layers key!'
                    return False
                elif not self.loadLayers(node, annotation):
                    return False
            elif node.nodeName == 'sentence':
                if annotation.has_key('sentence'):
                    print >> sys.stderr, 'Already has a sentences key!'
                    return False
                elif not self.loadSentence(node, annotation):
                    return False

        self['annotationSets'][annotation['ID']] = annotation
        return True


    def loadLayers(self, layersNode, annotation):
        """
        Loads the layers <layers>
        """

        layers = filter(lambda x:x.nodeType != x.TEXT_NODE, layersNode.childNodes)

        singleLayers = {}

        for layer in layers:
            loaded = self.loadSingleLayer(layer)

            if loaded == None:
                print >> sys.stderr, 'Unable to load a layer!'
                return False
            singleLayers[loaded['ID']] = loaded

        annotation['layers'] = singleLayers

        return True


    def loadSentence(self, sentNode, annotation):
        """
        Loads the sentence
        """
        goodNodes = filter(lambda x:x.nodeType != x.TEXT_NODE, sentNode.childNodes)

        if len(goodNodes) != 1:
            print >> sys.stderr, 'Sent node has:', len(goodNodes), 'good nodes'
            return False

        sent = {}
        try:
            sent = loadXMLAttributes(sent, sentNode.attributes)
        except:
            print >> sys.stderr, 'Uanble to get one of ID or aPos'
            return False
        
        sent['text'] = goodNodes[0].childNodes[0].nodeValue

        if not isinstance(sent['text'], unicode):
            print >> sys.stderr, 'Unable to get the sentence text from', goodNodes[0].childNodes[0]
            return False

        try:
            sent['text'] = str(sent['text'])
        except:
            pass

        annotation['sentence'] = sent

        return True


    def loadSingleLayer(self, layerNode):
        """
        Loads a single layer, <layer>
        """

        layer = {'labels':{}}
        try:
            layer['ID'] = int(layerNode.attributes['ID'].value)
            layer['name'] = str(layerNode.attributes['name'].value)
        except:
            print >> sys.stderr, 'Unable to load layer id or name'
            return None

        labelsNode = filter(lambda x:x.nodeType != x.TEXT_NODE, layerNode.childNodes)

        if len(labelsNode) > 1:
            print >> sys.stderr, 'Got more than one labels node for a layer'
            print >> sys.stderr, labelsNode
            return None

        if len(labelsNode) > 0:
            labels = filter(lambda x:x.nodeType != x.TEXT_NODE, labelsNode[0].childNodes)

            for l in labels:
                ll = {}

                ll = loadXMLAttributes(ll, l.attributes)
                        
                layer['labels'][ll['ID']] = ll

        self['layers'][layer['ID']] = layer
        return layer

#----------------------------------------------------------------------------

class Frame(dict):
    """
    The frame class
    """

    def __init__(self):
        """
        Constructor, doesn't do much.
        """
        dict.__init__(self)

        self['definition'] = None
        self['fes'] = {}
        self['lexunits'] = {}
        self['semtypes'] = None

        pass


    def loadXMLNode(self, frameNode):
        """
        """
        loadXMLAttributes(self, frameNode.attributes)
        goodNodes = getNoneTextChildNodes(frameNode)

        for node in goodNodes:
            if node.nodeName == 'definition':
                if not self.loadFrameDefinition(node):
                    print >> sys.stderr, 'Unable to read definition node for frame:', self['ID']
            elif node.nodeName == 'fes':
                if not self.loadFrameFes(node):
                    print >> sys.stderr, 'Unable to read a fes node for frame:', self['ID']
            elif node.nodeName == 'lexunits':
                if not self.loadFrameLexunits(node):
                    print >> sys.stderr, 'Unable to read a lexunits node for frame:', self['ID']
            elif node.nodeName == 'semTypes':
                if not self.loadFrameSemtypes(node):
                    print >> sys.stderr, 'Unable to read a semtypes node for frame:', self['ID']
            else:
                print >> sys.stderr, 'Have no idea how to deal with node type:', node.nodeName
                return False
        return True


    def loadFrameDefinition(self, node):
        """
        """
        if len(node.childNodes) == 0:
            return True

        try:
            self['definition'] = node.childNodes[0].nodeValue
        except:
            print >> sys.stderr, 'There is no definition!'
            return False

        return True


    def loadFrameFes(self, node):
        """
        """
        feNodes = getNoneTextChildNodes(node)

        fes = {}

        for feNode in feNodes:
            fe = self.loadFrameFe(feNode)

            if fe == None:
                print >> sys.stderr, 'Got a bad fe'
                return False

            fes[fe['ID']] = fe

        return True


    def loadFrameFe(self, feNode):
        """
        """
        goodNodes = getNoneTextChildNodes(feNode)

        fe = {}
        fe = loadXMLAttributes(fe, feNode.attributes)
        fe['semtypes'] = {}

        for gn in goodNodes:
            if gn.nodeName == 'definition':
                if not fe.has_key('definition'):
                    try:
                        fe['definition'] = gn.childNodes[0].nodeValue
                    except:
                        fe['definition'] = None
                else:
                    print >> sys.stderr, 'Error , fe already have a definition:', fe['definition']
                    return None
            elif gn.nodeName == 'semTypes':
                goodSemTypeNodes = getNoneTextChildNodes(gn)

                for gsn in goodSemTypeNodes:
                    semType = {}
                    loadXMLAttributes(semType, gsn.attributes)
                    fe['semtypes'][semType['ID']] = semType
            else:
                print >> sys.stderr, 'In loadFrameFe, found this node:', gn.nodeName
                return None

        return fe


    def loadFrameLexunits(self, node):
        """
        """
        goodNodes = getNoneTextChildNodes(node)

        i = 0
        for gn in goodNodes:
            lu = self.loadFrameLexicalUnit(gn)

            if lu == None:
                print >> sys.stderr, 'The lu No.' + str(i), 'is bad'
                return False
            i += 1

            self['lexunits'][lu['ID']] = lu

        return True


    def loadFrameLexicalUnit(self, lexunitNode):
        """
        """

        lexunit = {}

        loadXMLAttributes(lexunit, lexunitNode.attributes)

        goodNodes = getNoneTextChildNodes(lexunitNode)

        for gn in goodNodes:
            if gn.nodeName == 'definition':
                try:
                    lexunit['definition'] = gn.childNodes[0].nodeValue
                except:
                    lexunit['definition'] = None
            elif gn.nodeName == 'annotation':
                annoNodes = getNoneTextChildNodes(gn)
                anno = {}
                for an in annoNodes:
                    try:
                        anno[str(an.nodeName)] = an.childNodes[0].nodeValue
                        try:
                            n = int(anno[str(an.nodeName)])
                            anno[str(an.nodeName)] = n
                        except:
                            pass
                    except:
                        anno[str(an.nodeName)] = None
                        print >> sys.stderr, 'Warning!! unable to retrieve', an.nodeName, 'for annotation'
                lexunit['annotation'] = anno
            elif gn.nodeName == 'lexemes':
                goodSemTypeNodes = getNoneTextChildNodes(gn)
                lexemes = {}
                for gsn in goodSemTypeNodes:
                    lexeme = {}
                    loadXMLAttributes(lexeme, gsn.attributes)
                    lexemes[lexeme['ID']] = lexeme
                lexunit['lexeme'] = lexemes
            elif gn.nodeName == 'semTypes':
                goodSemTypeNodes = getNoneTextChildNodes(gn)
                semTypes = {}
                for gsn in goodSemTypeNodes:
                    semType = {}
                    loadXMLAttributes(semType, gsn.attributes)
                    semTypes[semType['ID']] = semType
                lexunit['semtypes'] = semTypes
            else:
                print >> sys.stderr, 'Error, encounted the node:', gn.nodeName, 'in', lexunitNode.nodeName, 'lexunit'
                return None
        return lexunit


    def loadFrameSemtypes(self, node):
        """
        """
                    
        goodSemTypeNodes = getNoneTextChildNodes(node)

        semTypes = {}
        for gsn in goodSemTypeNodes:
            semType = {}
            loadXMLAttributes(semType, gsn.attributes)
            semTypes[semType['ID']] = semType

        self['semtypes'] = semTypes

        return True

#----------------------------------------------------------------------------

class FrRelation(dict):
    """
    This class deals with frRelation.xml
    """

    def __init__(self):
        """
        Constructor, doesn't do much
        """

        dict.__init__(self)

        self['relation-types'] = {}

        pass


    def loadXML(self, fileName):
        """
        """

        doc = xml.dom.minidom.parse(fileName)

        relationTypeNodes = getNoneTextChildNodes(doc.childNodes[1]) #the actual frame-relation-type nodes

        for rtn in relationTypeNodes:
            rt = {} #dictionary for frame-relation-type
            loadXMLAttributes(rt, rtn.attributes)
            relationNodes = getNoneTextChildNodes(rtn) #the actual frame-relationS nodes
            if len(relationNodes) != 1:
                print >> sys.stderr, 'Got more than one frame-relations node in type:', rt['name']
                return False
            singleRelationNodes = getNoneTextChildNodes(relationNodes[0]) # the actual frame-relation nodes

            singleRelations = {}
            i = 0
            for srn in singleRelationNodes:
                tmp = self.loadSingleRelation(srn)
                if tmp == None:
                    print >> sys.stderr, 'Unable to load relation No.' + str(i), 'for type', rt['name']
                    return False
                singleRelations[tmp['ID']] = tmp

            rt['frame-relations'] = singleRelations
            self['relation-types'][rt['ID']] = rt

        return True


    def loadSingleRelation(self, relationNode):
        """
        """

        frRelation = {}

        loadXMLAttributes(frRelation, relationNode.attributes)

        feNodes = getNoneTextChildNodes(relationNode)
        for fn in feNodes:
            tmp = {}
            loadXMLAttributes(tmp, fn.attributes)
            frRelation[tmp['ID']] = tmp

        return frRelation

#----------------------------------------------------------------------------

class FrameNet(dict):
    """
    This the master class for FrameNet
    """

    def __init__(self):
        """
        Constructor, loads the frames and the frame relations.
        """
        pickledFramePath = os.environ[FRAMENET_HOME] + '/' + PICKLED_FRAME_FILE
        pickledFrRelationPath = os.environ[FRAMENET_HOME] + '/' + PICKLED_FRAME_RELATIONS_FILE
        pickledLUPath = os.environ[FRAMENET_HOME] + '/' + PICKLED_LU_FILE
            
        try:
            print >> sys.stderr, 'Loading the frames ...',
            frames = cPickle.load(open(pickledFramePath))
            self['frames'] = frames
            print >> sys.stderr, 'done'
            
            print >> sys.stderr, 'Loading the frame relations ...',
            frRelations = cPickle.load(open(pickledFrRelationPath))
            self['frameRelations'] = frRelations
            print >> sys.stderr, 'done'

            print >> sys.stderr, 'Loading the lexical units data ...',
            luData = cPickle.load(open(pickledLUPath))
            print >> sys.stderr, 'done'
            self['luIndex'] = luData
            
        except:
            print >> sys.stderr, 'Framenet not initialized, doing it now'
            self.initialize()
            print >> sys.stderr, 'Loading the frames ...',
            frames = cPickle.load(open(pickledFramePath))
            self['frames'] = frames
            print >> sys.stderr, 'done'
            
            print >> sys.stderr, 'Loading the frame relations ...',
            frRelations = cPickle.load(open(pickledFrRelationPath))
            self['frameRelations'] = frRelations
            print >> sys.stderr, 'done'
            
            print >> sys.stderr, 'Loading the lexical units data ...',
            luData = cPickle.load(open(pickledLUPath))
            print >> sys.stderr, 'done'
            self['luIndex'] = luData

        self['luCache'] = {}
        self._generateFrameIndex()
        pass


    def _generatePickledFrames(self):
        """
        Initialises all the frames
        """

        framePath = os.environ[FRAMENET_HOME] + '/' + FRAME_DIR_ENV + '/' + FRAME_FILE
        pickledFramePath = os.environ[FRAMENET_HOME] + '/' + PICKLED_FRAME_FILE

        print >> sys.stderr, 'Loading xml for frames ...',
        doc = xml.dom.minidom.parse(framePath)
        frameNodes = getNoneTextChildNodes(doc.childNodes[1])
        print >> sys.stderr, 'done',
        
        frames = {}
        print >> sys.stderr, 'parsing each frame ...',
        for fn in frameNodes:
            f = Frame()
            f.loadXMLNode(fn)
            frames[f['ID']] = f
        print >> sys.stderr, 'done',

        print >> sys.stderr, 'saving the frames ...',
        cPickle.dump(frames, open(pickledFramePath, 'w'), cPickle.HIGHEST_PROTOCOL)
        print >> sys.stderr, 'done'

        pass

    def _generatePickledFrameRelations(self):
        """
        Initialises all the frames
        """

        frRelationPath = os.environ[FRAMENET_HOME] + '/' + FRAME_DIR_ENV + '/' + FRAME_RELATION_FILE
        pickledFrRelationPath = os.environ[FRAMENET_HOME] + '/' + PICKLED_FRAME_RELATIONS_FILE

        print >> sys.stderr, 'Loading xml for frame relations ...',
        frRelations = FrRelation()
        frRelations.loadXML(frRelationPath)
        print >> sys.stderr, 'done',
        
        print >> sys.stderr, 'saving the frame relationships ...',
        cPickle.dump(frRelations, open(pickledFrRelationPath, 'w'), cPickle.HIGHEST_PROTOCOL)
        print >> sys.stderr, 'done'

        pass


    def _generatePickledLexicalUnitsIndex(self):
        """
        Initialises all the frames
        """

        baseDir = os.environ[FRAMENET_HOME] + '/' + LU_DIR_ENV
        pickledLUPath = os.environ[FRAMENET_HOME] + '/' + PICKLED_LU_FILE

        lexicalUnitsIndexByName = {}
        for _f in os.listdir(baseDir):
            if _f.lower().startswith('lu') and _f.lower().endswith('.xml'):
                print >> sys.stderr, 'Loading:', _f, '...',
                lu = LexicalUnit()
                lu.loadXML(baseDir + '/' + _f)
                print >> sys.stderr, 'done'

                if lexicalUnitsIndexByName.has_key(lu['name']):
                    lexicalUnitsIndexByName[lu['name']][lu['ID']] = 1
                else:
                    lexicalUnitsIndexByName[lu['name']] = {lu['ID']:1}

        print >> sys.stderr, 'Saving the pickled lu files ...',
        cPickle.dump(lexicalUnitsIndexByName, open(pickledLUPath, 'w'), cPickle.HIGHEST_PROTOCOL)
        print >> sys.stderr, 'done'
        pass

    def _generateFrameIndex(self):
        """
        Generate an index from frame name to Frame objects
        """

        self['frameIndex'] = {}

        for _id in self['frames'].keys():
            f = self['frames'][_id]
            name = f['name']
            if self['frameIndex'].has_key(name):
                print >> sys.stderr, 'Error, multiple frame name:', name, 'found'
                sys.exit()

            self['frameIndex'][name] = f

        pass

    def initialize(self):
        """
        This function should be called only once before the whole thing can be used.
        """
        self._generatePickledFrames()
        self._generatePickledFrameRelations()
        self._generatePickledLexicalUnitsIndex()

        return True


    def lookupLexicalUnit(self, headWord, pos):
        """
        This function will look up a given word by its pos. The word must be already
        lemmatised and in lower case. The pos must also be in lower case and it can be
        one of the following:
        (1) v  -- for verb
        (2) n  -- for noun
        (3) a  -- for adjective
        (4) adv -- for adverb
        (5) prep -- for preposition
        (6) num -- for numbers
        (7) intj -- for interjections

        This function will return a dictionary of lexical units which match the (headWord, pos)
        pair. The keys to the dictionary will be the IDs of the lexical units, and the values of
        the dictionary will be LexicalUnit objects.
        """

        pickledLUPath = os.environ[FRAMENET_HOME] + '/' + LU_DIR_ENV

        w = headWord + '.' + pos

        if self['luCache'].has_key(w):
            return self['luCache'][w]
        
        if not self['luIndex'].has_key(w):
            return {}

        objects = {}
        for _id in self['luIndex'][w].keys():
            inputFile = pickledLUPath + '/lu' + str(_id) + '.xml'
            lu = LexicalUnit()
            lu.loadXML(inputFile)
            objects[lu['ID']] = lu

        self['luCache'][w] = objects
        return objects


    def lookupFrame(self, frame):
        """
        This function takes a string as input, the string should be the name
        of the Frame that you want to lookup, and its case sensitive. If not
        found, None will be returned.
        """

        if self['frameIndex'].has_key(frame):
            return self['frameIndex'][frame]

        return None

#----------------------------------------------------------------------------

def testLU(fileName):
    """
    """

    a = LexicalUnit()

    if False:
        if not a.loadXML(fileName):
            print >> sys.stderr, 'loading:', fileName, 'failed'
        print a
    else:
        try:
            if not a.loadXML(fileName):
                print >> sys.stderr, 'loading:', fileName, 'failed'
        except:
            print >> sys.stderr, 'loading:', fileName, 'failed'
    return a


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
