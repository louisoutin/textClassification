#!/usr/bin/env python
# -*- coding: utf-8 -*-

import xml.etree.ElementTree as ET
from textTypes.textDelfi import *


class ClassifierUtils():


    """
    Retourne la liste des textes d'un dossier 'folder' passé en argument
    """
    def getTextsList(self, xmlFile):
        textsList = []
        tree = ET.parse(xmlFile)
        root = tree.getroot()
        for portion in root.iter('portion'):
            date = portion.find('meta').find('date').attrib['annee']
            body = portion.find('texte').text
            textsList.append(TextDelfi(date, body))
        return textsList


    """
    Retourne la classe d'une annee 'year' passé en argument
    """
    def getClasse(self, year):
        return int(year[1:3])


    """
    Retourne la liste des classes des textes contenus dans self.textsList
    """


    def getClassesTextes(self, textsList):
        listeClasses = []
        for texte in textsList:
            listeClasses.append(self.getClasse(texte.date))
        return listeClasses
