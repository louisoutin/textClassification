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



class EvaluateClassifiersByDecade(ClassifierUtils):

    def __init__(self):

        print "get text 1"

        self.textsListApprentissage = self.getTextsList('corpus_deft/deft_2011/appr/deft2011_diachronie_appr_300.xml')

        print "get text 2"

        self.textsListTest = self.getTextsList('corpus_deft/deft_2011/test/deft2011_diachronie_save_300.xml')

        self.textsList = self.textsListApprentissage + self.textsListTest

        print "get motifOccur"

        self.motifsOccurences = cPickle.Unpickler(open('extractedDatas/motifsOccurenceDelfiPypy_trainOnly_1-1000.pkl', 'rb')).load()



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
        #grid_scorer = make_scorer()both
        gs = GridMultipleClasifiers(models, params)
        gs.fit(self.X, self.Y,cv=cv, scoring='f1_macro')
        gs.score_summary()
        gs.showResults()
        gs.showBest()
        #self.classifier.fit(self.apprentissageX, self.apprentissageY)








if __name__ == "__main__":
    dataB = EvaluateClassifiersByDecade()
    dataB.run()