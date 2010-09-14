import os.path
import cPickle
import xml 
import xml.dom.minidom

from framenet import loadXMLAttributes, getNoneTextChildNodes

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