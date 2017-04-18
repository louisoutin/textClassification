#!/usr/bin/python3
# -*- coding: utf-8 -*-

from sklearn.metrics import accuracy_score, confusion_matrix, roc_auc_score, average_precision_score
from sklearn.preprocessing import label_binarize
from sklearn.metrics import f1_score
import numpy as np


"""
Interface metrics qui contients les différentes fonctions de scoring
"""
class Metrics():

    def accuracy_score(self,y_test,y_pred):
        return (100 * accuracy_score(y_test, y_pred))

    def well_detected_spam(self,y_test,y_pred):
        return confusion_matrix(y_test, y_pred)[1][1]

    def well_detected_ham(self,y_test,y_pred):
        return confusion_matrix(y_test, y_pred)[0][0]

    def roc_score(self,y_test,y_pred):
        return roc_auc_score(y_test, y_pred)

    def precision(self,y_test,y_pred):
        binarized_y_test = label_binarize(y_test, classes=['ham', 'spam'])
        binarized_y_pred = label_binarize(y_pred, classes=['ham', 'spam'])
        return average_precision_score(binarized_y_test, binarized_y_pred)

    def f1_scorer(self,y_test,y_pred):
        return f1_score(y_test, y_pred, average='weighted')


    def gaussianDistance(self, ground_truth, predictions):
            diff = np.exp((-np.pi/10**2)*((predictions-ground_truth)**2))
            return np.mean(diff)

    def medianeGaussianDistance(self, ground_truth, predictions):
            diff = np.exp((-np.pi/10**2)*((predictions-ground_truth)**2))
            return np.median(diff)

    def ecartTypeGaussianDistance(self, ground_truth, predictions):
            diff = np.exp((-np.pi/10**2)*((predictions-ground_truth)**2))
            return np.std(diff)

    def varianceGaussianDistance(self, ground_truth, predictions):
            diff = np.exp((-np.pi/10**2)*((predictions-ground_truth)**2))
            return np.var(diff)

if __name__=="__main__":
    g = np.array([1946])
    p= np.array([1946])
    print Metrics().gaussianDistance(g,p)

    # Fonction de score DEFT verifiée sur les resultats de la page pdf: OK