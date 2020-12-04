import os
import ast
class FileHandler:
    BASE_DIRECTORY = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__))+os.sep, os.pardir))
    print("basepath: "+BASE_DIRECTORY)
    MAPS_DIRECTORY = BASE_DIRECTORY+os.sep+"maps"+os.sep
    def __init__(self):
        self.blendPath = FileHandler.BASE_DIRECTORY

    def getFileContentsAsLiteral(self, fileName):
        print("loading map: "+fileName)
        saveDataString = ""
        with open(fileName) as data:
            for line in data:
                saveDataString+=str(line)
        print("map load complete...")
        return ast.literal_eval(saveDataString)

    def getFileContentsAsString(self, fileName):
        print("loading map: "+fileName)
        saveDataString = ""
        with open(fileName) as data:
            for line in data:
                saveDataString+=str(line)
        print("map load complete...")
        return saveDataString

    def getMapContents(self,mapName):
        return self.getFileContentsAsLiteral(FileHandler.MAPS_DIRECTORY+mapName)
