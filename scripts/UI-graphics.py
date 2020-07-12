import bge
import traceback
logic = bge.logic
render = bge.render
scene = logic.getCurrentScene()
cont = logic.getCurrentController()
owner = cont.owner
flowState = logic.flowState
UI = bge.UI
textColor = [1,1,1,1]
blockColor = flowState.menuButtonColor
flowState = logic.flowState

graphicsSettings = flowState.getGraphicsSettings()

def settingsAction(key,value):
    print(key,value)
    setattr(graphicsSettings,key,value)

def applySettings():
    flowState.saveSettings()
    if(flowState.getGameMode()!=flowState.GAME_MODE_MULTIPLAYER):
        logic.restartGame()
    else:
        backAction()

def spawnBoolRow(label,height,key,action):

    rowBox = UI.BoxElement(window,[50,height],11,0.5, blockColor, 5)
    titleText = UI.TextElement(window,[rowBox.position[0]-30,rowBox.position[1]], textColor, 4, label)

    box = UI.BoxElement(window,[80,height],1,0.5, blockColor, 1)
    text = UI.TextElement(window,[box.position[0],box.position[1]], textColor, 0, "INVERTED")
    button = UI.UIButton(text,box,settingsAction,key)

    #indicatorText = UI.TextElement(window,[50,height], textColor, 0, "0")
    #def __init__(textElement,boxElement,action,key=None,value=None):
    invertedBooleanButton = UI.UIBooleanInput(button,text,getattr(graphicsSettings,key))
    return invertedBooleanButton

def backAction():
    bge.logic.sendMessage("cam1")
    currentScene = logic.getCurrentScene()
    sceneHistory = flowState.sceneHistory
    print(sceneHistory)
    backScene = sceneHistory[-2]
    removedScene = sceneHistory.pop(-1)
    removedScene = sceneHistory.pop(-1)
    print("removing scene "+str(removedScene))
    currentScene.replace(backScene)

if(owner['init']!=True):
    flowState.setViewMode(flowState.VIEW_MODE_MENU)
    flowState.sceneHistory.append(logic.getCurrentScene().name)
    owner['init'] = True
    window = UI.Window()

    inset = 0.2

    mainMenuBlock = UI.BoxElement(window,[50,95],11,1, blockColor, 1)
    mainMenuText = UI.TextElement(window,mainMenuBlock.position, textColor, 0, "GRAPHIC")

    advancedGrass = spawnBoolRow("Advanced Grass",30,"advancedGrass",settingsAction)
    shaders = spawnBoolRow("Filters",40,"shaders",settingsAction)
    specularity = spawnBoolRow("Specularity",50,"specularity",settingsAction)
    shadows = spawnBoolRow("Shadows",60,"shadows",settingsAction)
    shading = spawnBoolRow("Shading",70,"shading",settingsAction)
    raceLine = spawnBoolRow("Race Line",80,"raceLine",settingsAction)
    aspectRatio = spawnBoolRow("Aspect Ratio (4:3)",20,"aspectRatio4x3",settingsAction)

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
