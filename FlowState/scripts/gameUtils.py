import bge
import copy
import os
logic = bge.logic
class flowState:
    #asset keys
    ASSET_MGP_GATE = "asset MGP gate"
    ASSET_MGP_GATE_DOUBLE = "asset MGP gate double"
    ASSET_MGP_GATE_LARGE = "asset MGP gate large"
    ASSET_MGP_GATE_HANGING_LARGE = "asset MGP gate hanging large"
    ASSET_MGP_GATE_HIGH_LARGE = "asset MGP gate high large"
    ASSET_MGP_GATE_DOUBLE_LARGE = "asset MGP gate double large"
    ASSET_MGP_LADDER_LARGE = "asset MGP ladder large"
    ASSET_MGP_GATE_ANGLED_DIVE_LARGE = "asset MGP gate angled dive large"
    ASSET_MGP_GATE_DIVE_LARGE = "asset MGP gate dive large"
    ASSET_MGP_HURDLE = "asset MGP hurdle"
    ASSET_MGP_HURDLE_LARGE = "asset MGP hurdle large"
    ASSET_MGP_FLAG = "asset MGP flag"
    ASSET_MGP_POLE = "asset pole"
    ASSET_LUMENIER_GATE_LARGE = "asset lumenier gate large"
    ASSET_TABLE = "asset table"
    ASSET_LAUNCH_PAD = "asset launch pad"
    ASSET_CONE = "asset cone"
    ASSET_START_FINISH = "asset start finish"
    ASSET_CHECKPOINT = "asset checkpoint square"
    ASSET_CONCRETE_BLOCK = "asset concrete block"
    ASSET_PINE_TREE_TALL = "asset pine tree 12m"
    ASSETS = [ASSET_MGP_GATE,ASSET_MGP_GATE_DOUBLE,ASSET_MGP_GATE_LARGE,ASSET_MGP_GATE_HANGING_LARGE,ASSET_MGP_GATE_HIGH_LARGE,ASSET_MGP_GATE_DOUBLE_LARGE,ASSET_MGP_LADDER_LARGE,ASSET_MGP_GATE_ANGLED_DIVE_LARGE,ASSET_MGP_GATE_DIVE_LARGE,ASSET_MGP_HURDLE,ASSET_MGP_HURDLE_LARGE,ASSET_MGP_FLAG,ASSET_MGP_POLE,ASSET_LUMENIER_GATE_LARGE,ASSET_TABLE,ASSET_LAUNCH_PAD,ASSET_CONE,ASSET_CONCRETE_BLOCK,ASSET_PINE_TREE_TALL,ASSET_START_FINISH,ASSET_CHECKPOINT]

    #asset metadata types
    METADATA_GATE = {"id":-1}
    STATIC_METADATA = ["id"]
    METADATA_CHECKPOINT = {"id":-1,"checkpoint order":1}

    #game state keys
    STATE_SELECTED_MAP_KEY = "selectedMap"
    STATE_SERVER_IP_KEY = "serverIP"
    STATE_MAP_EDITOR_KEY = "mapEditor"
    STATE_GAME_MODE_KEY = "gameMode"
    STATE_VIEW_MODE_KEY = "viewMode"
    STATE_NETWORK_CLIENT_KEY = "networkClient"
    STATE_LAP_KEY = "lap"
    STATE_PLAYER_DATA_KEY = "playerData"
    STATE_PLAYER_OBJECT_KEY = "playerObject"
    STATE_FIRST_RUN = "first run"

    #view mode keys
    VIEW_MODE_MENU=0
    VIEW_MODE_PLAY=1

    #game mode keys
    GAME_MODE_EDITOR = 0
    GAME_MODE_SINGLE_PLAYER = 1
    GAME_MODE_MULTIPLAYER = 2

    def __init__(self):
        self.log("gameflowState.init")
        self.setDefaults()
        self.gameState = self.getDefaultGameState()
        self.id = 0

    def log(self,error):
        error = str(error)
        userHome = str(logic.expandPath("//"))#os.path.expanduser('~')
        logFile = "flowstate.log"
        path = os.path.join(userHome,logFile)

        print("LOG: "+error)
        with open(path, 'a+') as saveFile:
            saveFile.write(str(error)+"\n")
            saveFile.close()

    def addMetadata(self,asset):
        self.log("gameflowState.addMetadata("+str(asset)+")")
        asset['metadata'] = {}
        if 'gate' in asset.name:
            asset['metadata'] = copy.deepcopy(flowState.METADATA_GATE)

        if 'checkpoint' in asset.name:
            asset['metadata'] = copy.deepcopy(flowState.METADATA_CHECKPOINT)
        asset['metadata']['id'] = self.getNewID()

    def getNewID(self):
        #self.log("gameflowState.getNewID()")
        self.id+=1
        return self.id

    def setDefaultState(self):
        self.log("gameflowState.setDefaultState()")
        self.gameState = copy.deepcopy(logic.defaultGameState)

    def getDefaultGameState(self):
        #self.log("gameflowState.getDefaultGameState()")
        return copy.deepcopy(logic.defaultGameState)

    def getGameState(self):
        #self.log("gameflowState.getGameState()")
        return self.gameState

    def getPlayerObject(self):
        #self.log("gameflowState.getPlayerObject()")
        return self.gameState[flowState.STATE_PLAYER_DATA_KEY][flowState.STATE_PLAYER_OBJECT_KEY]

    def setPlayerObject(self,value):
        self.log("gameflowState.setPlayerObject("+str(value)+")")
        self.gameState[flowState.STATE_PLAYER_DATA_KEY][flowState.STATE_PLAYER_OBJECT_KEY] = value

    def resetGameState(self):
        self.log("gameflowState.resetGameState()")
        self.gameState = copy.deepcopy(logic.defaultGameState)

    def selectMap(self,selectedMap):
        self.log("gameflowState.selectMap("+str(selectedMap)+")")
        self.gameState[flowState.STATE_SELECTED_MAP_KEY] = selectedMap

    def setServerIP(self,serverIP):
        self.log("gameflowState.setServerIP("+str(serverIP)+")")
        self.gameState[flowState.STATE_SERVER_IP_KEY] = serverIP

    def getServerIP(self):
        #self.log("gameflowState.getServerIP()")
        print("server ip is "+repr(str(self.gameState[flowState.STATE_SERVER_IP_KEY])))
        return self.gameState[flowState.STATE_SERVER_IP_KEY]

    def getSelectedMap(self):
        #self.log("gameflowState.getSelectedMap()")
        return self.gameState[flowState.STATE_SELECTED_MAP_KEY]

    def getMapEditor(self):
        #self.log("gameflowState.getMapEditor()")
        return self.gameState[flowState.STATE_MAP_EDITOR_KEY]

    def setGameMode(self,newMode):
        self.log("gameflowState.setGameMode("+str(newMode)+")")
        print("set game mode: "+str(newMode))
        self.gameState[flowState.STATE_GAME_MODE_KEY] = newMode

    def getGameMode(self):
        #self.log("gameflowState.getGameMode()")
        return self.gameState[flowState.STATE_GAME_MODE_KEY]

    def setViewMode(self,newMode):
        self.log("gameflowState.setViewMode("+str(newMode)+")")
        self.gameState[flowState.STATE_VIEW_MODE_KEY] = newMode

    def getViewMode(self):
        #self.log("gameflowState.getViewMode()")
        return self.gameState[flowState.STATE_VIEW_MODE_KEY]

    def getNetworkClient(self):
        #self.log("gameflowState.getNetworkClient()")
        return self.gameState[flowState.STATE_NETWORK_CLIENT_KEY]

    def setNetworkClient(self,client):
        self.log("gameflowState.setNetworkClient("+str(client)+")")
        self.gameState[flowState.STATE_NETWORK_CLIENT_KEY] = client

    def forceDefaults(self,defaultData):
        self.log("gameflowState.forceDefaults("+str(defaultData)+")")
        self.log("Profile versions do not match! You will need to reconfigure your settings ("+logic.globalDict['version']+": "+defaultData['version']+")")
        logic.globalDict = defaultData
        logic.saveGlobalDict()

    def setSkillLevel(self,skill):
        self.log("gameflowState.setSkillLevel("+str(skill)+")")
        version = "1.2"
        defaultData = {}
        self.log("updating save file")
        defaultData['version'] = version
        defaultData['sceneHistory'] = []
        defaultData['graphics'] = {}
        defaultData['options'] = {}
        defaultData['radio'] = {}
        defaultData['currentProfile'] = 0
        defaultData['profiles'] = []

        defaultProfile = {}
        defaultProfile['username'] = "Unkown Pilot"
        defaultProfile['color'] = [255,255,255]
        defaultProfile["droneSettings"] = {'autoLevel':False,'cameraTilt':40,'thrust':3100,'motorKV':1700,"pDrag":50,"iDrag":50,'batteryCellCount':6,'weight':500, "timeScale":100, 'yawExpo':0.0,'pitchExpo':0.0,'rollExpo':0.0,'pitchRate':100,'rollRate':100,'yawRate':100,'pitchSuperRate':70,'rollSuperRate':70,'yawSuperRate':70}
        defaultProfile['radioSettings'] = {'throttleInverted':False,'yawInverted':False,'pitchInverted':False,'rollInverted':False,'armInverted':True,'resetInverted':False,'yawChannel':1,'pitchChannel':4,'throttleChannel':2,'rollChannel':3,'resetChannel':6,'armChannel':5,'yawOffset':0,'pitchOffset':0,'rollOffset':0,'minThrottle':-32252,'maxThrottle':32252,'minYaw':-32252,'maxYaw':32252,'minPitch':-32252,'maxPitch':32252,'minRoll':-32252,'maxRoll':32252,'minReset':0,'maxReset':32768,'minArm':0,'maxArm':32768,'armSetpoint':0.5,'resetSetpoint':0.5,'dedicatedThrottleStick':True}
        defaultProfile['graphicsSettings'] = {"frameRate":False,"shaders":True,"specularity":True,"shadows":True,"shading":True, "raceLine":False, "aspectRatio4:3":True}

        beginnerProfile = {}
        beginnerProfile['username'] = "Unkown Pilot"
        beginnerProfile['color'] = [255,255,255]
        beginnerProfile["droneSettings"] = {'autoLevel':True,'cameraTilt':30,'thrust':1000,'motorKV':1700,"pDrag":50,"iDrag":50,'batteryCellCount':6,'weight':500, "timeScale":100, 'yawExpo':0.0,'pitchExpo':0.0,'rollExpo':0.0,'pitchRate':50,'rollRate':50,'yawRate':50,'pitchSuperRate':70,'rollSuperRate':70,'yawSuperRate':70}
        beginnerProfile['radioSettings'] = {'throttleInverted':True,'yawInverted':False,'pitchInverted':True,'rollInverted':False,'armInverted':True,'resetInverted':False,'yawChannel':1,'pitchChannel':4,'throttleChannel':2,'rollChannel':3,'resetChannel':6,'armChannel':5,'yawOffset':0,'pitchOffset':0,'rollOffset':0,'minThrottle':-32252,'maxThrottle':32252,'minYaw':-32252,'maxYaw':32252,'minPitch':-32252,'maxPitch':32252,'minRoll':-32252,'maxRoll':32252,'minReset':0,'maxReset':32768,'minArm':0,'maxArm':32768,'armSetpoint':0.5,'resetSetpoint':0.5,'dedicatedThrottleStick':True}
        beginnerProfile['graphicsSettings'] = {"frameRate":False,"shaders":True,"specularity":True,"shadows":True,"shading":True, "raceLine":False, "aspectRatio4:3":False}

        if(skill==0):
            self.log("player is a beginner")
            defaultData['profiles'].append(beginnerProfile)
        else:
            self.log("player is a pro")
            defaultData['profiles'].append(defaultProfile)
        self.forceDefaults(defaultData)
        self.gameState[self.STATE_FIRST_RUN]=False

    def setDefaults(self,skill=1):
        self.log("gameflowState.setDefaults("+str(skill)+")")
        version = "1.4"
        defaultData = {}
        self.log("updating save file")
        defaultData['version'] = version
        defaultData['sceneHistory'] = []
        defaultData['graphics'] = {}
        defaultData['options'] = {}
        defaultData['radio'] = {}
        defaultData['currentProfile'] = 0
        defaultData['profiles'] = []

        defaultProfile = {}
        defaultProfile['username'] = "Unkown Pilot"
        defaultProfile['color'] = [255,255,255]
        defaultProfile["droneSettings"] = {'autoLevel':True,'cameraTilt':40,'thrust':3100,'motorKV':1700,"pDrag":50,"iDrag":50,'batteryCellCount':6,'weight':500,"timeScale":100, 'yawExpo':0.0,'pitchExpo':0.0,'rollExpo':0.0,'pitchRate':100,'rollRate':100,'yawRate':100,'pitchSuperRate':70,'rollSuperRate':70,'yawSuperRate':70}
        defaultProfile['radioSettings'] = {'throttleInverted':False,'yawInverted':False,'pitchInverted':False,'rollInverted':False,'armInverted':True,'resetInverted':False,'yawChannel':1,'pitchChannel':4,'throttleChannel':2,'rollChannel':3,'resetChannel':6,'armChannel':5,'yawOffset':0,'pitchOffset':0,'rollOffset':0,'minThrottle':-32252,'maxThrottle':32252,'minYaw':-32252,'maxYaw':32252,'minPitch':-32252,'maxPitch':32252,'minRoll':-32252,'maxRoll':32252,'minReset':0,'maxReset':32768,'minArm':0,'maxArm':32768,'armSetpoint':0.5,'resetSetpoint':0.5,'dedicatedThrottleStick':True}
        defaultProfile['graphicsSettings'] = {"frameRate":False,"shaders":True,"specularity":True,"shadows":True,"shading":True, "raceLine":False, "aspectRatio4:3":True}

        beginnerProfile = {}
        beginnerProfile['username'] = "Unkown Pilot"
        beginnerProfile['color'] = [255,255,255]
        beginnerProfile["droneSettings"] = {'autoLevel':False,'cameraTilt':30,'thrust':1000,'motorKV':1700,"pDrag":50,"iDrag":50,'batteryCellCount':6,'weight':500,"timeScale":100, 'yawExpo':0.0,'pitchExpo':0.0,'rollExpo':0.0,'pitchRate':50,'rollRate':50,'yawRate':50,'pitchSuperRate':70,'rollSuperRate':70,'yawSuperRate':70}
        beginnerProfile['radioSettings'] = {'throttleInverted':True,'yawInverted':False,'pitchInverted':True,'rollInverted':False,'armInverted':True,'resetInverted':False,'yawChannel':1,'pitchChannel':4,'throttleChannel':2,'rollChannel':3,'resetChannel':6,'armChannel':5,'yawOffset':0,'pitchOffset':0,'rollOffset':0,'minThrottle':-32252,'maxThrottle':32252,'minYaw':-32252,'maxYaw':32252,'minPitch':-32252,'maxPitch':32252,'minRoll':-32252,'maxRoll':32252,'minReset':0,'maxReset':32768,'minArm':0,'maxArm':32768,'armSetpoint':0.5,'resetSetpoint':0.5,'dedicatedThrottleStick':True}
        beginnerProfile['graphicsSettings'] = {"frameRate":False,"shaders":True,"specularity":True,"shadows":True,"shading":True, "raceLine":False}

        if(skill==0):
            self.log("player is a beginner")
            defaultData['profiles'].append(beginnerProfile)
        else:
            self.log("player is a pro")
            defaultData['profiles'].append(defaultProfile)

        #logic.maps = {"
        logic.defaultGameState = {flowState.STATE_FIRST_RUN:False, flowState.STATE_SELECTED_MAP_KEY:"2018 Regional Final.fmp", "notification":{"Text":""}, flowState.STATE_GAME_MODE_KEY:self.GAME_MODE_SINGLE_PLAYER, flowState.STATE_VIEW_MODE_KEY:self.VIEW_MODE_MENU, "track":{"countdownTime":3,"checkpoints":[],"nextCheckpoint":0,"lastCheckpoint":0}, flowState.STATE_PLAYER_DATA_KEY:{flowState.STATE_PLAYER_OBJECT_KEY:None,flowState.STATE_LAP_KEY:0,"checkpoint":0},flowState.STATE_MAP_EDITOR_KEY:None,flowState.STATE_SERVER_IP_KEY:"localhost",flowState.STATE_NETWORK_CLIENT_KEY:None}
        logic.loadGlobalDict()
        firstBoot = (logic.globalDict == {})
        if(firstBoot):
            self.log("this is our first boot")
        else:
            self.log("this isn't our first boot")
        if('version' in logic.globalDict):

            if(logic.globalDict['version']!=defaultData['version']):
                self.forceDefaults(defaultData)
            else:
                self.log("version was in the dict, and the versions matched")
        else:
            logic.globalDict['version'] = "0.0.0"
            self.forceDefaults(defaultData)

        #add any values not in the old save file
        for key, value in defaultData.items():
            if(key in logic.globalDict):
                pass
            else:
                self.log("old save file was missing key "+str(key))
                logic.globalDict[key] = value

        #remove any values in the old save file which are no longer needed
        garbageKeys = []
        for key, value in logic.globalDict.items():
            if(key in defaultData):
                pass
            else:
                self.log("old save file contains deprecated key "+str(key))
                garbageKeys.append(key)
        for key in garbageKeys:
            del logic.globalDict[key]

        logic.globalDict[self.STATE_FIRST_RUN] = firstBoot
        print("first boot = "+str(firstBoot))
