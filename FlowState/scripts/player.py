import bge
import copy
import os
logic = bge.logic
class player:
    def __init__(self):
        self.log("player.init")
        self._lap = 0
        self._currentCheckpoint = 0
        self._nextCheckpoint = 0
        self._lastCheckpoint = 0
        self._playerObject = None
        self._fpvModel = None

    def getLap(self):
        return self._lap

    def setLap(self,lap):
        self._lap = lap

    def getCurrentCheckpoint(self):
        return self._currentCheckpoint

    def setCurrentCheckpoint(self,currentCheckpoint):
        self._currentCheckpoint = currentCheckpoint

    def getNextCheckpoint(self):
        return self._nextCheckpoint

    def setNextCheckpoint(self,nextCheckpoint):
        self._nextCheckpoint = nextCheckpoint

    def getLastCheckpoint(self):
        return self._lastCheckpoint

    def setLastCheckpoint(self,lastCheckpoint):
        self._lastCheckpoint = lastCheckpoint

    def getPlayerObject(self):
        return self._playerObject

    def setPlayerObject(self,playerObject):
        self._playerObject = playerObject

    def getDrone(self):
        return self._drone

    def setDrone(self,drone):
        self._drone = drone
