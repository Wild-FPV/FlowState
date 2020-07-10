import bge
from collections import OrderedDict

if not hasattr(bge, "__component__"):
    global render
    import time
    logic = bge.logic
    flowState = logic.flowState

    import numpy as np
    import math as m

class Player(bge.types.KX_PythonComponent):
    args = OrderedDict([
    ])

    def start(self, args):
        self.init = False

    def update(self):
        flowState = logic.flowState
        if not self.init:
            self.init = True
            flowState.setPlayer(self)
