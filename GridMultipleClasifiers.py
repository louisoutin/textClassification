
# -*- coding: utf-8 -*-

import numpy as np
from sklearn.model_selection import GridSearchCV

'''
Classe qui permet d'agréger plusieurs gridSearch pour pouvoir comparer
plusieurs classifiers avec leur jeux de paramètres respectifs.
'''
class GridMultipleClasifiers:
    def __init__(self, models, params):
        if not set(models.keys()).issubset(set(params.keys())):
            missing_params = list(set(models.keys()) - set(params.keys()))
            raise ValueError("Some estimators are missing parameters: %s" % missing_params)
        self.models = models
        self.params = params
        self.keys = models.keys()
        self.grid_searches = {} # Dictionnaire qui contient tous les gridsearchs
        self.results = []

    '''
    Méthode qui permet de fit les différents classifieurs
    '''
    def fit(self, X, y, cv=3, n_jobs=-1, verbose=True, scoring=None):
        for key in self.keys:
            print("Running GridSearchCV for %s." % key)
            model = self.models[key]
            params = self.params[key]

            gs = GridSearchCV(model, param_grid=params, cv=cv, n_jobs=n_jobs,
                              verbose=verbose, scoring=scoring)
            gs.fit(X,y)
            self.grid_searches[key] = gs

    """
    Méthode qui permet de classer tous les scores en fonction d'une fonction de scoring défini avant
    """
    def score_summary(self):
        result = []
        for key in self.keys:
            elts = self.grid_searches[key].cv_results_
            for i in np.argsort(elts['mean_test_score']):
                result.append((elts['mean_test_score'][i],
                               key,
                                elts['params'][i]))
        self.results = sorted(result, key=lambda tup: tup[0])

    """
    Affiche les résultats par ordre décroissant
    """
    def showResults(self):
        for i in reversed(self.results):
            print(i)

    """
    Affiche le classifieur qui réalise le meilleur score
    """
    def showBest(self):
        print( "  ----------------------  ")
        best = self.results[-1]
        print("Best classifier ", best[1])
        print("Best score: %0.3f" % best[0])
        print("Best parameters set:")
        print(best[2])
        print("  ----------------------  ")