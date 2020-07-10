import bge
import traceback
logic = bge.logic
render = bge.render
scene = logic.getCurrentScene()
cont = logic.getCurrentController()
owner = cont.owner
flowState = logic.flowState
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

#rate actions
def setYawRateAction():
    flowState.getDroneSettings().yawRate = yawRateInput.value

def setRollRateAction():
    flowState.getDroneSettings().rollRate = rollRateInput.value

def setPitchRateAction():
    flowState.getDroneSettings().pitchRate = pitchRateInput.value

#expo actions
def setYawExpoAction():
    flowState.getDroneSettings().yawExpo = yawExpoInput.value

def setRollExpoAction():
    flowState.getDroneSettings().rollExpo = rollExpoInput.value

def setPitchExpoAction():
    flowState.getDroneSettings().pitchExpo = pitchExpoInput.value

#super rate actions
def setYawSuperRateAction():
    flowState.getDroneSettings().yawSuperRate = yawSuperRateInput.value

def setRollSuperRateAction():
    flowState.getDroneSettings().rollSuperRate = rollSuperRateInput.value

def setPitchSuperRateAction():
    flowState.getDroneSettings().pitchSuperRate = pitchSuperRateInput.value

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
    print(sceneHistory)
    removedScene = sceneHistory.pop(-1)
    removedScene = sceneHistory.pop(-1)
    print("removing scene "+str(removedScene))
    currentScene.replace(backScene)

def spawnRateInput(label,height,channelKey,action,min,max,increment):

    rowBox = UI.BoxElement(window,[50,height],11,0.5, blockColor, 5)
    titleText = UI.TextElement(window,[rowBox.position[0]-35,rowBox.position[1]], textColor, 4, label)


    increaseBox = UI.BoxElement(window,[57,height],0.5,0.5, blockColor, 1)
    increaseText = UI.TextElement(window,increaseBox.position, textColor, 0, "+")
    increaseButton = UI.UIButton(increaseText,increaseBox,action)


    decreaseBox = UI.BoxElement(window,[45,height],0.5,0.5, blockColor, 1)
    decreaseText = UI.TextElement(window, decreaseBox.position, textColor, 0, "-")
    decreaseButton = UI.UIButton(decreaseText,decreaseBox,action)

    indicatorText = UI.TextElement(window,[50,height], textColor, 0, "0")
    print("spawning "+str(channelKey)+" "+str(getattr(droneSettings,channelKey)))
    channelInput = UI.UINumberInput(increaseButton,decreaseButton,indicatorText,int(getattr(droneSettings,channelKey)),min,max,increment)

    return channelInput

if(owner['init']!=True):
    flowState.setViewMode(flowState.VIEW_MODE_MENU)
    flowState.sceneHistory.append(logic.getCurrentScene().name)
    droneSettings = flowState.getDroneSettings()
    owner['init'] = True
    window = UI.Window()

    inset = 0.2

    pageHeaderBlock = UI.BoxElement(window,[50,95],11,1, blockColor, 5)
    pageHeaderText = UI.TextElement(window,pageHeaderBlock.position, textColor, 4, "GAME SETTINGS MENU")
    bHeight = 80
    yawRateInput = spawnRateInput("YAW RATE",bHeight,"yawRate",setYawRateAction,0,200,1)
    bHeight -= 7
    pitchRateInput = spawnRateInput("PITCH RATE",bHeight,"pitchRate",setPitchRateAction,0,200,1)
    bHeight -= 7
    rollRateInput = spawnRateInput("ROLL RATE",bHeight,"rollRate",setRollRateAction,0,200,1)
    bHeight -= 7

    yawSuperRateInput = spawnRateInput("YAW SUPER RATE",bHeight,"yawSuperRate",setYawSuperRateAction,0,100,1)
    bHeight -= 7
    pitchSuperRateInput = spawnRateInput("PITCH SUPER RATE",bHeight,"pitchSuperRate",setPitchSuperRateAction,0,100,1)
    bHeight -= 7
    rollSuperRateInput = spawnRateInput("ROLL SUPER RATE",bHeight,"rollSuperRate",setRollSuperRateAction,0,100,1)
    bHeight -= 7

    yawExpoInput = spawnRateInput("YAW EXPO",bHeight,"yawExpo",setYawExpoAction,0,100,1)
    bHeight -= 7
    pitchExpoInput = spawnRateInput("PITCH EXPO",bHeight,"pitchExpo",setPitchExpoAction,0,100,1)
    bHeight -= 7
    rollExpoInput = spawnRateInput("ROLL EXPO",bHeight,"rollExpo",setRollExpoAction,0,100,1)

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
        flowState.log(traceback.format_exc())
        owner['init'] = -1
