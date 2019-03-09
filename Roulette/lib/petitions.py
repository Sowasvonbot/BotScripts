
import os
import codecs


class myPetitions(object):
    PathPetitions = os.path.join(os.path.dirname(__file__), "Petitions/petitions.txt")
    allPetitions = []
    _instance = None

    @staticmethod
    def getInstance():
        if myPetitions._instance == None:
            myPetitions()
        return myPetitions._instance
    
    def __init__(self):
        myPetitions._instance = self
        try:
            with codecs.open(self.PathPetitions, encoding="utf-8-sig", mode="r") as petFile:
                for line in petFile.readlines():
                    self.allPetitions.append(str(line))
        except:
            self.allPetitions = [0]
        
        
