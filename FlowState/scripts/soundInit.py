import bge
logic = bge.logic
flowState = logic.flowState
render = bge.render
cont = logic.getCurrentController()
owner = cont.owner
for actuator in cont.actuators:
    #print(key)
    #actuator = cont.actuators[key]
    flowState.log("initializing sound: "+str(actuator))
    actuator.volume = 0
    actuator.startSound()