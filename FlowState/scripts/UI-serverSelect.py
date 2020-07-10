import bge
import traceback
import os
from os.path import isfile, join
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
mapButtons = []


if "window" not in owner:
    owner['window'] = UI.Window()

window = owner['window']

def mapSelectAction(key,mapName):
    scenes = logic.getSceneList()
    currentScene = logic.getCurrentScene()
    for scene in scenes:
        if(scene!=currentScene):
            scene.end()
    render.showMouse(0)
    flowState.selectMap(mapName)
    flowState.setGameMode(flowState.GAME_MODE_MULTIPLAYER)
    flowState.setViewMode(flowState.VIEW_MODE_PLAY)
    currentScene.replace("Main Game")

def loadMultiplayerServer(key,server):
    serverIP = server['address']
    serverPort = server['port']
    scenes = logic.getSceneList()
    currentScene = logic.getCurrentScene()
    for scene in scenes:
        if(scene!=currentScene):
            scene.end()
    render.showMouse(0)
    print("setting server name: "+serverIP)
    logic.lastServerIP = serverIP
    flowState.setGameMode(flowState.GAME_MODE_MULTIPLAYER)
    flowState.setViewMode(flowState.VIEW_MODE_PLAY)
    #flowState.selectMap("multiplayer.fmp")
    currentScene.replace("Main Game")
    flowState.setServerIP(serverIP)
    flowState.setServerPort(serverPort)
    flowState.log("loading server "+str(server))

def multiplayerAction():
    pass

def directConnectAction():
    bge.logic.sendMessage("cam2")
    currentScene = logic.getCurrentScene()
    currentScene.replace("UI-server-ip")


def backAction():
    currentScene = logic.getCurrentScene()
    sceneHistory = flowState.sceneHistory
    print(sceneHistory)
    backScene = sceneHistory[-2]
    removedScene = sceneHistory.pop(-1)
    removedScene = sceneHistory.pop(-1)
    print("removing scene "+str(removedScene))
    currentScene.replace(backScene)

def passAction():
    pass

def addMapButton(server,spacing,index):
    name = str(index)+": "+server['name']
    buttonIndex = len(mapButtons)
    height = 70-(buttonIndex*spacing)
    print(height)
    mapButtonBlock = UI.BoxElement(window,[50,height],5,0.5, blockColor, 1)
    mapButtonText = UI.TextElement(window,mapButtonBlock.position, textColor, 0,name)
    mapButton = UI.UIButton(mapButtonText,mapButtonBlock,loadMultiplayerServer,"server",server)
    mapButtons.append(mapButton)

    owner['window'].add("mapButtonBlock"+name,mapButtonBlock)
    owner['window'].add("mapButtonText"+name,mapButtonText)
    owner['window'].add("mapButton"+name,mapButton)


if(owner['init']!=True):

    #let's get the server list from the central server
    import requests
    import json
    url = "https://boxoprops.com/flow-state/flow-control/1.0.0/serverList.json"
    response = requests.get(url, data="")
    print(response.status_code)
    print(response.json())
    serverList = json.loads(response.text)
    print(serverList)
    servers = serverList['servers']
    print(servers)

    flowState.setViewMode(flowState.VIEW_MODE_MENU)
    flowState.sceneHistory.append(logic.getCurrentScene().name)
    owner['init'] = True
    window = UI.Window()

    inset = 0.2

    headerBox = UI.BoxElement(window,[50,95],11,1, blockColor, 1)
    headerText = UI.TextElement(window,headerBox.position, textColor, 0, "SELECT SERVER")
    #blendPath = logic.expandPath("//")
    #mapsPath = blendPath+"maps"+os.sep
    #f = []
    #maps = [f for f in os.listdir(mapsPath) if os.path.isfile(os.path.join(mapsPath, f))]

    #let's get the maps from the web server
    #import requests
    #import json
    #url = "https://boxoprops.com/flow-state/flow-control/1.0.0/maps.json"
    #response = requests.get(url, data="")
    #print(response.status_code)
    #print(response.json())
    #maps = json.loads(response.text)

    #maps = ["2018 Regional Final.fmp", "2018 Regional Qualifier.fmp", "custom.fmp"]
    spacing = 8

    for index in range(0,len(servers)):
        server = servers[index]
        addMapButton(server,spacing,index)

    itemNumber = len(mapButtons)
    mapListBox = UI.BoxElement(window,[50,50],5,((itemNumber)*spacing)/10, blockColor, 15)
    mapList = UI.UIList(mapListBox,mapButtons,spacing)

    #back button
    backBlockElement = UI.BoxElement(window,[10,10],1,.5, blockColor, 1)
    backText = UI.TextElement(window,backBlockElement.position, textColor, 0, "BACK")
    backButton = UI.UIButton(backText,backBlockElement,backAction)

    #direct connect button
    dcBlockElement = UI.BoxElement(window,[80,10],2,.5, blockColor, 1)
    dcText = UI.TextElement(window,dcBlockElement.position, textColor, 0, "DIRECT CONNECT")
    dcButton = UI.UIButton(dcText,dcBlockElement,directConnectAction)

    owner['window'].add("backBlockElement",backBlockElement)
    owner['window'].add("backText",backText)
    owner['window'].add("backButton",backButton)

    owner['window'].add("dcBlockElement",dcBlockElement)
    owner['window'].add("dcText",dcText)
    owner['window'].add("dcButton",dcButton)

    owner['window'].add("headerBox",headerBox)
    owner['window'].add("headerText",headerText)
    owner['window'].add("mapList",mapList)

else:
    try:
        #UI.run(cont)
        UI.runWindow(window,cont)
    except Exception as e:
        flowState.log(traceback.format_exc())
        owner['init'] = -1
