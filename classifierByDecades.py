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
from metrics.rocPlots import *

class ClassifierByDecades(ClassifierUtils):

    def __init__(self):

        print "get text 1"

        self.textsListApprentissage = self.getTextsList('corpus_deft/deft_2011/appr/deft2011_diachronie_appr_500.xml')

        print "get text 2"

        self.textsListTest = self.getTextsList('corpus_deft/deft_2011/test/deft2011_diachronie_save_500.xml')

        self.textsList = self.textsListApprentissage + self.textsListTest

        print "get motifOccur"

        self.motifsOccurences= cPickle.Unpickler(open('extractedDatas/motifsOccurenceDelfiPypy_all_500_3-7.pkl', 'rb')).load()



        self.motifsOccurencesApprentissage = self.motifsOccurences[:len(self.textsListApprentissage)]

        self.motifsOccurencesTest = self.motifsOccurences[len(self.textsListApprentissage):]



    def run(self):

        print "vector transform"



        self.Yapprentissage = self.getClassesTextes(self.textsListApprentissage)

        self.Ytest = self.getClassesTextes(self.textsListTest)

        self.vectorizer = TfidfVectorizer(min_df=1, decode_error="ignore",lowercase=False)

        self.Xapprentissage = self.vectorizer.fit_transform(self.motifsOccurencesApprentissage)

        print self.Xapprentissage[0]

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

        # Plot normalized confusion matrix
        plt.figure()
        plot_confusion_matrix(cnf_matrix, classes=class_names, normalize=True,
                              title='Normalized confusion matrix')

        plt.show()

        print "prediction"
        print min(self.Ytest)
        ROCmultiple(self, self.Ytest, prediction)






if __name__ == "__main__":
    dataB = ClassifierByDecades()
    dataB.run()