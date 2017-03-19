#!/usr/bin/env python
# -*- coding: utf-8 -*-

from text.textDelfi import *
import pickle
import xml.etree.ElementTree as ET
from extractorForBagOfWords import *



class ExtracteurMotifs():

    def __init__(self):
        print"Lancement analyse textes ..."

        print "get liste apprentissage"
        self.textsListApprentissage = self.getTextsList("corpus_deft/deft_2011/appr/deft2011_diachronie_appr_300.xml")

        print "get liste teste"
        self.textsListTest = self.getTextsList('corpus_deft/deft_2011/test/deft2011_diachronie_save_300.xml')
        self.textsList = self.textsListApprentissage + self.textsListTest

        print "get motifs"

        self.motifsOccurences = get_motifs(self.textsList,
                                           { 'minsup':2,
                                             'maxsup':10,
                                             'minlen':3,
                                             'maxlen':6})

        print "save"

        self.save(self.motifsOccurences, 'motifsOccurenceDelfiPypy.pkl')

    def save(self, data, path):
        output = open(path, 'wb')
        pickle.dump(data, output)

    """
    Retourne la liste des textes d'un dossier 'folder' passé en argument
    """
    def getTextsList(self,xmlFile):
        textsList = []
        tree = ET.parse(xmlFile)
        root = tree.getroot()
        for portion in root.iter('portion'):
            date = portion.find('meta').find('date').attrib['annee']
            body = portion.find('texte').text
            textsList.append(TextDelfi(date, body))
        return textsList

if __name__=="__main__":
    ExtracteurMotifs()