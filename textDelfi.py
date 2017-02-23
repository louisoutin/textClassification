import re
import sys
import os

from extracteur.extracteur_motifs import *

class Text():

    def __init__(self,date,body):
        self.title = "title"
        self.date = date
        self.body = body

    def getTitle(self, path):
        return (path.split("/")[-1]).split("_")[1]

    def __str__(self):
        return "Date => "+self.date+"\nTitle => "+self.title+"\n\n"+str(self.body)

if __name__ == "__main__":

    texte = Text("1993","Texte de test")
    print texte.date
    print texte.body
