#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import pickle
from extracteur.rstr_max.rstr_max import *
from text.textDelfi import *
from text.textChanson import *
import pickle
import xml.etree.ElementTree as ET

print"Lancement analyse textes ..."

class ExtracteurMotifs():

    def __init__(self):
        print "get liste apprentissage"
        self.textsListApprentissage = self.getTextsList("corpus_deft/deft_2011/appr/deft2011_diachronie_appr_300.xml")

        print "get liste teste"
        self.textsListTest = self.getTextsList('corpus_deft/deft_2011/test/deft2011_diachronie_save_300.xml')
        self.textsList = self.textsListApprentissage + self.textsListTest

        print "get motifs"

        self.motifsOccurences = self.get_motifs()

        print"get apprentissage X"

        self.apprentissageX = self.getVecteursTraits(self.textsListApprentissage)

        print"get test X"
        self.testX = self.getVecteursTraits(self.textsListTest)

        print"get apprentissa   ge Y"

        self.apprentissageY = self.getClassesTextes(self.textsListApprentissage)

        print"get test Y"
        self.testY = self.getClassesTextes(self.textsListTest)

        print "save"

        self.save(self.motifsOccurences,'motifsOccurenceDelfi.pkl')

        self.save((self.apprentissageX,self.apprentissageY), 'apprentissageData.pkl')

        self.save((self.testX, self.testY), 'testData.pkl')

    def save(self,data,path):
        output = open(path, 'wb')
        pickle.dump(data, output)


    def exploit_rstr(self,r, rstr, dic_occur, options):
        l_str = []
        cpt_ss = 0
        for (offset_end, nb), (l, start_plage) in r.iteritems():
            ss = rstr.global_suffix[offset_end-l:offset_end]
            if len(ss)<options['minlen'] or len(ss)>options['maxlen']:
                continue
            cpt_ss+=1
            set_occur = set()
            for o in xrange(start_plage, start_plage+nb) :
                id_str = rstr.idxString[rstr.res[o]]
                dic_occur[id_str][cpt_ss]=dic_occur[id_str].setdefault(cpt_ss,0)+1
                set_occur.add(id_str)
            if len(set_occur)>=options['minsup'] and len(set_occur)<=options['maxsup'] :
                occurences = {}
                for x in set_occur:
                    occurences[x] = dic_occur[x][cpt_ss]

                sortie = [ss, occurences]
                l_str.append(sortie)
        #print l_str
        return l_str

    def get_motifs(self,options = { 'minsup':2,
                                            'maxsup':5,
                                            'minlen':3,
                                            'maxlen':6}):
        rstr = Rstr_max()
        for ligne in self.textsList:
            rstr.add_str(ligne.body)
        dic_occur= {x:{} for x in xrange(0,len(self.textsList))}
        r=rstr.go()
        l_motifs = self.exploit_rstr(r, rstr, dic_occur, options)
        return l_motifs


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

    """
    Retourne la classe d'une annee 'year' passé en argument
    """
    def getClasse(self, year):
        return int(year[1:3])




    """
    Retourne le Vecteur X, pour chaque texte, son nombre d'occurence de chacun des motifs extraits
    """
    def getVecteursTraits(self,textsList):
        dico = self.motifsOccurences
        print "dico :"
        print len(dico)
        listeVecteurs = []
        for numTexte in range(len(textsList)):
            vecteurTexte = []
            for motif in range(len(dico)):
                if numTexte in dico[motif][1]:
                    vecteurTexte.append(dico[motif][1][numTexte])
                else:
                    vecteurTexte.append(0)
            listeVecteurs.append(vecteurTexte)
        return listeVecteurs

    """
    Retourne la liste des classes des textes contenus dans self.textsList
    """
    def getClassesTextes(self,textsList):
        listeClasses = []
        for texte in textsList:
            listeClasses.append(self.getClasse(texte.date))
        return listeClasses


ExtracteurMotifs()









# liste_motifs = get_motifs2(["HATTIVATTAATTI"])
# print 'liste motif :'
# print liste_motifs
# # get_motifs prend comme paramètre une liste de chaines et des options
# # chaque chaine étant une ligne généralement
# # on peut ajouter un dictionnaire d'options en donnant des valeurs de support (effectif) minimal et maximal (minsup et maxsup) de même pour la longueur en caractères du motif (minlen et maxlen)
# #Sinon, les valeurs par défaut sont utilisées: options = { 'minsup':2, 'maxsup':10, 'minlen':1, 'maxlen':10}
# # la fonction retourne une liste de paires : motif, liste de paires chaine (effectif)
# #chaine1 = open(sys.argv[1]).read()
# #chaine2 = open(sys.argv[2]).read()
# #liste_motifs = get_motifs([chaine1,chaine2])
# liste_motifs =[[len(x),x,y] for x,y in liste_motifs] # rajoute la longueur comme premiere elt de la sous liste
# print 'liste motif 2 :'
# print liste_motifs
# print sorted(liste_motifs) # tri en fonction de la taille du motif (A -> 1 ; ATTA -> 3 ...)
# for l,motif, positions in sorted(liste_motifs):
#     positions = [str((x,positions[x])) for x in positions]
#     print "%s\t\t trouvé dans les chaînes\t %s"%(motif,",".join(positions))
#
