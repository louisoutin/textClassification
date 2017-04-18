#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

sys.path.append('../textTypes')
sys.path.append('../extractors')

from textDelfi import *
import cPickle
import xml.etree.ElementTree as ET
from bagOfPatternsExtractor import *


class DelfiPatternsSaver():

    def __init__(self,apprentissageCorpus, testCorpus, savedFile):
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
                                             'minlen':3,
                                             'maxlen':7})

        print "save"

        self.save(self.motifsOccurences, savedFile)

    def save(self, data, path):
        #np.save(output, data)
        cPickle.dump(data, open(path,'wb'))

    """
    Retourne la liste des textes d'un dossier 'folder' passé en argument
    """
    def getTextsList(self,xmlFile):
        if xmlFile==None:
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
    DelfiPatternsSaver("../corpus_deft/deft_2011/appr/deft2011_diachronie_appr_500.xml", "../corpus_deft/deft_2011/test/deft2011_diachronie_save_500.xml", '../extractedDatas/motifsOccurenceDelfiPypy_all_500_3-7_from1.pkl')