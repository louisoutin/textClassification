#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

sys.path.append('../textTypes')
sys.path.append('../extractors')

from textDelfi import *
import cPickle
import xml.etree.ElementTree as ET
from bagOfPatternsExtractor import *
import sys

class DelfiPatternsSaver():

    def __init__(self,apprentissageCorpus, testCorpus, minlen, maxlen):



        print"Lancement analyse textes ..."

        print "get liste apprentissage"
        self.textsListApprentissage = self.getTextsList(apprentissageCorpus)

        print "get liste teste"
        self.textsListTest = self.getTextsList(testCorpus)
        self.textsList = self.textsListApprentissage + self.textsListTest

        print "get motifs"

        self.motifsOccurences = get_motifs(self.textsList,
                                           { 'minsup':1,
                                             'maxsup':10,
                                             'minlen':minlen,
                                             'maxlen':maxlen})

        print "save"
        if testCorpus == None or testCorpus == "None":
            savedFile = "../extractedDatas/motifsOccurenceDelfiPypy_onlyTrain_nbWords="+apprentissageCorpus[-7:-4]+"_minlen="+str(minlen)+"_maxlen="+str(maxlen)
        else:
            savedFile = "../extractedDatas/motifsOccurenceDelfiPypy_nbWords="+apprentissageCorpus[-7:-4]+"_minlen="+str(minlen)+"_maxlen="+str(maxlen)
        self.save(self.motifsOccurences, savedFile)

    def save(self, data, path):
        #np.save(output, data)
        cPickle.dump(data, open(path,'wb'))

    """
    Retourne la liste des textes d'un dossier 'folder' passé en argument
    """
    def getTextsList(self,xmlFile):
        if xmlFile==None or xmlFile=="None":
            return []
        textsList = []
        tree = ET.parse(xmlFile)
        root = tree.getroot()
        for portion in root.iter('portion'):
            date = portion.find('meta').find('date').attrib['annee']
            body = portion.find('texte').text
            textsList.append(TextDelfi(date, body))
        return textsList

if __name__=="__main__":
    apprentissage = sys.argv[1]
    test = sys.argv[2]
    minlen = int(sys.argv[3])
    maxlen = int(sys.argv[4])

    DelfiPatternsSaver(apprentissage,test,minlen,maxlen)