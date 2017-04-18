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
from ClassifierUtils import *



class ClassifierByYears(ClassifierUtils):

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

        print "load prediction First Strat"

        self.decadePredictions = cPickle.Unpickler(
            open('predictionFirstStrat_300_bagWord.pkl', 'rb')).load()

        print "load classifiers 30 years alredy fitted"

        self.classifiersThirtyYearsTrainSet = cPickle.Unpickler(
            open('classifiersThirtyYears_300_baWord.pkl', 'rb')).load()

        self.classifiersThirtyYears = []



    def run(self):

        print "vector transform"


        self.Yapprentissage = self.getClassesTextes(self.textsListApprentissage)

        self.Ytest = self.getClassesTextes(self.textsListTest)

        self.vectorizer = TfidfVectorizer(min_df=1, decode_error="ignore",lowercase=False)

        self.Xapprentissage = self.vectorizer.fit_transform(self.motifsOccurencesApprentissage)

        self.Xtest = self.vectorizer.transform(self.motifsOccurencesTest)

        for (X,Y) in self.classifiersThirtyYearsTrainSet:
            print 1
            classifier = OneVsRestClassifier(MultinomialNB(alpha=0.1, fit_prior=False))
            classifier.fit(X,Y)
            self.classifiersThirtyYears.append(classifier)

        print "predict"

        predictionFinal = []
        for i in range(len(self.decadePredictions)):
            x = self.Xtest[i].toarray()[0]
            result = self.classifiersThirtyYears[self.decadePredictions[i]].predict(x.reshape(1,-1))
            predictionFinal.append(result[0])
        print self.Ytest
        print predictionFinal
        predictionFinal = np.array(predictionFinal)
        score = Metrics().gaussianDistance(self.Ytest,predictionFinal)
        median = Metrics().medianeGaussianDistance(self.Ytest, predictionFinal)
        variance = Metrics().varianceGaussianDistance(self.Ytest, predictionFinal)
        ecart_type = Metrics().ecartTypeGaussianDistance(self.Ytest, predictionFinal)

        print"moyenne : "+str(score)
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