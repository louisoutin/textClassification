#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET

from sklearn.metrics import make_scorer
from sklearn.naive_bayes import MultinomialNB, GaussianNB, BernoulliNB
from sklearn.pipeline import Pipeline
from sklearn.model_selection import ShuffleSplit

from GridMultipleClasifiers import GridMultipleClasifiers
from metrics.resultEvaluation import *
from metrics.Metrics import *

from extractors.bagOfPatternsExtractor import *
from sklearn.multiclass import OneVsRestClassifier
from sklearn.svm import *
import cPickle
from textTypes.textDelfi import *
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer, TfidfVectorizer
from scipy import sparse



class ClassifierTwoStrats():

    def __init__(self):

        print "get text 1"

        self.textsListApprentissage = self.getTextsList('corpus_deft/deft_2011/appr/deft2011_diachronie_appr_300.xml')

        print "get text 2"

        self.textsListTest = self.getTextsList('corpus_deft/deft_2011/test/deft2011_diachronie_save_300.xml')

        self.textsList = self.textsListApprentissage + self.textsListTest

        print "get motifOccur"

        #self.motifsOccurences= cPickle.Unpickler(open('extractedDatas/motifsOccurenceDelfiPypy_all_500_3-7.pkl', 'rb')).load()
        self.motifsOccurences = [texte.body for texte in self.textsList]

        self.motifsOccurencesApprentissage = self.motifsOccurences[:len(self.textsListApprentissage)]

        self.motifsOccurencesTest = self.motifsOccurences[len(self.textsListApprentissage):]



    def run(self):

        print "vector transform"



        self.Yapprentissage = self.getClassesTextes(self.textsListApprentissage)

        self.Ytest = self.getClassesTextes(self.textsListTest)

        self.vectorizer = TfidfVectorizer(min_df=1, decode_error="ignore",lowercase=False)

        self.Xapprentissage = self.vectorizer.fit_transform(self.motifsOccurencesApprentissage)

        self.Xtest = self.vectorizer.transform(self.motifsOccurencesTest)

        self.classifier = OneVsRestClassifier(MultinomialNB(alpha=0.1, fit_prior=False))
        self.secondaryClassifiersTrains = []



        print "fitting"

        print self.Xapprentissage, self.Yapprentissage
        self.classifier.fit(self.Xapprentissage,self.Yapprentissage)
        print "prediction : \n"
        prediction = self.classifier.predict(self.Xtest)

        self.save(prediction,'predictionFirstStrat_300_bagWord.pkl')

        self.classifiersThirtyYears = []
        for i in range(15):
            print str(i)+" over 15 ..."
            (X,Y) = self.getDecadeTextsFitting(i)
            self.classifiersThirtyYears.append((X,Y))

        print "saving"

        self.save(self.classifiersThirtyYears,'classifiersThirtyYears_300_baWord.pkl')

    def save(self, data, path):
        #np.save(output, data)
        cPickle.dump(data, open(path,'wb'))

    def getDecadeTextsFitting(self,N):
        vectorX = None
        vectorY = []
        for i  in range(1,len(self.textsListApprentissage)):
            if (self.textsListApprentissage[i].date[1:3] == str(80+N)) or (self.textsListApprentissage[i].date[1:3] == str(81+N)) or (self.textsListApprentissage[i].date[1:3] == str(79+N)):

                vectorY.append(int(self.textsListApprentissage[i].date))
                x = sparse.csr_matrix(self.Xapprentissage[i].toarray()[0])
                if vectorX == None:
                    vectorX= x
                else:
                    vectorX = sparse.vstack([vectorX,x])


        return (vectorX,vectorY)

    def meanPredictedClass(self,array,N):
        maxIndexs = sorted(range(len(array)), key=lambda x: array[x])[-N:]
        return int(np.mean(maxIndexs))


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
            listeClasses.append(self.getClasse(texte.date)-80)
        return listeClasses



    """
    Predit la classe d'un texte passé par son chemin en parametre 'path'
    """
    def predict(self):
        return self.clf.predict([vecteurX])



if __name__ == "__main__":
    dataB = ClassifierTwoStrats()
    dataB.run()