#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ClassifierUtils import *
from ClassifierTwoStratsPreliminary import *
import os.path
import subprocess


class ClassifierTwoStratsMain(ClassifierUtils):

    def __init__(self, apprentissage, test, bagOfWords=False, minlen=3, maxlen=7):

        self.nbWords = apprentissage[-7:-4]
        self.bagOfWords = bagOfWords

        print "get text 1"

        self.textsListApprentissage = self.getTextsList(apprentissage)

        print "get text 2"

        self.textsListTest = self.getTextsList(test)

        self.textsList = self.textsListApprentissage + self.textsListTest

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

        print "load prediction First Strat"

        if not bagOfWords:
            firstStratPredictionFile = "extractedDatas/predictionFirstStrat_nbWords=" + self.nbWords + "_minlen=" + str(minlen) + "_maxlen=" + str(maxlen) + ".pkl"
            print "repeatly maximum strings loading first prediction strat"
            if os.path.isfile(firstStratPredictionFile):
                print ("Extracted datas file already exist, unpickling...")
                self.decadePredictions = cPickle.Unpickler(open(firstStratPredictionFile, 'rb')).load()
            else:
                print ("Extracted datas file do not exist, computing...")
                dataB = ClassifierTwoStratsPreliminary(apprentissage, test, bagOfWords, minlen, maxlen)
                dataB.run()
                print "Unpickling datas..."
                self.decadePredictions = cPickle.Unpickler(open(firstStratPredictionFile, 'rb')).load()
        else:
            firstStratPredictionFile = "extractedDatas/predictionFirstStrat_nbWords=" + self.nbWords + "_bagOfWord.pkl"
            print "Bag Of Words loading first prediction strat"
            if os.path.isfile(firstStratPredictionFile):
                print ("Extracted datas file already exist, unpickling...")
                self.decadePredictions = cPickle.Unpickler(open(firstStratPredictionFile, 'rb')).load()
            else:
                print ("Extracted datas file do not exist, computing...")
                dataB = ClassifierTwoStratsPreliminary(apprentissage, test, bagOfWords, minlen, maxlen)
                dataB.run()
                print "Unpickling datas..."
                self.decadePredictions = cPickle.Unpickler(open(firstStratPredictionFile, 'rb')).load()


        print "load classifiers 30 years fitting samples"

        if not bagOfWords:
            fitingSamples = "extractedDatas/classifiersThirtyYears_nbWords=" + self.nbWords + "_minlen=" + str(
                minlen) + "_maxlen=" + str(maxlen) + ".pkl"
            print "repeatly maximum strings loading first prediction strat"
            if os.path.isfile(fitingSamples):
                print ("Extracted datas file already exist, unpickling...")
                self.classifiersThirtyYearsTrainSet = cPickle.Unpickler(open(fitingSamples, 'rb')).load()
            else:
                print ("Extracted datas file do not exist, computing...")
                dataB = ClassifierTwoStratsPreliminary(apprentissage, test, bagOfWords, minlen, maxlen)
                dataB.run()
                print "Unpickling datas..."
                self.classifiersThirtyYearsTrainSet = cPickle.Unpickler(open(fitingSamples, 'rb')).load()
        else:
            fitingSamples = "extractedDatas/classifiersThirtyYears_nbWords=" + self.nbWords + "_bagOfWord.pkl"
            print "Bag Of Words loading first prediction strat"
            if os.path.isfile(fitingSamples):
                print ("Extracted datas file already exist, unpickling...")
                self.classifiersThirtyYearsTrainSet = cPickle.Unpickler(open(fitingSamples, 'rb')).load()
            else:
                print ("Extracted datas file do not exist, computing...")
                dataB = ClassifierTwoStratsPreliminary(apprentissage, test, bagOfWords, minlen, maxlen)
                dataB.run()
                print "Unpickling datas..."
                self.classifiersThirtyYearsTrainSet = cPickle.Unpickler(open(fitingSamples, 'rb')).load()

        # Initialisation de la liste des classifieurs locaux
        self.classifiersThirtyYears = []



    def run(self):

        print "vector transform"


        self.Yapprentissage = self.getClassesTextes(self.textsListApprentissage)

        self.Ytest = self.getClassesTextes(self.textsListTest)

        self.vectorizer = TfidfVectorizer(min_df=1, decode_error="ignore",lowercase=False)

        self.Xapprentissage = self.vectorizer.fit_transform(self.motifsOccurencesApprentissage)

        self.Xtest = self.vectorizer.transform(self.motifsOccurencesTest)

        cpt = 1
        for (X,Y) in self.classifiersThirtyYearsTrainSet:
            print str(cpt)+" / 15 fitting"
            cpt+=1
            if not self.bagOfWords:
                classifier = OneVsRestClassifier(MultinomialNB(alpha=0.1, fit_prior=False))
            else:
                classifier = OneVsRestClassifier(LinearSVC(random_state=0, C=1.5))
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
        wellDetectedDecades = Metrics().decadesWellDetected(self.Ytest, predictionFinal)

        print"moyenne : "+str(score)
        print"mediane : " + str(median)
        print"ecart-type : " + str(ecart_type)
        print"variance : " + str(variance)
        print "décennies bien prédites : " + str(wellDetectedDecades)




    """
    Retourne la classe d'une annee 'year' passé en argument
    """
    def getClasse(self, year):
        return int(year[0:4])





if __name__ == "__main__":
    dataB = ClassifierTwoStratsMain('corpus_deft/deft_2011/appr/deft2011_diachronie_appr_500.xml', 'corpus_deft/deft_2011/test/deft2011_diachronie_save_500.xml', bagOfWords=True)
    dataB.run()