#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET


from extractorForBagOfWords import *
from sklearn.multiclass import OneVsRestClassifier
from sklearn.svm import LinearSVC
import pickle
from text.textDelfi import *
from sklearn.feature_extraction.text import CountVectorizer

class DataBaseDelfi():

    def __init__(self):

        print "get text 1"

        self.textsListApprentissage = self.getTextsList('corpus_deft/deft_2011/appr/deft2011_diachronie_appr_300.xml')

        print "get text 2"

        self.textsListTest = self.getTextsList('corpus_deft/deft_2011/test/deft2011_diachronie_save_300.xml')

        self.textsList = self.textsListApprentissage + self.textsListTest

        print "get motifOccur"

        self.motifsOccurences = pickle.load(open('motifsOccurenceDelfiPypy.pkl', 'rb'))

        print "vector transform"

        self.vectorizer = CountVectorizer(min_df=1, decode_error="ignore",lowercase=False)
        self.vecteursTraits = self.vectorizer.fit_transform(self.motifsOccurences)

        print "splitting"

        self.apprentissageX = self.vecteursTraits[:len(self.textsListApprentissage)]

        self.apprentissageY = self.getClassesTextes(self.textsListApprentissage)

        self.testX = self.vecteursTraits[len(self.textsListApprentissage):]

        self.testY = self.getClassesTextes(self.textsListTest)

        print "fitting"

        #self.testX, self.testY = [], []
        #self.separationEnsembles(0.1)
        #self.clf = svm.SVC()
        #self.clf.fit(self.apprentissageX, self.apprentissageY)
        self.classifier = OneVsRestClassifier(LinearSVC(random_state=0))
        self.classifier.fit(self.apprentissageX, self.apprentissageY)


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
    Retourne le Vecteur X, pour un seul texte (a ne pas utiliser car il faut calculer avec tous les textes)
    """
    def getVecteurTexte(self,texte):
        motifsTexte = get_motifs([texte],
                                           { 'minsup':1,
                                             'maxsup':10,
                                             'minlen':3,
                                             'maxlen':6})
        vecteurTexte = []
        dico = self.motifsOccurences
        for indexMotif in range(len(dico)):
            if dico[indexMotif][0] in [x[0] for x in motifsTexte]:
                for motif in motifsTexte:
                    if motif[0] == dico[indexMotif][0]:
                        vecteurTexte.append(motif[1][0])
            else:
                vecteurTexte.append(0)
        return vecteurTexte

    """
    Retourne la liste des classes des textes contenus dans self.textsList
    """
    def getClassesTextes(self,textsList):
        listeClasses = []
        for texte in textsList:
            listeClasses.append(self.getClasse(texte.date))
        return listeClasses



    """
    Predit la classe d'un texte passé par son chemin en parametre 'path'
    """
    def predict(self):
        return self.clf.predict([vecteurX])

    def eval_res(self, l1, l2):
        dic = {x: {"VP": 0, "FP": 0, "FN": 0} for x in set(l1)}
        for i in range(len(l1)):
            if l1[i] == l2[i]:
                dic[l1[i]]["VP"] += 1
            else:
                dic[l1[i]]["FN"] += 1
                dic[l2[i]]["FP"] += 1
        return dic

    def printEvalRes(self, dic):
        f_mesureMoyenne = 0
        cpt=0
        for i in dic:
            cpt+=1
            rappel = float(dic[i]["VP"])/(dic[i]["VP"]+dic[i]["FN"])
            precision = float(dic[i]["VP"]) / (dic[i]["VP"] + dic[i]["FP"])
            f_mesure = 2*((precision*rappel)/(precision+rappel))
            f_mesureMoyenne+=f_mesure
            print "Classe"+str(i)
            print "Rappel : "+str(rappel)+"      Precision : "+str(precision)+"      F-mesure : "+str(f_mesure)
        print "FMOYENNE : "+str(f_mesureMoyenne/cpt)

if __name__ == "__main__":
    dataB = DataBaseDelfi()
    #print dataB.motifsOccurences
    #print len(dataB.textsList)
    print dataB.classifier
    prediction = []
    arrayX = dataB.testX.toarray()
    for i in range(len(arrayX)):
        prediction.append(dataB.classifier.predict([arrayX[i]])[0])
    print dataB.testY
    print prediction

    cpt1=0
    cpt2=0
    for i in range(len(prediction)):
        if abs(dataB.testY[i]-prediction[i])<1:
            cpt2+=1
        cpt1+=1

    eval_res =dataB.eval_res(dataB.testY, prediction)
    print eval_res
    dataB.printEvalRes(eval_res)
    print "differences"
    print cpt1, cpt2
    #print dataB.vecteursTraits
    #print dataB.predict("CorpusTest/1971_test7")
