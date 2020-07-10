import bge
print("INIT STARTING!!!")
from scripts.abstract.FlowState import FlowState
render = bge.render
logic = bge.logic
logic.flowState = FlowState() #let's add our flow state object to the logic controller so we can access it from other scripts
flowState = logic.flowState


logic.loadGlobalDict() #load the settings from the save file
flowState.loadSaveSettings() #load those settings into our game state

#TODO: consider getting rid of this since it's in flowstate
flowState.sceneHistory = [] #let's keep a list of what scene/menu we are in so we can use a "back" button
logic.saveGlobalDict()

print("INIT FINISH!!!")
