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
    channelKeyStates = {1:bge.events.ONEKEY in pressedKeys, 2:bge.events.TWOKEY in pressedKeys, 3:bge.events.THREEKEY in pressedKeys, 4:bge.events.FOURKEY in pressedKeys, 5:bge.events.FIVEKEY in pressedKeys, 6:bge.events.SIXKEY in pressedKeys, 7:bge.events.SEVENKEY in pressedKeys, 8:bge.events.EIGHTKEY in pressedKeys, 9:bge.events.NINEKEY in pressedKeys}
    rankKeyStates = {1:bge.events.PAD1 in pressedKeys, 2:bge.events.PAD2 in pressedKeys, 3:bge.events.PAD3 in pressedKeys, 4:bge.events.PAD4 in pressedKeys, 5:bge.events.PAD5 in pressedKeys, 6:bge.events.PAD6 in pressedKeys, 7:bge.events.PAD7 in pressedKeys, 8:bge.events.PAD8 in pressedKeys}
    debugKeyState = bge.events.ZEROKEY in pressedKeys
    shiftKeyState = bge.events.LEFTSHIFTKEY in activeKeys
    #OSDToggleKeyState = bge.events.ACCENTGRAVEKEY in pressedKeys
    OSDToggleKeyState = bge.events.BACKSPACEKEY in pressedKeys
    receiver = flowState.getRFEnvironment().getReceiver()
    if(debugKeyState):
        flowState.getRFEnvironment().printRFState()
        #toggle spectating
        flowState.getRFEnvironment().getReceiver().setSpectating(not flowState.getRFEnvironment().getReceiver().isSpectating())

    if(OSDToggleKeyState):
        flowState.getGraphicsSettings().OSDEnabled = not flowState.getGraphicsSettings().OSDEnabled
        print("Show OSD = "+str(flowState.getGraphicsSettings().OSDEnabled))
    if(receiver!=None):
        if(receiver.isSpectating()):
            logic.sendMessage("disable shaders")
            print("disable shaders")
        else:
            print("we aren't spectating")
            if(flowState.getGraphicsSettings().getShaders()):
                logic.sendMessage("enable shaders")
                print("enable shaders")


    if(pressedKeys!=[]):
        flowState.log("player is changing channel")
        #handle any channel key changes
        for index in channelKeyStates:
            keyPressed = channelKeyStates[index]
            if(keyPressed):
                flowState.getRFEnvironment().getReceiver().setChannel(index-1)
                #if(flowState.getGameMode()!=flowState.GAME_MODE_SINGLE_PLAYER):
                if(shiftKeyState): #shift modifier is happening
                    print("also setting quad channel")
                    try:
                        print("setting player vtx "+str(logic.player.name))
                        vtx = logic.player['camera']['vtx']
                        vtx.setFrequency(flowState.getRFEnvironment().getReceiver().getFrequency())
                        flowState.setInitialVTXChannel(index-1)
                    except Exception as e:
                        print(e)

                print("setting channel number to "+str(index))
                break
                #loadMultiplayerServer(serverIP)
        #handle any rank key changes
        for index in rankKeyStates:
            keyPressed = rankKeyStates[index]
            if(keyPressed):
                ranks = flowState.getRaceState().getPlayerRanks()
                print(ranks)
                flowState.getRFEnvironment().getReceiver().setFrequency(ranks[index-1])
                break
                #loadMultiplayerServer(serverIP)
def main():
    keyboard = cont.sensors['channelButtons']
    handleUserInputs(keyboard)
main()
