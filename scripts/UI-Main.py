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
#flowState = logic.flowState

def joystickMenuNav():
    joy = cont.sensors["JoystickAxis"]
    axis = joy.axisValues
    rs = flowState.getRadioSettings() #radio settings

    pitchInverted = -(int(rs.pitchInverted)-0.5)*2
    rollInverted = -(int(rs.rollInverted)-0.5)*2

    verticle = getStickPercentage(rs.minPitch,rs.maxPitch,axis[rs.pitchChannel-1]*pitchInverted)
    horizontal = getStickPercentage(rs.minRoll,rs.maxRoll,axis[rs.rollChannel-1]*rollInverted)
    aspectRatio = 3/4
    bge.render.drawLine([(horizontal*10)-5,(verticle*aspectRatio*10)-(5*aspectRatio),-1],[0,0,0],[1,1,1,1])
    print([(horizontal*10)-5,verticle])
    windowSize = [bge.render.getWindowWidth(),bge.render.getWindowHeight()]
    render.setMousePosition(int(windowSize[0]*horizontal),int(windowSize[1]*(1-verticle)))

def getStickPercentage(min,max,value):
    resolution = abs(min)+abs(max)
    percent = abs(((value-min)/resolution))
    (0+(100/2))/100.0
    return percent

def soloGameAction():
    scenes = logic.getSceneList()
    currentScene = logic.getCurrentScene()
    render.showMouse(0)
    currentScene.replace("UI-map-select")

def multiplayerGameAction():
    scenes = logic.getSceneList()
    currentScene = logic.getCurrentScene()
    render.showMouse(0)
    currentScene.replace("UI-server-select")

def doNothing():
    pass

def editorAction():
    scenes = logic.getSceneList()
    currentScene = logic.getCurrentScene()
    render.showMouse(0)
    currentScene.replace("UI-map-edit-select")

def settingsAction():
    #bge.logic.sendMessage("cam2") #we used to do this to set the background scene camera
    currentScene = logic.getCurrentScene()
    currentScene.replace("UI-settings")

def quitGameAction():
    logic.endGame()

def passAction():
    pass


if(owner['init']!=True):
    flowState.mapLoadStage = flowState.MAP_LOAD_STAGE_NONE
    flowState.setViewMode(flowState.VIEW_MODE_MENU)
    flowState.sceneHistory.append(logic.getCurrentScene().name)
    owner['init'] = True
    window = UI.Window()

    inset = 0.2

    mainMenuBlock = UI.BoxElement(window,[50,95],10,1, blockColor, 1)
    mainMenuText = UI.TextElement(window,mainMenuBlock.position, textColor, 0, "MAIN MENU")


    soloGameBlockElement = UI.BoxElement(window,[30,70],2.5,1.25, blockColor, 1)
    soloGameText = UI.TextElement(window,soloGameBlockElement.position, textColor, 0, "SINGLE PLAYER")
    soloGameButton = UI.UIButton(soloGameText,soloGameBlockElement,soloGameAction)

    multiplayerGameBlockElement = UI.BoxElement(window,[30,30],2.5,1.25, blockColor, 1)
    multiplayerGameText = UI.TextElement(window,multiplayerGameBlockElement.position, textColor, 0, "MULTIPLAYER")
    multiplayerGameButton = UI.UIButton(multiplayerGameText,multiplayerGameBlockElement,multiplayerGameAction)

    #asdf = UI.BoxElement(window,[50,50],10,9.9, [1,0,0,.5], 1)
    editorBlockElement = UI.BoxElement(window,[70,70],2.5,1.25, blockColor, 1)
    editorText = UI.TextElement(window,editorBlockElement.position, textColor, 0, "MAP EDITOR")
    editorGameButton = UI.UIButton(editorText,editorBlockElement,editorAction)

    settingsBlockElement = UI.BoxElement(window,[70,30],2.5,1.25, blockColor, 1)
    settingsText = UI.TextElement(window,settingsBlockElement.position, textColor, 0, "SETTINGS")

    settingsButton = UI.UIButton(settingsText,settingsBlockElement,settingsAction)


    quitBlockElement = UI.BoxElement(window,[90,10],1,.5, blockColor, 1)
    quitText = UI.TextElement(window,quitBlockElement.position, textColor, 0, "QUIT")
    quitButton = UI.UIButton(quitText,quitBlockElement,quitGameAction)

else:
    try:
        UI.run(cont)
        #joystickMenuNav()
    except Exception as e:
        logic.flowState.log(traceback.format_exc())
        owner['init'] = -1
