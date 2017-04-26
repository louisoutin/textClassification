#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sklearn.naive_bayes import MultinomialNB, GaussianNB, BernoulliNB

from metrics.confMatrixPlots import plot_confusion_matrix

from metrics.Metrics import *
from sklearn.multiclass import OneVsRestClassifier

import cPickle

from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer, TfidfVectorizer
from ClassifierUtils import *

from metrics.rocPlots import *
import os.path
import subprocess

class ClassifierByDecades(ClassifierUtils):

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
                subprocess.call(["pypy", "DelfiPatternsSaver.py", "../"+apprentissage, "../"+test, str(minlen), str(maxlen)])
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

        self.classifier = OneVsRestClassifier(MultinomialNB(alpha=0.1, fit_prior=False))



        print "fitting"

        self.classifier.fit(self.Xapprentissage,self.Yapprentissage)
        print "prediction : \n"
        prediction = self.classifier.predict(self.Xtest)
        score = Metrics().f1_scorer(self.Ytest,prediction)

        print score

        # Compute confusion matrix
        cnf_matrix = confusion_matrix(self.Ytest, prediction)
        np.set_printoptions(precision=2)

        class_names = [i for i in range(15)]

        # Plot non-normalized confusion matrix
        plt.figure()
        plot_confusion_matrix(cnf_matrix, classes=class_names,
                              title='Confusion matrix, without normalization')

        plt.show()

        print "prediction"
        print min(self.Ytest)
        ROCmultiple(self, self.Ytest, prediction)






if __name__ == "__main__":
    dataB = ClassifierByDecades('corpus_deft/deft_2011/appr/deft2011_diachronie_appr_300.xml', 'corpus_deft/deft_2011/test/deft2011_diachronie_save_300.xml')
    dataB.run()