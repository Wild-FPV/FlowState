import bge
import math
import traceback
import types
logic = bge.logic
flowState = logic.flowState
render = bge.render

scene = logic.getCurrentScene()
cont = logic.getCurrentController()
owner = cont.owner
flowState = logic.flowState
UI = bge.UI

textColor = [1,1,1,1]
blockColor = flowState.menuButtonColor

if "window" not in owner:
    owner['window'] = UI.Window()

window = owner['window']

def playAction():
    mapName = "custom.fmp"
    scenes = logic.getSceneList()
    currentScene = logic.getCurrentScene()
    for scene in scenes:
        if(scene!=currentScene):
            scene.end()
    flowState.selectMap(mapName)
    logic.flowState.GAME_MODE_SINGLE_PLAYER
    currentScene.replace("Main Game")


def saveAction():
    logic.sendMessage("saveMap")
    logic.flowState.getMapEditor().setMode(logic.flowState.VIEW_MODE_PLAY)

def toggleUnitsAction():
    print("toggleUnitsAction()")
    logic.flowState.getMapEditor().toggleUnits()
    print(logic.flowState.getMapEditor().unitsMetric)

def mainMenuAction():
    scenes = logic.getSceneList()
    currentScene = logic.getCurrentScene()
    for scene in scenes:
        if(scene!=currentScene):
            scene.end()
    logic.flowState.resetGameState()

    currentScene.replace("Menu Background")

def helpAction():
    currentScene = logic.getCurrentScene()
    currentScene.replace("UI-editor-help")

def inputAction(key,value):
    logic.flowState.getMapEditor().applyMetadata(key,value)

def noAction():
    print("no action")

def quitGameAction():
    logic.flowState.getMapEditor().setMode(logic.flowState.VIEW_MODE_PLAY)

def resumeAction():
    logic.flowState.getMapEditor().setMode(logic.flowState.VIEW_MODE_PLAY)

def buildBooleanInput(baseId, window, label, value,position, action):
    flowState.debug("UI-EditorMenu.buildBooleanInput with label "+str(label))
    height = position[1]
    width = position[0]
    pos = [62.5,90.5]
    #text indicating what the value of the metadata field is
    indicatorText = UI.TextElement(window,[65+width,height], textColor, 0, str(value))

    #button to decrease the value of the metadata field
    decreaseBox = UI.BoxElement(window,[55+width,height],0.5,0.5, blockColor, 1)
    decreaseText = UI.TextElement(window, decreaseBox.position, textColor, value, "/")
    decreaseButton = UI.UIButton(decreaseText,decreaseBox,action,label)

    #tie the buttons together in order to handle the input
    UI.UIBooleanInput(decreaseButton,indicatorText,value)

    #add the items to the window to be handled each game frame
    window.add(label+"ToggleBox",decreaseBox)
    window.add(label+"ToggleText",decreaseText)
    window.add(label+"ToggleButton",decreaseButton)

def buildIntegerInput(baseId, window, label, value, position, action, min, max, increment):
    flowState.debug("UI-EditorMenu.buildIntegerInput with label "+str(label))
    height = position[1]
    width = position[0]
    pos = [62.5,90.5]
    #text indicating what the value of the metadata field is
    indicatorText = UI.TextElement(window,[60+width,height], textColor, 0, str(value))

    #button to increase the value of the metadata field
    increaseBox = UI.BoxElement(window,[67+width,height],0.5,0.5, blockColor, 1)
    increaseText = UI.TextElement(window,increaseBox.position, textColor, value, "+")
    increaseButton = UI.UIButton(increaseText,increaseBox,action,label)

    #button to decrease the value of the metadata field
    decreaseBox = UI.BoxElement(window,[55+width,height],0.5,0.5, blockColor, 1)
    decreaseText = UI.TextElement(window, decreaseBox.position, textColor, value, "-")
    decreaseButton = UI.UIButton(decreaseText,decreaseBox,action,label)

    #tie the buttons together in order to handle the input
    UI.UINumberInput(increaseButton,decreaseButton, indicatorText,value,min,max)

    #add the items to the window to be handled each game frame
    owner['window'].add(label+"IndicatorText",indicatorText)
    window.add(baseId+"IncreaseBox",increaseBox)
    window.add(baseId+"IncreaseText",increaseText)
    window.add(baseId+"IncreaseButton",increaseButton)
    window.add(label+"DecreaseBox",decreaseBox)
    window.add(label+"DecreaseText",decreaseText)
    window.add(label+"DecreaseButton",decreaseButton)

def spawnMetadataInput(window,label,value,position,action,min,max,increment):
    height = position[1]
    width = position[0]
    pos = [62.5,90.5]
    rowBox = UI.BoxElement(window,[50+width,height],4,0.5, blockColor, 5)
    titleText = UI.TextElement(window,[40+width,height], textColor, 0, label)

    #create metadata based on its type
    if type(value) is bool:
        flowState.debug(str(label)+" IS A BOOL!!!")
        buildBooleanInput(label, window, label, value, position, action)
        channelInput = None
    if type(value) is int:
        flowState.debug(str(label)+" IS AN INT!!!")
        buildIntegerInput(label, window, label, value, position, action, min, max, increment)

    window.add(label+"RowBox",rowBox)
    window.add(label+"TitleText",titleText)
    return None

if(owner['init']==0):
    flowState.sceneHistory.append(logic.getCurrentScene().name)
    owner['init'] = 1
    inset = 0.2

    metadataContainerBlock = UI.BoxElement(window,[85,50],5,6, blockColor, -1000)

    owner['metadataObject'] = []
    i = 0
    asset = logic.flowState.getMapEditor().selectedAsset
    if(asset!=None):
        if 'metadata' in asset:
            print(asset['metadata'])
        for key in asset['metadata']:
            if(key not in flowState.STATIC_METADATA):
                value = asset['metadata'][key]
                metadataInput = spawnMetadataInput(window,key,value,[30,85-(i*10)],inputAction,1,10000,1)
                i+=1

    mainMenuBlock = UI.BoxElement(window,[7.5,2.5],1.5,.5, blockColor, 1)
    mainMenuText = UI.TextElement(window,mainMenuBlock.position, textColor, 0, "MAIN MENU")
    mainMenuButton = UI.UIButton(mainMenuText,mainMenuBlock,mainMenuAction)

    #playBlock = UI.BoxElement(window,[65,2.5],1,.5, blockColor, 1)
    #playText = UI.TextElement(window,playBlock.position, textColor, 0, "PLAY")
    #playButton = UI.UIButton(playText,playBlock,playAction)

    unitsBlock = UI.BoxElement(window,[90,90],2,.5, blockColor, 1)
    unitsText = UI.TextElement(window,unitsBlock.position, textColor, 0, "TOGGLE UNITS")
    unitsButton = UI.UIButton(unitsText,unitsBlock,toggleUnitsAction)

    saveBlock = UI.BoxElement(window,[75,2.5],1,.5, blockColor, 1)
    saveText = UI.TextElement(window,saveBlock.position, textColor, 0, "SAVE")
    saveButton = UI.UIButton(saveText,saveBlock,saveAction)

    helpBlockElement = UI.BoxElement(window,[85,2.5],1,.5, blockColor, 1)
    helpText = UI.TextElement(window,helpBlockElement.position, textColor, 0, "HELP")
    helpButton = UI.UIButton(helpText,helpBlockElement,helpAction)


    quitBlockElement = UI.BoxElement(window,[95,2.5],1,.5, blockColor, 1)
    quitText = UI.TextElement(window,quitBlockElement.position, textColor, 0, "RESUME")
    quitButton = UI.UIButton(quitText,quitBlockElement,quitGameAction)


    owner['window'].add("metadataContainerBlock",metadataContainerBlock)
    owner['window'].add("mainMenuBlock",mainMenuBlock)
    owner['window'].add("mainMenuText",mainMenuText)
    owner['window'].add("mainMenuButton",mainMenuButton)
    owner['window'].add("unitsBlock",unitsBlock)
    owner['window'].add("unitsText",unitsText)
    owner['window'].add("unitsButton",unitsButton)
    owner['window'].add("saveBlock",saveBlock)
    owner['window'].add("saveText",saveText)
    owner['window'].add("saveButton",saveButton)
    owner['window'].add("helpBlockElement",helpBlockElement)
    owner['window'].add("helpText",helpText)
    owner['window'].add("helpButton",helpButton)
    owner['window'].add("quitBlockElement",quitBlockElement)
    owner['window'].add("quitText",quitText)
    owner['window'].add("quitButton",quitButton)

if(owner['init']==1):
    try:
        editor = logic.flowState.getMapEditor()
        if(editor != None):
            if(flowState.getViewMode() == flowState.VIEW_MODE_MENU):
                UI.runWindow(window,cont)

        else:

            UI.runWindow(window,cont)
    except Exception as e:
        flowState.error(traceback.format_exc())
        owner['init'] = -1
