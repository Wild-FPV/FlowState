import time
import bge
logic = bge.logic
cont = logic.getCurrentController()
owner = cont.owner
logic.endTime = time.perf_counter()
try:
    logic.startTime
except:
    logic.startTime = 0
    logic.endTime = 0
if(owner['playSound']):
    print("sound about to play")
    
print("frame time: "+str((logic.endTime-logic.startTime)*1000)+"ms")
logic.startTime = time.perf_counter()