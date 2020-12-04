import bge
import traceback
logic = bge.logic
render = bge.render
scene = logic.getCurrentScene()
cont = logic.getCurrentController()
owner = cont.owner
UI = bge.UI
textColor = [1,1,1,1]
flowState = logic.flowState
blockColor = flowState.menuButtonColor

def joystickMenuNav():
    joy = cont.sensors["JoystickButtons"]#cont.sensors["JoystickAxis"]
    #joyButtons = cont.sensors["JoystickButtons"]
    axis = joy.axisValues
    if(axis!=[]):
        rs = logic.flowState.getRadioSettings() #radio settings
        pitchInverted = -(int(rs.pitchInverted)-0.5)*2
        rollInverted = -(int(rs.rollInverted)-0.5)*2

        verticle = getStickPercentage(rs.minPitch,rs.maxPitch,axis[rs.pitchChannel-1]*pitchInverted)
        horizontal = getStickPercentage(rs.minRoll,rs.maxRoll,axis[rs.rollChannel-1]*rollInverted)
        aspectRatio = 3/4

        if('lastCursorPos' in owner):
            movement = [abs(owner['lastCursorPos'][0]-horizontal),abs(owner['lastCursorPos'][1]-verticle)]
            if(movement[0]+movement[1]>0.005):
                print([movement[0],movement[1]])
                #bge.render.drawLine([(horizontal*10)-5,(verticle*aspectRatio*10)-(5*aspectRatio),-1],[0,0,0],[1,1,1,1])
                #print([(horizontal*10)-5,verticle])
                windowSize = [bge.render.getWindowWidth(),bge.render.getWindowHeight()]
                render.setMousePosition(int(windowSize[0]*horizontal),int(windowSize[1]*(1-verticle)))
                owner['lastCursorPos'] = [horizontal,verticle]
        else:
            owner['lastCursorPos'] = [horizontal,verticle]

def getStickPercentage(min,max,value):
    resolution = abs(min)+abs(max)
    percent = abs(((value-min)/resolution))
    (0+(100/2))/100.0
    return percent

joystickMenuNav()
