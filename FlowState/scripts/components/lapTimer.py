import bge
import time
from collections import OrderedDict
import FSNObjects

if not hasattr(bge, "__component__"):
    render = bge.render
    logic = bge.logic
    flowState = logic.flowState

class LapTimer(bge.types.KX_PythonComponent):
    args = OrderedDict([
        #("Power Output (mw)", 25),
        #("Pit Mode",False),
        #("Frequency", raceband[0])
    ])

    def start(self, args):
        flowState.debug("lapTimer: start("+str(args)+")")
        self.timeline = {}

    def addTimelineEvent(self,event):
        eventTime = time.time()
        self.timeline[eventTime] = event
        return self.timeline

    def registerLap(self):
        gatePass = {"channel":1, "time":time.time()}
        gatePassEvent = FSNObjects.PlayerEvent(FSNObjects.PlayerEvent.PLAYER_MESSAGE,flowState.getNetworkClient().clientID,gatePass)
        if(flowState.getGameMode()==flowState.GAME_MODE_MULTIPLAYER):
            flowState.debug("sending gate pass event")
            flowState.getNetworkClient().sendEvent(gatePassEvent)
        addTimelineEvent(gatePassEvent)

    def update(self):
        if(playerPass==True):
