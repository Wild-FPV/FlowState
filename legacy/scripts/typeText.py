import bge
render = bge.render
logic = bge.logic
flowState = logic.flowState
cont = logic.getCurrentController()
owner = cont.owner
keyboard = cont.sensors['Keyboard']
blendPath = logic.expandPath("//")
import os
import numpy
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

def saveMapToFile(map,fileName):
    fileName = blendPath+"maps"+os.sep+fileName
    logic.flowState.log("saving map: "+fileName)
    print("saving map to: "+fileName)
    try:
        with open(fileName, 'w+') as saveFile:
            saveFile.write(str(map))
            saveFile.close()
    except Exception as e:
        logic.flowState.log("map save error: "+str(e))
    logic.flowState.log("map save complete: "+fileName)


(pressedKeys,activeKeys,inactiveKeys,releasedKeys) = getKeyStates(keyboard)
enter = bge.events.ENTERKEY in pressedKeys
if(enter):
    scenes = logic.getSceneList()
    currentScene = logic.getCurrentScene()
    for scene in scenes:
        if(scene!=currentScene):
            scene.end()
    render.showMouse(0)
    mapName = str(owner.text)+".fmp"


    map = {"assets":[]}
    saveMapToFile(map,mapName)

    currentScene.replace("Map Editor")
    flowState.selectMap(mapName)
print(pressedKeys)
