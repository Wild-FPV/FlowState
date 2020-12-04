import bge
logic = bge.logic
render = bge.render
scene = logic.getCurrentScene()
cont = logic.getCurrentController()
owner = cont.owner
import bge
logic = bge.logic
flowState = logic.flowState
scene = logic.getCurrentScene()
owner = logic.getCurrentController().owner
parent = owner.parent
checkpoint = scene.addObject(flowState.ASSET_CHECKPOINT,owner,0)
checkpoint.setParent(parent)
size = owner.localScale
checkpoint.localScale = [size[0],0.1,size[2]]

flowState.addMetadata(checkpoint)
#checkpoint['solid'] = True
owner.endObject()
