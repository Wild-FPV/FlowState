import bge
import copy
import os
import traceback
from scripts.abstract.settings.DroneSettings import DroneSettings
from scripts.abstract.settings.RadioSettings import RadioSettings
from scripts.abstract.settings.GraphicsSettings import GraphicsSettings
from scripts.abstract.RFEnvironment import RFEnvironment
logic = bge.logic
render = bge.render

class FlowState:
    #the version of the save data format
    VERSION = "1.0.0"

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

    #game modes
    GAME_MODE_EDITOR = 0
    GAME_MODE_SINGLE_PLAYER = 1
    GAME_MODE_MULTIPLAYER = 2
    GAME_MODE_TEAM_RACE = 3

    #view modes
    VIEW_MODE_MENU=0
    VIEW_MODE_PLAY=1

    #log levels
    LOG_LEVEL_DEBUG = 0
    LOG_LEVEL_INFO = 1
    LOG_LEVEL_ERROR = 2

    #map load stages
    MAP_LOAD_STAGE_NONE = -1
    MAP_LOAD_STAGE_LOADING = 0
    MAP_LOAD_STAGE_DONE = 1

    LOG_LEVEL = LOG_LEVEL_INFO

    def __init__(self):
        self.__logFile = os.path.join(str(logic.expandPath("//")),"flowstate.log") #remove once propper logging is implemented

        self.log("FlowState.init()")
        self._version = self.VERSION
        self._timeLimit = 120
        self._checkpoints = []
        self._selectedMap = "2018 Regional Final.fmp"
        self._player = None #needs to be implemented
        self._HUDController = None #needs to be implemented
        self._gameMode = self.GAME_MODE_SINGLE_PLAYER
        self._mapEditor = None

        self._networkClient = None
        self._notification = {"Text":""}
        self._viewMode = self.VIEW_MODE_MENU
        self._isFirstRun = True
        self.mapLoadStage = self.MAP_LOAD_STAGE_LOADING
        self.sceneHistory = []
        self.track = {"launchPads":[], "startFinishPlane":None,"countdownTime":3,"checkpoints":[],"nextCheckpoint":0,"lastCheckpoint":0}
        self._serverIP = "localhost"
        self._serverPort = 50002
        self.lastId = 0

        self._rfEnvironment = RFEnvironment(self)
        self._droneSettings = DroneSettings(self)
        self._radioSettings = RadioSettings(self)
        self._graphicsSettings = GraphicsSettings(self)
        self._networkClient = None
        self.menuButtonColor = [0.3,0.3,0.3,0.6]

    #eventually we should implement propper logging
    def debug(self,output):
        output = str(output)
        if(self.LOG_LEVEL<=self.LOG_LEVEL_DEBUG):
            print("DEBUG: "+output)

    def log(self,output):
        output = str(output) #let's make sure that output is actually a string
        if(self.LOG_LEVEL<=self.LOG_LEVEL_INFO):
            print("LOG: "+output) #let's print it to the console
        with open(self.__logFile, 'a+') as saveFile: #let's write it to the log file
            saveFile.write(str(output)+"\n")
            saveFile.close()

    def error(self,output):
        output = str(output)

        if(self.LOG_LEVEL<=self.LOG_LEVEL_ERROR):
            print("ERROR: "+output)
        traceback.print_exc()
        with open(self.__logFile, 'a+') as saveFile:
            saveFile.write(str(output)+"\n")
            saveFile.close()

    def loadSaveSettings(self):
        saveDict = logic.globalDict
        #first let's determin if this is the first time the game is being booted
        self._isFirstRun = (logic.globalDict == {})
        if(self._isFirstRun): #let's handle the first boot
            self.log("FlowState.loadSaveSettings: this is our first boot")

            droneSettings = {}
            radioSettings = {}
            graphicsSettings = {}

        else: #let's handle a returning user
            self.log("FlowState.loadSaveSettings: this isn't our first boot")

            #Let's load graphics settings
            profileIndex = 0#saveDict['currentProfile'] #let's get the index of the last user we were using
            profiles = saveDict['profiles'] #
            profile = profiles[profileIndex]

            #let's get the various settings for the profile
            droneSettings = profile['droneSettings']
            radioSettings = profile['radioSettings']
            graphicsSettings = profile['graphicsSettings']

        #read in the graphics settings
        self._graphicsSettings = GraphicsSettings(self, **graphicsSettings)

        #read in the drone settings
        self._droneSettings = DroneSettings(self, **droneSettings)

        #read in the radio settings
        self._radioSettings = RadioSettings(self, **radioSettings)

        if(self._isFirstRun): #if this is our first run, create a save file
            self.saveSettings()

    def saveSettings(self):
        self.debug("FlowState.saveSettings()")
        #let's serialized versions of each of our settings
        serializedDroneSettings = self._droneSettings.getSerializedSettings()
        serializedRadioSettings = self._radioSettings.getSerializedSettings()
        serializedGraphicsSettings = self._graphicsSettings.getSerializedSettings()

        #let's define the structure for our save data
        saveData = {}
        saveData['version'] = self._version
        saveData['currentProfile'] = 0
        saveData['profiles'] = [{"droneSettings":serializedDroneSettings,"radioSettings":serializedRadioSettings,"graphicsSettings":serializedGraphicsSettings}]
        logic.globalDict = saveData
        logic.saveGlobalDict() #save the file to the disk

    def setEasyDefaults(self):
        #change the settings to something more appropriate for newbs
        self._droneSettings.setEasyDefaults()
        self._radioSettings.setEasyDefaults()

    def resetGameState(self):
        history = copy.deepcopy(self.sceneHistory)
        self.__init__()
        self.sceneHistory = history #we don't typically want the scene history to be reset
        self.loadSaveSettings()

    def getRFEnvironment(self):
        return self._rfEnvironment

    def addRFEmitter(self,emitter):
        self._rfEnvironment.addEmitter(emitter)

    def removeRFEmitter(self,emitter):
        self._rfEnvironment.removeEmitter(emitter)

    def addRFReceiver(self,receiver):
        self._rfEnvironment.addReceiver(receiver)

    def removeRFReceiver(self,receiver):
        self._rfEnvironment.removeReceiver(receiver)

    def updateRFEnvironment(self, noiseFloor):
        self._rfEnvironment.update(noiseFloor)

    def resetRFEnvironment(self):
        self._rfEnvironment = RFEnvironment(self)

    def addMetadata(self,asset):
        self.log("mapEditor.addMetadata("+str(asset)+")")
        asset['metadata'] = {}
        if 'gate' in asset.name:
            asset['metadata'] = copy.deepcopy(self.METADATA_GATE)

        if 'checkpoint' in asset.name:
            asset['metadata'] = copy.deepcopy(self.METADATA_CHECKPOINT)
        asset['metadata']['id'] = self.getNewID()

    def getNewID(self):
        self.lastId+=1
        return self.lastId

    def getTimeLimit(self):
        return self._timeLimit

    def setTimeLimit(self,timeLimit):
        self._timeLimit = timeLimit

    def getCheckpoints(self):
        return self._checkpoints

    def setCheckpoints(self,checkpoints):
        self._checkpoints = checkpoints

    def getSelectedMap(self):
        return self._selectedMap

    def selectMap(self,selectedMap):
        self._selectedMap = selectedMap

    def getPlayer(self):
        return self._player

    def setPlayer(self,player):
        self._player = player

    def getHUDController(self):
        return self._HUDController

    def setHUDController(self,HUDController):
        self._HUDController = HUDController

    def getGameMode(self):
        return self._gameMode

    def setGameMode(self,gameMode):
        self.log("setting game mode "+str(gameMode))
        self._gameMode = gameMode

    def getMapEditor(self):
        return self._mapEditor

    def setMapEditor(self,mapEditor):
        self._mapEditor = mapEditor

    def getServerIp(self):
        return self._serverIp

    def setServerIp(self,serverIp):
        self._serverIp = serverIp

    def getServerPort(self):
        return self._serverPort

    def setServerPort(self,serverPort):
        self._serverPort = serverPort

    def getNetworkClient(self):
        return self._networkClient

    def setNetworkClient(self,networkClient):
        self._networkClient = networkClient

    def getNotification(self):
        return self._notification

    def setNotification(self,notification):
        self._notification = notification

    def getViewMode(self):
        return self._viewMode

    def setViewMode(self,viewMode):
        print("FlowState.setViewMode("+str(viewMode)+")")
        if viewMode == self.VIEW_MODE_MENU:
            render.showMouse(1)
        if viewMode == self.VIEW_MODE_PLAY:
            render.showMouse(0)
        self._viewMode = viewMode

    def isFirstRun(self):
        return self._isFirstRun

    def getDroneSettings(self):
        return self._droneSettings

    def getRadioSettings(self):
        return self._radioSettings

    def getGraphicsSettings(self):
        return self._graphicsSettings

    def getNetworkClient(self):
        return self._networkClient

    def setNetworkClient(self,client):
        self._networkClient = client

    def getServerIP(self):
        return self._serverIP

    def setServerIP(self,ip):
        self._serverIP = ip
