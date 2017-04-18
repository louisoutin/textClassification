#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from textTypes.textChanson import *
import pickle
import xml.etree.ElementTree as ET
from extractors.basicPatternsExtractor import *



class BasicPatternsSaver():

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
                                             'minlen':2,
                                             'maxlen':7})

        print "save"
        print self.motifsOccurences
        self.save(self.motifsOccurences, savedFile)

    def save(self, data, path):
        output = open(path, 'wb')
        pickle.dump(data, output)

    """
        Retourne la liste des textes d'un dossier 'folder' passé en argument
    """
    def getTextsList(self, folder):
        if folder==None:
            return []
        textsList = []
        for dirname, dirnames, filenames in os.walk(folder):

            # print path to all filenames.
            for filename in filenames:
                text = TextChanson(os.path.join(dirname, filename))
                # print(os.path.join(dirname, filename))
                textsList.append(text)
        return textsList

if __name__=="__main__":
    BasicPatternsSaver("../Corpus", None, '../testMotifsOccurenceBasicPypy.pkl')