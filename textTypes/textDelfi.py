
class TextDelfi():

    def __init__(self,date,body):
        self.title = "title"
        self.date = date
        self.body = body


    def __str__(self):
        return "Date => "+self.date+"\nTitle => "+self.title+"\n\n"+str(self.body)

if __name__ == "__main__":

    texte = TextDelfi("1993", "Texte de test")
    print texte.date
    print texte.body
