#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sklearn.naive_bayes import MultinomialNB, GaussianNB, BernoulliNB

from metrics.Metrics import *

from sklearn.multiclass import OneVsRestClassifier
import cPickle
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer, TfidfVectorizer
from ClassifierUtils import *
import os.path
import subprocess

class ClassifierByYears(ClassifierUtils):

    def __init__(self, apprentissage, test, bagOfWords=False, minlen=3, maxlen=7):

        print "get text 1"

        self.textsListApprentissage = self.getTextsList(apprentissage)

        print "get text 2"

        self.textsListTest = self.getTextsList(test)

        self.textsList = self.textsListApprentissage + self.textsListTest

        print "get motifOccur"

        savedFile = "extractedDatas/motifsOccurenceDelfiPypy_nbWords=" + apprentissage[-7:-4] + "_minlen=" + str(minlen) + "_maxlen=" + str(maxlen)

        if not bagOfWords:
            print "repeatly maximum strings extraction..."
            if os.path.isfile(savedFile):
                print ("Extracted datas file already exist, unpickling...")
                self.motifsOccurences = cPickle.Unpickler(open(savedFile, 'rb')).load()
            else:
                print ("Extracted datas file do not exist, computing it...")
                os.chdir("patternsOccurence_saver")
                subprocess.call(
                    ["pypy", "DelfiPatternsSaver.py", "../" + apprentissage, "../" + test, str(minlen), str(maxlen)])
                print ("Unpickling extracted datas file...")
                os.chdir("../")
                self.motifsOccurences = cPickle.Unpickler(open(savedFile, 'rb')).load()
        else:
            print "bag of word extraction..."
            self.motifsOccurences = [texte.body for texte in self.textsList]

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
        wellDetectedDecades = Metrics().decadesWellDetected(self.Ytest, prediction)

        print"moyenne : " + str(score)
        print"mediane : " + str(median)
        print"ecart-type : " + str(ecart_type)
        print"variance : " + str(variance)
        print "décennies bien prédites"+ str(wellDetectedDecades)


    """
    Retourne la classe d'une annee 'year' passé en argument
    """
    def getClasse(self, year):
        return int(year[0:4])





if __name__ == "__main__":
    dataB = ClassifierByYears('corpus_deft/deft_2011/appr/deft2011_diachronie_appr_500.xml', 'corpus_deft/deft_2011/test/deft2011_diachronie_save_500.xml', bagOfWords=False)
    dataB.run()