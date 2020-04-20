import bge
import copy
import time
from collections import OrderedDict

raceband = {1:5658,2:5695,3:5732,4:5769,5:5806,6:5843,7:5880,8:5917}

if not hasattr(bge, "__component__"):
    render = bge.render
    logic = bge.logic
    flowState = logic.flowState

class RFEnvironment(bge.types.KX_PythonComponent):
    args = OrderedDict([
        ("Noise Floor", 0)
    ])

    def start(self, args):
        flowState.resetRFEnvironment()
        self.noiseFloor = args['Noise Floor']

    def update(self):
        flowState.updateRFEnvironment(self.noiseFloor)
