# import game engine modules
import bge
# import stand alone modules
import bgl
import blf
logic = bge.logic
render = bge.render
owner = logic.getCurrentController().owner

def init():
    """init function - runs once"""
    # create a new font object, use external ttf file
    font_path = logic.expandPath('//fonts/impact.ttf')
    # store the font indice - to use later
    logic.font_id = blf.load(font_path)

    # set the font drawing routine to run every frame
    scene = logic.getCurrentScene()
    scene.post_draw = [write]


def write():
    """write on screen"""
    width = render.getWindowWidth()
    height = render.getWindowHeight()

    # OpenGL setup
    bgl.glMatrixMode(bgl.GL_PROJECTION)
    bgl.glLoadIdentity()
    bgl.gluOrtho2D(0, width, 0, height)
    #bgl.glColor(1,1,1,1)
    bgl.glMatrixMode(bgl.GL_MODELVIEW)
    bgl.glLoadIdentity()

    # BLF drawing routine
    font_id = logic.font_id
    RED = (1, 0, 0, 1)
    pcol = ("Blue ", RED)
    #blf.color(font_id, 1, 1, 0, 0.5)
    blf.blur(font_id,500)
    blf.rotation(font_id, 90)
    blf.position(font_id, (width * 0.5), (height * 0.5), 0.5)
    blf.size(font_id, 20, 100)
    blf.draw(font_id, "Hello World1")
    blf.size(font_id, 50, 72)
    blf.position(font_id, (width * 0.0), (height * 0.5), 0.5)
    blf.draw(font_id, "Hello World2")

if 'init' in owner:
    write()
else:
    init()
    print(blf.__dict__)
    owner['init'] = True