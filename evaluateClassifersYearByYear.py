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




class EvaluateClassifiersByDate():

    def __init__(self):

        print "get text 1"

        self.textsListApprentissage = self.getTextsList('corpus_deft/deft_2011/appr/deft2011_diachronie_appr_300.xml')

        print "get text 2"

        self.textsListTest = self.getTextsList('corpus_deft/deft_2011/test/deft2011_diachronie_save_300.xml')

        self.textsList = self.textsListApprentissage + self.textsListTest

        print "get motifOccur"

        self.motifsOccurences = cPickle.Unpickler(open('motifsOccurenceDelfiPypy_trainOnly_3-7.pkl', 'rb')).load()



    def run(self):

        print "vector transform"



        self.Y = self.getClassesTextes(self.textsListApprentissage)

        self.vectorizer = TfidfVectorizer(min_df=1, decode_error="ignore",lowercase=False)

        self.X = self.vectorizer.fit_transform(self.motifsOccurences)

        self.classifier = OneVsRestClassifier(SVC(random_state=0))


        models = {'SVC_lineaire': OneVsRestClassifier(LinearSVC(random_state=0)),
                  'MultinomialNB': OneVsRestClassifier(MultinomialNB()),
                  'BernoulliNB': OneVsRestClassifier(BernoulliNB())
                  }


        params = {'SVC_lineaire': {'estimator__C': [0.1, 0.5, 1, 1.5, 2, 5]},

                'MultinomialNB': {'estimator__alpha': (0.1, 0.5, 1.0, 2.5),
                                  'estimator__fit_prior': (True, False)},


                'BernoulliNB': {'estimator__alpha': (0.1, 0.5, 1.0, 2.5),
                                'estimator__fit_prior': (True, False)}

        }


        print "fitting"

        cv = ShuffleSplit(n_splits=3, test_size=0.3, random_state=42)
        gaussianDistanceScorer = make_scorer(Metrics().gaussianDistance)
        gs = GridMultipleClasifiers(models, params)
        gs.fit(self.X, self.Y,cv=cv, scoring=gaussianDistanceScorer, n_jobs=1)
        gs.score_summary()
        gs.showResults()
        gs.showBest()
        #self.classifier.fit(self.apprentissageX, self.apprentissageY)




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
        return int(year[0:4])

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



if __name__ == "__main__":
    dataB = EvaluateClassifiersByDate()
    dataB.run()