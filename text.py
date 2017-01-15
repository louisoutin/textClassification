import re
import sys
import os

from extracteur.extracteur_motifs import *

class Text():

    def __init__(self,path):
        self.file = open(path)
        self.title = self.getTitle(path)
        self.date = self.getDate(path)
        self.body = self.getBody()

    def getTitle(self, path):
        return (path.split("/")[-1]).split("_")[1]

    def getDate(self, path):
        return (path.split("/")[-1]).split("_")[0]

    def getBody(self):
        body = self.file.read().replace('\n', ' ')
        return re.sub(' +', " ", body)

    def __str__(self):
        return "Date => "+self.date+"\nTitle => "+self.title+"\n\n"+str(self.body)

if __name__ == "__main__":

    texte = Text("Corpus/1990/1993_Letangoducachalot")
    print texte.body
    liste_motifs = get_motifs([texte.body])
    print liste_motifs