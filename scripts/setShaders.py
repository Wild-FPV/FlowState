import bge
render = bge.render
logic = bge.logic
owner = logic.getCurrentController().owner
flowState = logic.flowState

graphicsSettings = flowState.getGraphicsSettings()
shaders = graphicsSettings.shaders
shading = graphicsSettings.shading
specularity = graphicsSettings.specularity
shadows = graphicsSettings.shadows
advancedGrass = graphicsSettings.advancedGrass

if not "shaderInit" in owner:
    print("PLAYER FOUND! SETTING SHADERS!!!!!")
    if hasattr(logic,"player"):
        owner['shaderInit'] = True

        playerCamera = logic.player['camera']

        if shaders:
            playerCamera.lens= 5.823523998260498
            logic.sendMessage("enable shaders")
            print("enabling shaders")
        else:
            playerCamera.lens = 10
            logic.sendMessage("disable shaders")
            print("disabling shaders")

        #render.showFramerate(frameRate)
        render.setGLSLMaterialSetting("lights",shading)
        render.setGLSLMaterialSetting("shaders",specularity)
        render.setGLSLMaterialSetting("shadows",shadows)

        print("setting lights "+str(shading))
        if(shading):
            print("setting specularity "+str(specularity))
            print("setting shadows "+str(shadows))
