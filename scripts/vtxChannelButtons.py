import bge
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
    channelKeyStates = {1:bge.events.ONEKEY in pressedKeys, 2:bge.events.TWOKEY in pressedKeys, 3:bge.events.THREEKEY in pressedKeys, 4:bge.events.FOURKEY in pressedKeys, 5:bge.events.FIVEKEY in pressedKeys, 6:bge.events.SIXKEY in pressedKeys, 7:bge.events.SEVENKEY in pressedKeys, 8:bge.events.EIGHTKEY in pressedKeys}
    debugKeyState = bge.events.ZEROKEY in pressedKeys

    if(debugKeyState):
        flowState.getRFEnvironment().printRFState()
        #toggle spectating
        flowState.getRFEnvironment().getReceiver().setSpectating(not flowState.getRFEnvironment().getReceiver().isSpectating())

    if(flowState.getRFEnvironment().getReceiver().isSpectating()):
        logic.sendMessage("disable shaders")
        print("disable shaders")
    else:
        print("we aren't spectating")
        if(flowState.getGraphicsSettings().getShaders()):
            logic.sendMessage("enable shaders")
            print("enable shaders")


    if(pressedKeys!=[]):
        flowState.log("player is changing channel")
        for index in channelKeyStates:
            keyPressed = channelKeyStates[index]
            if(keyPressed):
                flowState.getRFEnvironment().getReceiver().setChannel(index-1)
                if(flowState.getGameMode()!=flowState.GAME_MODE_SINGLE_PLAYER):
                    try:
                        print("setting player vtx "+str(logic.player.name))
                        vtx = logic.player['camera']['vtx']
                        vtx.setFrequency(flowState.getRFEnvironment().getReceiver().getFrequency())
                    except Exception as e:
                        print(e)

                print("setting channel number to "+str(index))
                break
                #loadMultiplayerServer(serverIP)
def main():
    keyboard = cont.sensors['channelButtons']
    handleUserInputs(keyboard)
main()
