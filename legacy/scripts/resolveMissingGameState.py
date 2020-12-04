import bge
from scripts.abstract.FlowState import FlowState
logic = bge.logic
try:
    logic.flowState
except:
    #If for some reason we never created a flow state, create a default instance
    print("WARNING GAME STATE WAS INVALID!")
    logic.flowState = FlowState()
    logic.loadGlobalDict()
    flowState.sceneHistory = []
    logic.saveGlobalDict()
    logic.flowState.log("Default Flow State created")
