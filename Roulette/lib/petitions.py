
import os
import codecs


class myPetitions(object):
    PathPetitions = os.path.join(os.path.dirname(__file__), "Petitions/petitions.txt")
    allPetitions = []
    
    def __init__(self):
        try:
            with codecs.open(self.PathPetitions, encoding="utf-8-sig", mode="r") as petFile:
                for line in petFile.readlines():
                    self.allPetitions.append(str(line))
        except:
            self.allPetitions = [0]