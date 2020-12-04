import bge
from collections import OrderedDict

groundMeshNames = {"grass":{"advanced":"ground grass advanced","simple":"ground grass simple"}}

if not hasattr(bge, "__component__"):
    render = bge.render
    logic = bge.logic
    try:
        flowState = logic.flowState
    except Exception as e:
        print("Ground: "+str(e))
        from scripts.abstract.FlowState import FlowState
        logic.flowState = FlowState()
        flowState = logic.flowState

class Ground(bge.types.KX_PythonComponent):
    args = OrderedDict([
        ("Ground Type", {"grass"}),
        ("Detail", {"advanced", "simple"})
    ])

    def start(self, args):
        flowState.log("levelGround: start("+str(args)+")")
        self.groundType = args['Ground Type']
        self.detail = args['Detail']
        self.updateGroundMesh()

    def updateGroundMesh(self):
        graphicsSettings = logic.flowState.getGraphicsSettings()
        if(graphicsSettings.getAdvancedGrass()):
            self.detail = "advanced"
        else:
            self.detail = "simple"
        self.replaceMesh(self.groundType,self.detail)

    def replaceMesh(self,groundType,detail):
        meshName = groundMeshNames[groundType][detail]
        self.object.replaceMesh(meshName,True,False)

    def update(self):
        pass
