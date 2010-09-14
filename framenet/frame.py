
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
        FrameNet.loadXMLAttributes(self, frameNode.attributes)
        goodNodes = FrameNet.getNoneTextChildNodes(frameNode)

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
        feNodes = FrameNet.getNoneTextChildNodes(node)

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
        goodNodes = FrameNet.getNoneTextChildNodes(feNode)

        fe = {}
        fe = FrameNet.loadXMLAttributes(fe, feNode.attributes)
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
                goodSemTypeNodes = FrameNet.getNoneTextChildNodes(gn)

                for gsn in goodSemTypeNodes:
                    semType = {}
                    FrameNet.loadXMLAttributes(semType, gsn.attributes)
                    fe['semtypes'][semType['ID']] = semType
            else:
                print >> sys.stderr, 'In loadFrameFe, found this node:', gn.nodeName
                return None

        return fe


    def loadFrameLexunits(self, node):
        """
        """
        goodNodes = FrameNet.getNoneTextChildNodes(node)

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

        FrameNet.loadXMLAttributes(lexunit, lexunitNode.attributes)

        goodNodes = FrameNet.getNoneTextChildNodes(lexunitNode)

        for gn in goodNodes:
            if gn.nodeName == 'definition':
                try:
                    lexunit['definition'] = gn.childNodes[0].nodeValue
                except:
                    lexunit['definition'] = None
            elif gn.nodeName == 'annotation':
                annoNodes = FrameNet.getNoneTextChildNodes(gn)
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
                goodSemTypeNodes = FrameNet.getNoneTextChildNodes(gn)
                lexemes = {}
                for gsn in goodSemTypeNodes:
                    lexeme = {}
                    FrameNet.loadXMLAttributes(lexeme, gsn.attributes)
                    lexemes[lexeme['ID']] = lexeme
                lexunit['lexeme'] = lexemes
            elif gn.nodeName == 'semTypes':
                goodSemTypeNodes = FrameNet.getNoneTextChildNodes(gn)
                semTypes = {}
                for gsn in goodSemTypeNodes:
                    semType = {}
                    FrameNet.loadXMLAttributes(semType, gsn.attributes)
                    semTypes[semType['ID']] = semType
                lexunit['semtypes'] = semTypes
            else:
                print >> sys.stderr, 'Error, encounted the node:', gn.nodeName, 'in', lexunitNode.nodeName, 'lexunit'
                return None
        return lexunit


    def loadFrameSemtypes(self, node):
        """
        """
                    
        goodSemTypeNodes = FrameNet.getNoneTextChildNodes(node)

        semTypes = {}
        for gsn in goodSemTypeNodes:
            semType = {}
            FrameNet.loadXMLAttributes(semType, gsn.attributes)
            semTypes[semType['ID']] = semType

        self['semtypes'] = semTypes

        return True

#----------------------------------------------------------------------------
