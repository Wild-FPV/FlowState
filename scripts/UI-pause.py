import bge
import traceback
import time
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
textColorGrey = [0.5,0.5,0.5,1]

def restartAction():
    render.showMouse(0)
    if(logic.flowState.getGameMode()!=logic.flowState.GAME_MODE_SINGLE_PLAYER):
        resetEvent = FSNObjects.PlayerEvent(FSNObjects.PlayerEvent.PLAYER_RESET,flowState.getNetworkClient().clientID,{"reset":time.time()+10})
        flowState.getNetworkClient().sendEvent(resetEvent)
        logic.sendMessage({"reset":time.time()+10})
    else:
        scenes = logic.getSceneList()
        currentScene = logic.getCurrentScene()
        for scene in scenes:
            if(scene!=currentScene):
                scene.end()
        currentMap = logic.flowState.getSelectedMap()
        logic.flowState.resetGameState()
        logic.flowState.selectMap(currentMap)
        currentScene.replace("Main Game")

def mainMenuAction():
    if(logic.flowState.getGameMode()!=logic.flowState.GAME_MODE_SINGLE_PLAYER):
        flowState.getNetworkClient().quit()
    else:
        scenes = logic.getSceneList()
        currentScene = logic.getCurrentScene()
        for scene in scenes:
            if(scene!=currentScene):
                scene.end()
        logic.flowState.resetGameState()
        logic.flowState.setViewMode(logic.flowState.VIEW_MODE_MENU)
        currentScene.replace("Menu Background")

def settingsAction():
    currentScene = logic.getCurrentScene()
    currentScene.replace("UI-settings")

def quitGameAction():
    logic.endGame()

def resumeAction():
    render.showMouse(0)
    currentScene = logic.getCurrentScene()
    currentScene.end()
    if(flowState.getGameMode()==flowState.GAME_MODE_SINGLE_PLAYER):
        logic.getSceneList()[0].resume()
    flowState.sceneHistory.remove(logic.getCurrentScene().name)

def doNothingAction():
    pass

if(owner['init']!=True):
    scenes = logic.getSceneList()
    currentScene = logic.getCurrentScene()

    #if the pause menu is already up
    if(logic.getCurrentScene().name in flowState.sceneHistory):
        flowState.log("pause menu already exists")
        flowState.log(currentScene)
        currentScene.end()
    else:
        flowState.setViewMode(flowState.VIEW_MODE_MENU)

        #pause the main game if we aren't in multiplayer

        print(scenes)
        if(flowState.getGameMode()==flowState.GAME_MODE_SINGLE_PLAYER):
            scenes[0].suspend()

        flowState.sceneHistory.append(logic.getCurrentScene().name)
        owner['init'] = True
        window = UI.Window()

        inset = 0.2

        mainMenuBlock = UI.BoxElement(window,[50,95],11,1, blockColor, 1)
        mainMenuText = UI.TextElement(window,mainMenuBlock.position, textColor, 0, "PAUSE MENU")

        mainMenuBlock = UI.BoxElement(window,[10,50],2,1, blockColor, 1)
        mainMenuText = UI.TextElement(window,mainMenuBlock.position, textColor, 0, "MAIN MENU")
        mainMenuButton = UI.UIButton(mainMenuText,mainMenuBlock,mainMenuAction)

        doNothingAction


        restartBlock = UI.BoxElement(window,[50,50],2,1, blockColor, 1)
        restartText = UI.TextElement(window,restartBlock.position, textColor, 0, "RESTART")
        restartButton = UI.UIButton(restartText,restartBlock,restartAction)

        settingsBlockElement = UI.BoxElement(window,[90,50],2,1, blockColor, 1)
        settingsText = UI.TextElement(window,settingsBlockElement.position, textColor, 0, "SETTINGS")
        settingsButton = UI.UIButton(settingsText,settingsBlockElement,settingsAction)

        quitBlockElement = UI.BoxElement(window,[90,10],1,.5, blockColor, 1)
        quitText = UI.TextElement(window,quitBlockElement.position, textColor, 0, "QUIT")
        quitButton = UI.UIButton(quitText,quitBlockElement,quitGameAction)

        resumeElement = UI.BoxElement(window,[10,10],1,.5, blockColor, 1)
        resumeText = UI.TextElement(window,resumeElement.position, textColor, 0, "RESUME")
        resumeButton = UI.UIButton(resumeText,resumeElement,resumeAction)

else:
    try:
        UI.run(cont)
    except Exception as e:
        flowState.log(traceback.format_exc())
        owner['init'] = -1
