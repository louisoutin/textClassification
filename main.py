#!/usr/bin/python
# -*- coding: utf-8 -*-

from ClassifierByDecades import *
from ClassifierByYears import *
from ClassifierSongTexts import *
from ClassifierTwosStratsMain import *
from EvaluateClassifersDecadeByDecade import *
from EvaluateClassifersYearByYear import *


###
###  Commenter ou décommenter les algorithmes de classification voulant être lancé.
###

print "\nClassification des textes de chansons par décénnies\n"

# Classification des textes de chansons
dataB0 = ClassifierSongTexts("Corpus")
dataB0.run()

print "\nEvaluation de la classification des textes de journaux par décénnies\n"

# Evaluation des classifieurs sur les décennies
dataB1 = EvaluateClassifiersDecadeByDecade('corpus_deft/deft_2011/appr/deft2011_diachronie_appr_300.xml', bagOfWords=False)
dataB1.run()

print "\nEvaluation de la classification des textes de journaux par années\n"

# Evaluation des classifieurs sur les années
dataB2 = EvaluateClassifiersYearByYear('corpus_deft/deft_2011/appr/deft2011_diachronie_appr_300.xml', bagOfWords=False)
dataB2.run()

print "\nClassification des textes de journaux par décennies\n"

# Classification par décennies
dataB3 = ClassifierByDecades('corpus_deft/deft_2011/appr/deft2011_diachronie_appr_300.xml', 'corpus_deft/deft_2011/test/deft2011_diachronie_save_300.xml', bagOfWords=False)
dataB3.run()

print "\nClassification des textes de journaux par années\n"

# Classification par années
dataB4 = ClassifierByYears('corpus_deft/deft_2011/appr/deft2011_diachronie_appr_500.xml', 'corpus_deft/deft_2011/test/deft2011_diachronie_save_500.xml', bagOfWords=False)
dataB4.run()

print "\nClassification des textes de journaux par années (en 2 étapes)\n"

# Classification en 2 étapes
dataB5 = ClassifierTwoStratsMain('corpus_deft/deft_2011/appr/deft2011_diachronie_appr_500.xml', 'corpus_deft/deft_2011/test/deft2011_diachronie_save_500.xml', bagOfWords=True)
dataB5.run()

