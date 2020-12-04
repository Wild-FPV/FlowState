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

def restartAction():
    scenes = logic.getSceneList()
    currentScene = logic.getCurrentScene()
    for scene in scenes:
        if(scene!=currentScene):
            scene.end()
    currentMap = logic.flowState.getSelectedMap()
    logic.flowState.resetGameState()
    logic.flowState.selectMap(currentMap)
    currentScene.replace("Map Editor")

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

def backAction():
    currentScene = logic.getCurrentScene()
    sceneHistory = flowState.sceneHistory
    print(sceneHistory)
    backScene = sceneHistory[-2]
    removedScene = sceneHistory.pop(-1)
    removedScene = sceneHistory.pop(-1)
    print("removing scene "+str(removedScene))
    currentScene.replace(backScene)

def resumeAction():
    currentScene = logic.getCurrentScene()
    currentScene.end()

if(owner['init']!=True):
    flowState.sceneHistory.append(logic.getCurrentScene().name)
    owner['init'] = True
    window = UI.Window()

    inset = 0.2

    mainMenuBlock = UI.BoxElement(window,[50,95],11,1, blockColor, 1)
    mainMenuText = UI.TextElement(window,mainMenuBlock.position, textColor, 0, "CONTROLS")
    helpHeight = 80
    helpWidth = 50
    inc = -5
    mainMenuText = UI.TextElement(window,[helpWidth,helpHeight+(inc*0)], textColor, 0, "W.S.A.D: movement")
    mainMenuText = UI.TextElement(window,[helpWidth,helpHeight+(inc*1)], textColor, 0, "mouse: look")
    mainMenuText = UI.TextElement(window,[helpWidth,helpHeight+(inc*2)], textColor, 0, "left click: place asset (create mode)")
    mainMenuText = UI.TextElement(window,[helpWidth,helpHeight+(inc*3)], textColor, 0, "left click: edit asset (edit mode)")
    mainMenuText = UI.TextElement(window,[helpWidth,helpHeight+(inc*4)], textColor, 0, "right click: select asset")
    mainMenuText = UI.TextElement(window,[helpWidth,helpHeight+(inc*5)], textColor, 0, "middle click: snap to ground")
    mainMenuText = UI.TextElement(window,[helpWidth,helpHeight+(inc*6)], textColor, 0, "scroll: push/pull cursor")
    mainMenuText = UI.TextElement(window,[helpWidth,helpHeight+(inc*7)], textColor, 0, "spacebar: toggle edit/create mode ")
    mainMenuText = UI.TextElement(window,[helpWidth,helpHeight+(inc*8)], textColor, 0, "delete/backspace: delete object")
    mainMenuText = UI.TextElement(window,[helpWidth,helpHeight+(inc*9)], textColor, 0, "G key: grid snap toggle")
    mainMenuText = UI.TextElement(window,[helpWidth,helpHeight+(inc*10)], textColor, 0, "T key: scale/rotate toggle")
    mainMenuText = UI.TextElement(window,[helpWidth,helpHeight+(inc*11)], textColor, 0, "R key: reset scale or rotation")
    mainMenuText = UI.TextElement(window,[helpWidth,helpHeight+(inc*12)], textColor, 0, "up arrow: next item")
    mainMenuText = UI.TextElement(window,[helpWidth,helpHeight+(inc*13)], textColor, 0, "down arrow: previous item")
    mainMenuText = UI.TextElement(window,[helpWidth,helpHeight+(inc*14)], textColor, 0, "left shift: fast movement")
    mainMenuText = UI.TextElement(window,[helpWidth,helpHeight+(inc*15)], textColor, 0, "esc: menu toggle")
    mainMenuBlock = UI.BoxElement(window,[50,40],6,7, blockColor, 1)
    #mainMenuButton = UI.UIButton(mainMenuText,mainMenuBlock,mainMenuAction)


    backBlockElement = UI.BoxElement(window,[90,10],1,.5, blockColor, 1)
    backText = UI.TextElement(window,backBlockElement.position, textColor, 0, "BACK")
    backButton = UI.UIButton(backText,backBlockElement,backAction)


else:
    try:
        editor = logic.flowState.getMapEditor()
        if(editor != None):
            if(flowState.getViewMode() == flowState.VIEW_MODE_MENU):
                UI.run(cont)
            else:
                backAction()
        else:
            UI.run(cont)
    except Exception as e:
        flowState.log(traceback.format_exc())
        owner['init'] = -1
