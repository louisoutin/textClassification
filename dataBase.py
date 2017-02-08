#!/usr/bin/env python
# -*- coding: utf-8 -*-
from text import *
import os
from extracteur.extracteur_motifs import *
from sklearn import svm
from sklearn.multiclass import OneVsRestClassifier
from sklearn.model_selection import train_test_split
from sklearn.svm import LinearSVC

class DataBase():

    def __init__(self, folder):
        self.textsList = self.getTextsList(folder)

        self.motifsOccurences = get_motifs(self.textsList,
                                           { 'minsup':1,
                                             'maxsup':10,
                                             'minlen':3,
                                             'maxlen':6})
        self.vecteursTraits = self.getVecteursTraits()
        self.classesTextes = self.getClassesTextes()

        self.apprentissageX, self.testX, self.apprentissageY, self.testY = train_test_split(self.vecteursTraits, self.classesTextes, test_size=0.1, random_state=42)
        #self.testX, self.testY = [], []
        #self.separationEnsembles(0.1)
        #self.clf = svm.SVC()
        #self.clf.fit(self.apprentissageX, self.apprentissageY)
        self.classifier = OneVsRestClassifier(LinearSVC(random_state=0))
        self.classifier.fit(self.apprentissageX, self.apprentissageY)


    """
    Retourne la liste des textes d'un dossier 'folder' passé en argument
    """
    def getTextsList(self,folder):
        textsList = []
        for dirname, dirnames, filenames in os.walk(folder):

            # print path to all filenames.
            for filename in filenames:
                text = Text(os.path.join(dirname, filename))
                #print(os.path.join(dirname, filename))
                textsList.append(text)
        return textsList

    """
    Retourne la classe d'une annee 'year' passé en argument
    """
    def getClasse(self, year):
        if year[:3] == "197":
            return 0
        if year[:3] == "198":
            return 1
        if year[:3] == "199":
            return 2
        if year[:3] == "200":
            return 3
        if year[:3] == "201":
            return 4

    """
    Retourne le Vecteur X, pour chaque texte, son nombre d'occurence de chacun des motifs extraits
    """
    def getVecteursTraits(self):
        dico = self.motifsOccurences
        listeVecteurs = []
        for numTexte in range(len(self.textsList)):
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
    def getClassesTextes(self):
        listeClasses = []
        for texte in self.textsList:
            listeClasses.append(self.getClasse(texte.date))
        return listeClasses



    def separationEnsembles(self, pourcentage):
        cp = {}
        cp[0] = round(self.classesTextes.count(0)*pourcentage)
        cp[1] = round(self.classesTextes.count(1)*pourcentage)
        cp[2] = round(self.classesTextes.count(2)*pourcentage)
        cp[3] = round(self.classesTextes.count(3)*pourcentage)
        cp[4] = round(self.classesTextes.count(4)*pourcentage)
        for i in range(len(self.vecteursTraits)):
            if cp[self.classesTextes[i]]>0:
                self.testX.append(self.vecteursTraits[i])
                self.testY.append(self.classesTextes[i])
                cp[self.classesTextes[i]]-=1
            else:
                self.apprentissageX.append(self.vecteursTraits[i])
                self.apprentissageY.append(self.classesTextes[i])


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
        print dic

if __name__ == "__main__":
    dataB = DataBase("Corpus")
    #print dataB.textsList
    #print dataB.motifsOccurences
    #print len(dataB.textsList)
    print dataB.classifier
    liste = []
    for i in range(len(dataB.testX)):
        liste.append(dataB.classifier.predict([dataB.testX[i]])[0])
    print dataB.testY
    print liste

    dataB.eval_res(dataB.testY,liste)

    #print dataB.vecteursTraits
    #print dataB.predict("CorpusTest/1971_test7")
