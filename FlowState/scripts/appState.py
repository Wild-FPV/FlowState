import bge
import copy
import os
logic = bge.logic
class appState:
    #moved to game state:SELECTED_MAP_DEFAULT = "2018 Regional Final.fmp"
    #moved to game state: TRACK_DEFAULT = {"countdownTime":3,"checkpoints":[],"nextCheckpoint":0,"lastCheckpoint":0}
    SERVER_IP_DEFAULT = "localhost"
    MAP_EDITOR_DEFAULT = None
    #moved to game state: GAME_MODE_DEFAULT = self.GAME_MODE_SINGLE_PLAYER
    VIEW_MODE_DEFAULT = self.VIEW_MODE_MENU
    NETWORK_CLIENT_DEFAULT = None
    #moved to game state:LAP_DEFAULT = 0
    #moved to game state:CHECKPOINT_DEFAULT = 0
    PLAYER_DATA_DEFAULT = {self.STATE_PLAYER_OBJECT_KEY:None,self.STATE_LAP_KEY:self.LAP_DEFAULT,self.FIRST_CHECKPOINT_KEY:self.CHECKPOINT_DEFAULT}
    PLAYER_OBJECT_DEFAULT = None
    NOTIFICATION_DEFAULT = {"Text":""}
    FIRST_RUN_DEFAULT = True

    #view mode keys
    VIEW_MODE_MENU=0
    VIEW_MODE_PLAY=1

    #game mode keys
    GAME_MODE_EDITOR = 0
    GAME_MODE_SINGLE_PLAYER = 1
    GAME_MODE_MULTIPLAYER = 2

    def __init__(self):
        self.log("appState.init")
        self._selectedMap = SELECTED_MAP_DEFAULT
        self._track = TRACK_DEFAULT
        self._serverIp = SERVER_IP_DEFAULT
        self._mapEditor = MAP_EDITOR_DEFAULT
        self._gameMode = GAME_MODE_DEFAULT
        self._viewMode = VIEW_MODE_DEFAULT
        self._networkClient = NETWORK_CLIENT_DEFAULT
        self._lap = LAP_DEFAULT
        self._playerData = PLAYER_DATA_DEFAULT
        self._playerObject = PLAYER_OBJECT_DEFAULT
        self._notification = NOTIFICATION_DEFAULT
        self._firstRun = FIRST_RUN_DEFAULT

    def printAppeState(self):
        attrs = vars(self)
        print(', '.join("%s: %s" % item for item in attrs.items()))

    def selectMap(self,mapName):
        self._selectedMap = mapName

    def getSelectedMap(self):
        return self._selectedMap

    def setServerIP(self,ip):
        self._serverIp = ip

    def getServerIP(self):
        return self._serverIp

    def setMapEditor(self,mapEditor):
        self._mapEditor = mapEditor

    def getMapEditor(self):
        return self._mapEditor

    def setGameMode(self,mode):
        self._gameMode = mode

    def getGameMode(self):
        return self._gameMode

    def setViewMode(self,mode):
        self._viewMode = mode

    def getViewMode(self):
        return self._viewMode

    def setNetworkClient(self, client):
        self._networkClient = client

    def getNetworkClient(self):
        return self._networkClient

    def setLap()
