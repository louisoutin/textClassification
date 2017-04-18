#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET

from sklearn.metrics import make_scorer
from sklearn.naive_bayes import MultinomialNB, GaussianNB, BernoulliNB
from sklearn.pipeline import Pipeline
from sklearn.model_selection import ShuffleSplit

from GridMultipleClasifiers import GridMultipleClasifiers
from metrics.confMatrixPlots import plot_confusion_matrix
from metrics.resultEvaluation import *
from metrics.Metrics import *

from extractors.bagOfPatternsExtractor import *
from sklearn.multiclass import OneVsRestClassifier
from sklearn.svm import *
import cPickle
from textTypes.textDelfi import *
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer, TfidfVectorizer
from ClassifierUtils import *
import matplotlib.pyplot as plt


class ClassifierByYears(ClassifierUtils):

    def __init__(self):

        print "get text 1"

        self.textsListApprentissage = self.getTextsList('corpus_deft/deft_2011/appr/deft2011_diachronie_appr_300.xml')

        print "get text 2"

        self.textsListTest = self.getTextsList('corpus_deft/deft_2011/test/deft2011_diachronie_save_300.xml')

        self.textsList = self.textsListApprentissage + self.textsListTest

        print "get motifOccur"

        self.motifsOccurences= cPickle.Unpickler(open('extractedDatas/motifsOccurenceDelfiPypy_all_300_3-7.pkl', 'rb')).load()
        #self.motifsOccurences = [texte.body for texte in self.textsList]
        #print self.motifsOccurences[0]

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



        print "fitting"
        print self.Xapprentissage
        self.classifier.fit(self.Xapprentissage,self.Yapprentissage)
        print "prediction : \n"
        prediction = self.classifier.predict(self.Xtest)

        print self.Ytest
        print prediction
        prediction = np.array(prediction)
        score = Metrics().gaussianDistance(self.Ytest, prediction)
        median = Metrics().medianeGaussianDistance(self.Ytest, prediction)
        variance = Metrics().varianceGaussianDistance(self.Ytest, prediction)
        ecart_type = Metrics().ecartTypeGaussianDistance(self.Ytest, prediction)

        print"moyenne : " + str(score)
        print"mediane : " + str(median)
        print"ecart-type : " + str(ecart_type)
        print"variance : " + str(variance)



    """
    Retourne la classe d'une annee 'year' passé en argument
    """
    def getClasse(self, year):
        return int(year[0:4])





if __name__ == "__main__":
    dataB = ClassifierByYears()
    dataB.run()