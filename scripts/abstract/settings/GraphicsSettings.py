import bge
import copy
logic = bge.logic
class GraphicsSettings:

    VALID_KEYS = ["advancedGrass","shaders","specularity","shadows","shading","raceLine","aspectRatio4x3"]

    def __init__(self, flowState, **kwargs):
        flowState.log("GraphicsSettings.init()")
        self.flowState = flowState
        self.advancedGrass = False
        self.shaders = True
        self.specularity = True
        self.shadows = True
        self.shading = True
        self.raceLine = False
        self.aspectRatio4x3 = True

        #let's read in any arguments passed in via kwargs dictionary
        #these should override the defaults above
        self.flowState = flowState
        self.applyDictFields(kwargs)
        self.flowState.log("GraphicsSettings.init()")

    def applyDictFields(self,dict):
        for key in self.VALID_KEYS:
            newValue = dict.get(key)
            if(newValue != None):
                setattr(self, key, newValue)
                self.flowState.debug("GraphicsSettings: read valid settings key: "+str(key))
        for key in dict:
            if key not in self.VALID_KEYS:
                self.flowState.error("GraphicsSettings: invalid key passed to settings: "+str(key))

    def getSerializedSettings(self):
        serializedSettings = GraphicsSettings(**self.__dict__).__dict__ #we don't want to actually manipulate this object's fields so lets do a deep copy
        invalidKeys = [] #we're going to keep track of keys which don't need to be stored E.G. the flowState instance

        #let's build a list of key's which aren't serializable
        for key in serializedSettings:
            if key not in self.VALID_KEYS:
                invalidKeys.append(key)

        #let's remove those key's from our dictionary
        for key in invalidKeys:
            del serializedSettings[key]
        self.flowState.debug("GraphicsSettings: returning serialized settings: "+str(serializedSettings))

        return serializedSettings

    def getAdvancedGrass(self):
        return self.advancedGrass

    def setAdvancedGrass(self,advancedGrass):
        self.advancedGrass = advancedGrass
        render.showFramerate(advancedGrass)

    def getShaders(self):
        return self.shaders

    def setShaders(self,shaders):
        self.shaders = shaders

    def getSpecularity(self,specularity):
        return self.specularity

    def setSpecularity(self,specularity):
        self.specularity = specularity
        render.setGLSLMaterialSetting("shaders",specularity)

    def getShadows(self,shadows):
        return self.shadows

    def setShadows(self,shadows):
        self.shadows = shadows
        render.setGLSLMaterialSetting("shadows",shadows)

    def getShading(self,shading):
        return self.shading

    def setShading(self,shading):
        self.shading = shading
        render.setGLSLMaterialSetting("lights",shading)

    def getRaceLine(self,raceLine):
        return self.raceLine

    def setRaceLine(self,raceLine):
        self.raceLine = raceLine

    def aspectRatioIs4x3(self):
        return self.aspectRatio4x3

    def setAspectRatio4x3(self,is4x3):
        self.aspectRatio4x3 = is4x3
