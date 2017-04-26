#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
from ClassifierUtils import *
from sklearn.naive_bayes import MultinomialNB, GaussianNB, BernoulliNB
from sklearn.svm import LinearSVC

from metrics.Metrics import *

from extractors.bagOfPatternsExtractor import *
from sklearn.multiclass import OneVsRestClassifier

import cPickle
from textTypes.textDelfi import *
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer, TfidfVectorizer
from scipy import sparse
import os.path
import subprocess


class ClassifierTwoStratsPreliminary(ClassifierUtils):

    def __init__(self, apprentissage, test, bagOfWords=False, minlen=3, maxlen=7):

        self.bagOfWords= bagOfWords
        print "get text 1"

        self.textsListApprentissage = self.getTextsList(apprentissage)

        print "get text 2"

        self.textsListTest = self.getTextsList(test)

        self.textsList = self.textsListApprentissage + self.textsListTest

        self.nbWords = apprentissage[-7:-4]
        self.strMinMaxLen = (str(minlen),str(maxlen))

        print "get motifOccur"

        savedFile = "extractedDatas/motifsOccurenceDelfiPypy_nbWords=" + self.nbWords + "_minlen=" + str(minlen) + "_maxlen=" + str(maxlen)

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

        self.motifsOccurencesApprentissage = self.motifsOccurences[:len(self.textsListApprentissage)]

        self.motifsOccurencesTest = self.motifsOccurences[len(self.textsListApprentissage):]



    def run(self):

        print "vector transform"



        self.Yapprentissage = self.getClassesTextes(self.textsListApprentissage)

        self.Ytest = self.getClassesTextes(self.textsListTest)

        self.vectorizer = TfidfVectorizer(min_df=1, decode_error="ignore",lowercase=False)

        self.Xapprentissage = self.vectorizer.fit_transform(self.motifsOccurencesApprentissage)

        self.Xtest = self.vectorizer.transform(self.motifsOccurencesTest)

        if not self.bagOfWords:
            self.classifier = OneVsRestClassifier(MultinomialNB(alpha=0.1, fit_prior=False))
        else:
            self.classifier = OneVsRestClassifier(OneVsRestClassifier(LinearSVC(random_state=0, C=1.5)))
        self.secondaryClassifiersTrains = []



        print "fitting"

        self.classifier.fit(self.Xapprentissage,self.Yapprentissage)
        print "prediction : \n"
        prediction = self.classifier.predict(self.Xtest)

        if self.bagOfWords:
            self.save(prediction,'extractedDatas/predictionFirstStrat_nbWords='+self.nbWords+'_bagOfWord.pkl')
        else:
            self.save(prediction, 'extractedDatas/predictionFirstStrat_nbWords=' + self.nbWords + '_minlen='+self.strMinMaxLen[0]+'_maxlen='+self.strMinMaxLen[1]+'.pkl')

        self.classifiersThirtyYears = []
        for i in range(15):
            print str(i+1)+" over 15 ..."
            (X,Y) = self.getDecadeTextsFitting(i)
            self.classifiersThirtyYears.append((X,Y))

        print "saving"

        if self.bagOfWords:
            self.save(self.classifiersThirtyYears,'extractedDatas/classifiersThirtyYears_nbWords='+self.nbWords+'_bagOfWord.pkl')
        else:
            self.save(self.classifiersThirtyYears, 'extractedDatas/classifiersThirtyYears_nbWords=' + self.nbWords + '_minlen='+self.strMinMaxLen[0]+'_maxlen='+self.strMinMaxLen[1]+'.pkl')

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







if __name__ == "__main__":

    dataB = ClassifierTwoStratsPreliminary('corpus_deft/deft_2011/appr/deft2011_diachronie_appr_300.xml', 'corpus_deft/deft_2011/test/deft2011_diachronie_save_300.xml', bagOfWords=True)
    dataB.run()