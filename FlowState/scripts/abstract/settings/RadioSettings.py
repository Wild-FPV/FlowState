import bge
import copy
logic = bge.logic
class RadioSettings:

    VALID_KEYS = ["throttleInverted","yawInverted","pitchInverted","rollInverted","armInverted","resetInverted","yawChannel","pitchChannel","throttleChannel","rollChannel","resetChannel","armChannel","yawOffset","pitchOffset","rollOffset","minThrottle","maxThrottle","minYaw","maxYaw","minPitch","maxPitch","minRoll","maxRoll","minReset","maxReset","minArm","maxArm","armSetpoint","resetSetpoint","dedicatedThrottleStick"]

    def __init__(self, flowState, **kwargs):
        flowState.log("RadioSettings.init()")
        self.flowState = flowState
        self.throttleInverted = False
        self.yawInverted = False
        self.pitchInverted = False
        self.rollInverted = False
        self.armInverted = True
        self.resetInverted = False
        self.yawChannel = 1
        self.pitchChannel = 4
        self.throttleChannel = 2
        self.rollChannel = 3
        self.resetChannel = 6
        self.armChannel = 5
        self.yawOffset = 0
        self.pitchOffset = 0
        self.rollOffset = 0
        self.minThrottle = -32252
        self.maxThrottle = 32252
        self.minYaw = -32252
        self.maxYaw = 32252
        self.minPitch = -32252
        self.maxPitch = 32252
        self.minRoll = -32252
        self.maxRoll = 32252
        self.minReset = 0
        self.maxReset = 32768
        self.minArm = 0
        self.maxArm = 32768
        self.armSetpoint = 0.5
        self.resetSetpoint = 0.5
        self.dedicatedThrottleStick = True

        #let's read in any arguments passed in via kwargs dictionary
        #these should override the defaults above
        self.flowState = flowState
        self.applyDictFields(kwargs)
        self.flowState.log("RadioSettings.init()")

    def applyDictFields(self,dict):
        for key in self.VALID_KEYS:
            newValue = dict.get(key)
            if(newValue != None):
                setattr(self, key, newValue)
                self.flowState.debug("RadioSettings: read valid settings key: "+str(key))
        for key in dict:
            if key not in self.VALID_KEYS:
                self.flowState.error("RadioSettings: invalid key passed to settings: "+str(key))

    def getSerializedSettings(self):
        serializedSettings = RadioSettings(**self.__dict__).__dict__ #we don't want to actually manipulate this object's fields so lets do a deep copy
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

    def setEasyDefaults(self):
        easyDefaults = {'throttleInverted':True,'yawInverted':False,'pitchInverted':True,'rollInverted':False,'armInverted':True,'resetInverted':False,'yawChannel':1,'pitchChannel':4,'throttleChannel':2,'rollChannel':3,'resetChannel':6,'armChannel':5,'yawOffset':0,'pitchOffset':0,'rollOffset':0,'minThrottle':-32252,'maxThrottle':32252,'minYaw':-32252,'maxYaw':32252,'minPitch':-32252,'maxPitch':32252,'minRoll':-32252,'maxRoll':32252,'minReset':0,'maxReset':32768,'minArm':0,'maxArm':32768,'armSetpoint':0.5,'resetSetpoint':0.5,'dedicatedThrottleStick':True}
        self.applyDictFields(easyDefaults)
