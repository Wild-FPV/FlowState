import bge
import traceback
logic = bge.logic
render = bge.render
scene = logic.getCurrentScene()
cont = logic.getCurrentController()
owner = cont.owner
UI = bge.UI
flowState = logic.flowState

textColor = [1,1,1,1]
blockColor = flowState.menuButtonColor
droneSettings = flowState.getDroneSettings()
def soloGameAction():
    scenes = logic.getSceneList()
    currentScene = logic.getCurrentScene()
    for scene in scenes:
        if(scene!=currentScene):
            scene.end()
    currentScene.replace("main regional finals")

def graphicsAction():
    pass

def setThrustAction():
    flowState.getDroneSettings().thrust = thrustInput.value
    bge.logic.sendMessage("loadNewSettings")

def setWeightAction():
    flowState.getDroneSettings().weight = int(weightInput.value)
    bge.logic.sendMessage("loadNewSettings")

def setCameraTiltAction():
    print("UI camera tilt action")
    flowState.getDroneSettings().cameraTilt = int(camTiltInput.value)
    bge.logic.sendMessage("loadNewSettings")

def setSlowMoAction():
    flowState.getDroneSettings().timeScale = int(slowMo.value)
    bge.logic.sendMessage("loadNewSettings")

def setMotorKVAction():
    flowState.getDroneSettings().pDrag = int(motorKVmInput.value)
    bge.logic.sendMessage("loadNewSettings")

def setCellCountAction():
    flowState.getDroneSettings().iDrag = int(cellCountInput.value)
    bge.logic.sendMessage("loadNewSettings")

def applySettings():
    scenes = logic.getSceneList()
    currentScene = logic.getCurrentScene()
    flowState.saveSettings()
    for scene in scenes:
        if(scene!=currentScene):
            if(scene.name == "Main Game"):
                print(flowState.getGameMode())
                #if(flowState.getGameMode()==flowState.GAME_MODE_MULTIPLAYER):
                #    print("WE ARE IN MULTIPLAYER!!!! DONT RESTART")
                #else:
                #    currentMap = logic.flowState.getSelectedMap()
                #    logic.flowState.resetGameState()
                #    logic.flowState.selectMap(currentMap)
                #    #scene.restart()
                #    print("WE ARE IN SINGLE!!!! COOL TO RESTART")
    backAction()

def backAction():
    currentScene = logic.getCurrentScene()
    sceneHistory = flowState.sceneHistory
    print(sceneHistory)
    backScene = sceneHistory[-2]
    removedScene = sceneHistory.pop(-1)
    removedScene = sceneHistory.pop(-1)
    print("removing scene "+str(removedScene))
    currentScene.replace(backScene)

def settingsAction(key,value): #we need to find a better way of doing this in the future
    droneSettings.__dict__[key] = value

def spawnSetting(label,height,key,action,min,max,increment):
    logic.flowState.debug("UI-settingsDrone.spawnSetting("+label+","+str(height)+","+str(key)+","+str(action)+","+str(min)+","+str(max)+","+str(increment)+")")
    itemRow = UI.BoxElement(window,[50,height],11,0.5, blockColor, 5)
    itemText = UI.TextElement(window, [itemRow.position[0]-30,itemRow.position[1]], textColor, 4, label)

    itemUpBox = UI.BoxElement(window,[60,height],0.5,0.5, blockColor, 1)
    itemUpText = UI.TextElement(window,itemUpBox.position, textColor, 0, "+")
    itemUpButton = UI.UIButton(itemUpText,itemUpBox,action)

    itemDownBox = UI.BoxElement(window,[45,height],0.5,0.5, blockColor, 1)
    itemDownText = UI.TextElement(window,itemDownBox.position, textColor, 0, "-")
    itemDownButton = UI.UIButton(itemDownText,itemDownBox,action)

    currentItemText = UI.TextElement(window,[50,height], textColor, 0, "")
    print(droneSettings.getSerializedSettings())
    value = int(droneSettings.__dict__[str(key)])
    return UI.UINumberInput(itemUpButton,itemDownButton,currentItemText,value,min, max, increment)

def spawnBoolRow(label,height,key,action):

    rowBox = UI.BoxElement(window,[50,height],11,0.5, blockColor, 5)
    titleText = UI.TextElement(window,[rowBox.position[0]-30,rowBox.position[1]], textColor, 4, label)

    box = UI.BoxElement(window,[47.5,height],1,0.5, blockColor, 1)
    text = UI.TextElement(window,[box.position[0],box.position[1]], textColor, 0, "INVERTED")
    button = UI.UIButton(text,box,settingsAction,key)
    invertedBooleanButton = UI.UIBooleanInput(button,text,droneSettings.__dict__[key])
    return invertedBooleanButton

if(owner['init']!=True):
    flowState.setViewMode(flowState.VIEW_MODE_MENU)
    flowState.sceneHistory.append(logic.getCurrentScene().name)
    owner['init'] = True
    window = UI.Window()

    pageHeaderBlock = UI.BoxElement(window,[50,95],11,1, blockColor, 5)
    pageHeaderText = UI.TextElement(window,pageHeaderBlock.position, textColor, 4, "GAME SETTINGS MENU")

    camTiltInput = spawnSetting("CAMERA TILT (DEGREES)",80,"cameraTilt",setCameraTiltAction,0,90,1)
    thrustInput = spawnSetting("STATIC THRUST (GRAMS)",70,"thrust",setThrustAction,0,10000,50)
    weightInput = spawnSetting("ALL UP WEIGHT (GRAMS)",60,"weight",setWeightAction,1,2000,10)
    motorKVmInput = spawnSetting("DRAG",50,"pDrag",setMotorKVAction,0,100,1)
    cellCountInput = spawnSetting("LIFT / DOWNFORCE",40,"iDrag",setCellCountAction,0,100,1)
    slowMo = spawnSetting("SIM SPEED PERCENT",30,"timeScale",setSlowMoAction,1,100,1)
    autoLevel = spawnBoolRow("Auto Level",20,"autoLevel",settingsAction)

    #back button
    backBlockElement = UI.BoxElement(window,[10,10],1,.5, blockColor, 1)
    backText = UI.TextElement(window,backBlockElement.position, textColor, 0, "BACK")
    backButton = UI.UIButton(backText,backBlockElement,backAction)

    #apply button
    applyBox = UI.BoxElement(window,[90,10],1,.5, blockColor, 1)
    applyText = UI.TextElement(window,applyBox.position, textColor, 0, "APPLY")
    applyButton = UI.UIButton(applyText,applyBox,applySettings)

else:
    try:
        UI.run(cont)
    except Exception as e:
        flowState.error(traceback.format_exc())
        owner['init'] = -1
