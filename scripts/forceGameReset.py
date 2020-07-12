import bge
import FSNObjects
import time
logic = bge.logic
flowState = logic.flowState
render = bge.render
scene = logic.getCurrentScene()
cont = logic.getCurrentController()
owner = cont.owner
def getKeyStates(keyboard):

    pressedKeys = []
    activeKeys = []
    inactiveKeys = []
    releasedKeys = []
    for event in keyboard.events:
        if(event[1] == bge.logic.KX_SENSOR_JUST_ACTIVATED):
            pressedKeys.append(event[0])
        if(event[1] == bge.logic.KX_SENSOR_ACTIVE):
            activeKeys.append(event[0])
        if(event[1] == bge.logic.KX_SENSOR_INACTIVE ):
            inactiveKeys.append(event[0])
        if(event[1] == bge.logic.KX_SENSOR_JUST_DEACTIVATED ):
            releasedKeys.append(event[0])
    return (pressedKeys,activeKeys,inactiveKeys,releasedKeys)

def handleUserInputs(keyboard):
    (pressedKeys,activeKeys,inactiveKeys,releasedKeys) = getKeyStates(keyboard)
    enter = bge.events.SPACEKEY in pressedKeys
    if(pressedKeys!=[]):
        print("reset "+str(enter))
        if(enter):
            #if(flowState.getGameMode()==flowState.GAME_MODE_TEAM_RACE):
            flowState.log("resetting multiplayer game")
            resetEvent = FSNObjects.PlayerEvent(FSNObjects.PlayerEvent.PLAYER_RESET,flowState.getNetworkClient().clientID,{"reset":time.time()+10})
            flowState.getNetworkClient().sendEvent(resetEvent)
            print("sending reset message")
            owner['canReset'] = False
def main():
    keyboard = cont.sensors['gameResetButton']
    handleUserInputs(keyboard)
main()
