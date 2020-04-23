import bge
import copy
logic = bge.logic
class DroneSettings:

    VALID_KEYS = ["autoLevel","cameraTilt","thrust","motorKV","pDrag","iDrag","batteryCellCount","weight","timeScale","yawExpo","pitchExpo","rollExpo","pitchRate","rollRate","yawRate","pitchSuperRate","rollSuperRate","yawSuperRate","videoChannel"]

    def __init__(self, flowState, **kwargs):
        self.autoLevel = False
        self.cameraTilt = 40
        self.videoChannel = 0
        self.thrust = 3100
        self.motorKV = 1700
        self.pDrag = 50
        self.iDrag = 50
        self.batteryCellCount = 6
        self.weight = 500
        self.timeScale = 100
        self.yawExpo = 0.0
        self.pitchExpo = 0.0
        self.rollExpo = 0.0
        self.pitchRate = 100
        self.rollRate = 100
        self.yawRate = 100
        self.pitchSuperRate = 70
        self.rollSuperRate = 70
        self.yawSuperRate = 70

        #let's read in any arguments passed in via kwargs dictionary
        #these should override the defaults above
        self.flowState = flowState
        self.applyDictFields(kwargs)
        self.flowState.log("DroneSettings.init()")

    def applyDictFields(self,dict):
        for key in self.VALID_KEYS:
            newValue = dict.get(key)
            if(newValue != None):
                setattr(self, key, newValue)
                self.flowState.debug("DroneSettings: read valid settings key: "+str(key))
        for key in dict:
            if key not in self.VALID_KEYS:
                self.flowState.error("DroneSettings: invalid key passed to settings: "+str(key))

    def getSerializedSettings(self):
        serializedSettings = DroneSettings(**self.__dict__).__dict__ #we don't want to actually manipulate this object's fields so lets do a deep copy
        invalidKeys = [] #we're going to keep track of keys which don't need to be stored E.G. the flowState instance

        #let's build a list of key's which aren't serializable
        for key in serializedSettings:
            if key not in self.VALID_KEYS:
                invalidKeys.append(key)

        #let's remove those key's from our dictionary
        for key in invalidKeys:
            del serializedSettings[key]
        self.flowState.debug("DroneSettings: returning serialized settings: "+str(serializedSettings))

        return serializedSettings

    def setEasyDefaults(self):
        easyDefaults = {'autoLevel':True,'cameraTilt':30,'thrust':1000,'motorKV':1700,"pDrag":50,"iDrag":50,'batteryCellCount':6,'weight':500, "timeScale":100, 'yawExpo':0.0,'pitchExpo':0.0,'rollExpo':0.0,'pitchRate':50,'rollRate':50,'yawRate':50,'pitchSuperRate':70,'rollSuperRate':70,'yawSuperRate':70}
        self.applyDictFields(easyDefaults)
