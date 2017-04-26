#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sklearn.naive_bayes import MultinomialNB, GaussianNB, BernoulliNB

from sklearn.model_selection import ShuffleSplit

from GridMultipleClasifiers import GridMultipleClasifiers

from sklearn.multiclass import OneVsRestClassifier
from sklearn.svm import *
import cPickle

from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer, TfidfVectorizer
from ClassifierUtils import *
import os.path
import subprocess


class EvaluateClassifiersDecadeByDecade(ClassifierUtils):

    def __init__(self, apprentissage, bagOfWords=False, minlen=3, maxlen=7):

        print "get text 1"

        self.textsListApprentissage = self.getTextsList(apprentissage)

        print "get motifOccur"

        savedFile = "extractedDatas/motifsOccurenceDelfiPypy_onlyTrain_nbWords=" + apprentissage[-7:-4] + "_minlen=" + str(minlen) + "_maxlen=" + str(maxlen)

        if not bagOfWords:
            print "repeatly maximum strings extraction..."
            if os.path.isfile(savedFile) :
                print ("Extracted datas file already exist, unpickling...")
                self.motifsOccurences = cPickle.Unpickler(open(savedFile, 'rb')).load()
            else:
                print ("Extracted datas file do not exist, computing it...")
                os.chdir("patternsOccurence_saver")
                subprocess.call(["pypy", "DelfiPatternsSaver.py", "../"+apprentissage, "None",str(minlen),str(maxlen)])
                print ("Unpickling extracted datas file...")
                os.chdir("../")
                self.motifsOccurences = cPickle.Unpickler(open(savedFile, 'rb')).load()
        else:
                print "bag of word extraction..."
                self.motifsOccurences = [texte.body for texte in self.textsListApprentissage]


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
    dataB = EvaluateClassifiersDecadeByDecade('corpus_deft/deft_2011/appr/deft2011_diachronie_appr_300.xml', bagOfWords=True)
    dataB.run()