import numpy as np
import math as m
import bge
import mathutils
import warnings
warnings.filterwarnings("ignore", category=RuntimeWarning)
logic = bge.logic
render = bge.render
cont = logic.getCurrentController()
owner = cont.owner

droneSettings = logic.flowState.getDroneSettings()

def angle(v1, v2):
    a = np.dot(v1, v2)
    b = np.linalg.norm(v1)
    c = np.linalg.norm(v2)
    angle = np.arccos(a / (b * c))
    return angle
    #return 2 * np.pi - angle

def drawVectorFromPosition(pos,vect,color):
    render.drawLine(pos,[pos[0]+vect[0],pos[1]+vect[1],pos[2]+vect[2]],color)

def drawStuff(position,a1,a2):
    drawVectorFromPosition(position,a1,[0,0,1])
    drawVectorFromPosition(position,a2,[1,0,0])

def main():
    pDrag = 0.225 #the magic parasitic drag number (needs to be measured)
    pDrag += ((droneSettings.pDrag-70)/1000) #allow the user to change parasitic drag by +/- 0.05

    iDrag = 0.675 #the magic induced drag number (needs to be measured)
    iDrag += ((droneSettings.iDrag-70)/1000) #allow the user to change induced drag by +/- 0.05

    totalDragMultiplier = 1.0*((droneSettings.weight/500)**0.75) #we're going to assume that the drone's size scales with the weight until we have measurements from parts
    dragMultiplier = totalDragMultiplier*(pDrag) #parasitic drag (4.0 - 3.0)
    liftMultiplier = totalDragMultiplier*(iDrag) #induced drag (lift/downforce)

    velocity = owner.getLinearVelocity(True) #local velocity of the model

    #let's get the model's Z axis as a vector
    vect = owner.orientation.to_euler()
    topVec = mathutils.Vector((0.0, 0.0, 1.0))

    #measure the model's angle of attack
    aoa = m.degrees(angle(velocity,topVec))

    #let's get the magnitude of the airflow vector
    mag = m.sqrt((velocity[0]**2)+(velocity[1]**2)+(velocity[2]**2))

    #the angle of attack goes between 180 and 0, let's make it go from 1 to -1, apply our induced drag multiplier, and multiplay by the magnitude of the velocity (lift increases as airspeed increases)
    lift = (((aoa-90))/90)*liftMultiplier*mag
    liftVec = [0,0,lift] #left or downforce vector

    #let's create a vector for our parasitic drag, taking into account our drag multiplier
    drag = [-velocity[0]*dragMultiplier,-velocity[1]*dragMultiplier,-velocity[2]*dragMultiplier] #Parasitic drag
    #let's combine both parasitic and induced drag into a new vector
    aeroForce = [liftVec[0]+drag[0],liftVec[1]+drag[1],liftVec[2]+drag[2]]
    owner.applyForce(aeroForce,True) #apply the vector
main()
