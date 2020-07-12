import bge
import time
from scripts.abstract.RaceFormat import RaceFormat
logic = bge.logic
render = bge.render
class TrackState:
    EVENT_LAP = 0
    EVENT_RACE_FINISH = 1
    EVENT_HOLE_SHOT = 2
    EVENT_CHECKPOINT_COLLECT = 3
    def __init__(self,flowState):
        flowState.debug("TrackState.init()")
        self.flowState = flowState
        self.launchPads = []
        self.checkpoints = []
        self.lastCheckpoint = 0

    def getLastCheckpoint(self):
        return self.lastCheckpoint

    def setLastCheckpoint(self,lastCheckpoint):
        self.flowState.debug("setLastCheckpoint("+str(lastCheckpoint)+")")
        self.lastCheckpoint = lastCheckpoint
