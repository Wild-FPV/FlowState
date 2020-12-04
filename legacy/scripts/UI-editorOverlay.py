import bge
import math
import traceback
logic = bge.logic
flowState = logic.flowState
render = bge.render

scene = logic.getCurrentScene()
cont = logic.getCurrentController()
owner = cont.owner
UI = bge.UI

textColor = [1,1,1,1]
blockColor = flowState.menuButtonColor

if "window" not in owner:
    owner['window'] = UI.Window()

window = owner['window']

def updateElementValue(element,value):
    element.setText(value)

if(owner['init']==0):
    owner['init'] = 1
    escToggleHintText = UI.TextElement(window,[10,95], textColor, 0, "esc (toggle menu)",0.75)
    modeHintText = UI.TextElement(window,[7.75,90], textColor, 0, "mode: create",0.75)

    positionBlock = UI.BoxElement(window,[90,97.5],2.75,.5, blockColor, 0.75)
    positionText = UI.TextElement(window,positionBlock.position, textColor, 0, "P 100.0, 100.0, 100.0")

    orientationBlock = UI.BoxElement(window,[62.5,97.5],2.75,.5, blockColor, 0.75)
    orientationText = UI.TextElement(window,orientationBlock.position, textColor, 0, "O 100.0, 100.0, 100.0")

    window.add("positionBlock",positionBlock)
    window.add("positionText",positionText)
    window.add("orientationBlock",orientationBlock)
    window.add("orientationText",orientationText)
    window.add("escToggleHintText",escToggleHintText)
    window.add("modeHintText",modeHintText)

if(owner['init']==1):
    try:
        editor = logic.flowState.getMapEditor()
        if(editor != None):
            if(flowState.getViewMode == flowState.VIEW_MODE_MENU):
                UI.runWindow(window,cont)
            else:
                digits = 1
                cursorPos = list(logic.flowState.getMapEditor().cursor.position)
                cursorOri = list(logic.flowState.getMapEditor().cursor.orientation.to_euler())
                cursorOri = [math.degrees(cursorOri[0]),math.degrees(cursorOri[1]),math.degrees(cursorOri[2])]
                if(logic.flowState.getMapEditor().unitsMetric):
                    unit = 0.1 #metric (the game is scale 10x because of bullet physics)
                    positionValue = "meters: "+str(round(cursorPos[0]*unit,digits))+","+str(round(cursorPos[1]*unit,digits))+","+str(round(cursorPos[2]*unit,digits))
                else:
                    unit = 3.2808*0.1
                    positionValue = "feet: "+str(round(cursorPos[0]*unit,digits))+","+str(round(cursorPos[1]*unit,digits))+","+str(round(cursorPos[2]*unit,digits))
                updateElementValue(window.elements['positionText'], positionValue)

                orientationValue = "degrees: "+str(round(cursorOri[0],digits))+","+str(round(cursorOri[1],digits))+","+str(round(cursorOri[2],digits))
                updateElementValue(window.elements['orientationText'], orientationValue)

                editing = logic.flowState.getMapEditor().editing
                if(editing):
                    mode = "edit"
                else:
                    mode = "create"
                updateElementValue(window.elements['modeHintText'], "mode: "+mode)
        else:

            UI.runWindow(window,cont)
    except Exception as e:
        flowState.log(traceback.format_exc())
        owner['init'] = -1
