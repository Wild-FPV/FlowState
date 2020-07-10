import bge.logic as logic
import time
cont = logic.getCurrentController()
own = cont.owner

try:
    logic.lastLogicTic
except:
    logic.lastLogicTic = float(time.perf_counter())
    print("creating time")
frameTime = float(time.perf_counter())-logic.lastLogicTic
own['Text'] = 1.0/frameTime