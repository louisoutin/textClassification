#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from extractorForBagOfWords import *
from sklearn.model_selection import train_test_split
from sklearn.multiclass import OneVsRestClassifier
from sklearn.svm import LinearSVC
from text.textChanson import *
from sklearn.preprocessing import label_binarize

import numpy as np
import matplotlib.pyplot as plt
from itertools import cycle

from sklearn import svm, datasets
from sklearn.metrics import roc_curve, auc
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import label_binarize
from sklearn.multiclass import OneVsRestClassifier
from scipy import interp

from sklearn.feature_extraction.text import CountVectorizer

class DataBase():

    def __init__(self, folder):
        self.textsList = self.getTextsList(folder)

        self.motifsOccurences = get_motifs(self.textsList,
                                           { 'minsup':2,
                                             'maxsup':10,
                                             'minlen':3,
                                             'maxlen':6})

        print self.motifsOccurences[0]

        self.vectorizer = CountVectorizer(min_df=1, decode_error="ignore")
        self.vecteursTraits = self.vectorizer.fit_transform(self.motifsOccurences)
        self.classesTextes = self.getClassesTextes()


        self.apprentissageX, self.testX, self.apprentissageY, self.testY = train_test_split(self.vecteursTraits, self.classesTextes, test_size=0.1, random_state=42)
        #self.testX, self.testY = [], []
        #self.separationEnsembles(0.1)
        #self.clf = svm.SVC()
        #self.clf.fit(self.apprentissageX, self.apprentissageY)
        self.classifier = OneVsRestClassifier(LinearSVC(random_state=0))
        self.classifier.fit(self.apprentissageX, self.apprentissageY)
        self.scoreY = self.classifier.decision_function(self.testX)

        #self.ROCsimple()

    def ROCsimple(self):
        testY = label_binarize(self.testY, classes=[0, 1, 2, 3, 4])
        scoreY = self.scoreY
        fpr = dict()
        tpr = dict()
        roc_auc = dict()
        for i in range(5):
            fpr[i], tpr[i], _ = roc_curve(testY[:, i], scoreY[:, i])
            roc_auc[i] = auc(fpr[i], tpr[i])

        print testY[:, 3]
        print scoreY

        # Compute micro-average ROC curve and ROC area
        fpr["micro"], tpr["micro"], _ = roc_curve(testY.ravel(), scoreY.ravel())
        roc_auc["micro"] = auc(fpr["micro"], tpr["micro"])

        print roc_auc


        plt.figure()
        lw = 2
        plt.plot(fpr[1], tpr[1], color='darkorange',
                 lw=lw, label='ROC curve (area = %0.2f)' % roc_auc[1])
        plt.plot([0, 1], [0, 1], color='navy', lw=lw, linestyle='--')
        plt.xlim([0.0, 1.0])
        plt.ylim([0.0, 1.05])
        plt.xlabel('False Positive Rate')
        plt.ylabel('True Positive Rate')
        plt.title('Receiver operating characteristic example')
        plt.legend(loc="lower right")
        plt.show()

    def ROCmultiple(self):


        # First aggregate all false positive rates
        all_fpr = np.unique(np.concatenate([fpr[i] for i in range(n_classes)]))

        # Then interpolate all ROC curves at this points
        mean_tpr = np.zeros_like(all_fpr)
        for i in range(n_classes):
            mean_tpr += interp(all_fpr, fpr[i], tpr[i])

        # Finally average it and compute AUC
        mean_tpr /= n_classes

        lw = 2

        fpr["macro"] = all_fpr
        tpr["macro"] = mean_tpr
        roc_auc["macro"] = auc(fpr["macro"], tpr["macro"])

        # Plot all ROC curves
        plt.figure()
        plt.plot(fpr["micro"], tpr["micro"],
                 label='micro-average ROC curve (area = {0:0.2f})'
                       ''.format(roc_auc["micro"]),
                 color='deeppink', linestyle=':', linewidth=4)

        plt.plot(fpr["macro"], tpr["macro"],
                 label='macro-average ROC curve (area = {0:0.2f})'
                       ''.format(roc_auc["macro"]),
                 color='navy', linestyle=':', linewidth=4)

        colors = cycle(['aqua', 'darkorange', 'cornflowerblue'])
        for i, color in zip(range(n_classes), colors):
            plt.plot(fpr[i], tpr[i], color=color, lw=lw,
                     label='ROC curve of class {0} (area = {1:0.2f})'
                           ''.format(i, roc_auc[i]))

        plt.plot([0, 1], [0, 1], 'k--', lw=lw)
        plt.xlim([0.0, 1.0])
        plt.ylim([0.0, 1.05])
        plt.xlabel('False Positive Rate')
        plt.ylabel('True Positive Rate')
        plt.title('Some extension of Receiver operating characteristic to multi-class')
        plt.legend(loc="lower right")
        plt.show()

    """
    Retourne la liste des textes d'un dossier 'folder' passé en argument
    """
    def getTextsList(self,folder):
        textsList = []
        for dirname, dirnames, filenames in os.walk(folder):

            # print path to all filenames.
            for filename in filenames:
                text = TextChanson(os.path.join(dirname, filename))
                #print(os.path.join(dirname, filename))
                textsList.append(text)
        return textsList

    """
    Retourne la classe d'une annee 'year' passé en argument
    """
    def getClasse(self, year):
        if year[:3] == "197":
            return 0
        if year[:3] == "198":
            return 1
        if year[:3] == "199":
            return 2
        if year[:3] == "200":
            return 3
        if year[:3] == "201":
            return 4

    """
    Retourne le Vecteur X, pour chaque texte, son nombre d'occurence de chacun des motifs extraits
    """
    def getVecteursTraits(self):

        dico = self.motifsOccurences
        listeVecteurs = []
        for numTexte in range(len(self.textsList)):
            vecteurTexte = []
            for motif in range(len(dico)):
                if numTexte in dico[motif][1]:
                    vecteurTexte.append(dico[motif][1][numTexte])
                else:
                    vecteurTexte.append(0)
            listeVecteurs.append(vecteurTexte)
        return listeVecteurs


    """
    Retourne la liste des classes des textes contenus dans self.textsList
    """
    def getClassesTextes(self):
        listeClasses = []
        for texte in self.textsList:
            listeClasses.append(self.getClasse(texte.date))
        return listeClasses



    def separationEnsembles(self, pourcentage):
        cp = {}
        cp[0] = round(self.classesTextes.count(0)*pourcentage)
        cp[1] = round(self.classesTextes.count(1)*pourcentage)
        cp[2] = round(self.classesTextes.count(2)*pourcentage)
        cp[3] = round(self.classesTextes.count(3)*pourcentage)
        cp[4] = round(self.classesTextes.count(4)*pourcentage)
        for i in range(len(self.vecteursTraits)):
            if cp[self.classesTextes[i]]>0:
                self.testX.append(self.vecteursTraits[i])
                self.testY.append(self.classesTextes[i])
                cp[self.classesTextes[i]]-=1
            else:
                self.apprentissageX.append(self.vecteursTraits[i])
                self.apprentissageY.append(self.classesTextes[i])


    """
    Predit la classe d'un texte passé par son chemin en parametre 'path'
    """
    def predict(self):
        return self.clf.predict([vecteurX])

    def eval_res(self, l1, l2):
        dic = {x: {"VP": 0, "FP": 0, "FN": 0} for x in set(l1)}
        for i in range(len(l1)):
            if l1[i] == l2[i]:
                dic[l1[i]]["VP"] += 1
            else:
                dic[l1[i]]["FN"] += 1
                dic[l2[i]]["FP"] += 1
        return dic

    def printEvalRes(self, dic):
        for i in dic:
            rappel = float(dic[i]["VP"])/(dic[i]["VP"]+dic[i]["FN"])
            precision = float(dic[i]["VP"]) / (dic[i]["VP"] + dic[i]["FP"])
            #f_mesure = 2*(precision*rappel)/(precision+rappel)
            print "Classe"+str(i)
            print "Rappel : "+str(rappel)+"      Precision : "+str(precision)+"      F-mesure : "


if __name__ == "__main__":
    dataB = DataBase("Corpus")
    #print dataB.textsList
    #print dataB.motifsOccurences
    #print len(dataB.textsList)
    print dataB.classifier
    prediction = []
    #print dataB.vectorizer.get_feature_names()
    arrayX = dataB.testX.toarray()
    for i in range(len(arrayX)):
        prediction.append(dataB.classifier.predict([arrayX[i]])[0])
    print "la réalité    ==>", dataB.testY
    print "la prediction ==>", prediction

    eval_res =dataB.eval_res(dataB.testY, prediction)
    print eval_res
    dataB.printEvalRes(eval_res)
    #print dataB.vecteursTraits
    #print dataB.predict("CorpusTest/1971_test7")
