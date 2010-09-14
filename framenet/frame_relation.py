import os.path
import cPickle
import xml 
import xml.dom.minidom

from framenet import loadXMLAttributes, getNoneTextChildNodes

class FrameRelation(dict):
    """
    This class deals with frRelation.xml
    """

    def __init__(self):
        """
        Constructor, doesn't do much
        """

        dict.__init__(self)

        self['relation-types'] = {}


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
