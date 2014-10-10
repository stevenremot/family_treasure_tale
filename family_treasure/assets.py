from graphics import GraphicsSystem

charsets = {"boy.png": (30,60),"burglar.png": (30,60), "girl.png": (30,60), "boy_chest.png": (40,60), "burglar_lantern.png": (30,60)}

orientations = ["wall_tile.png", "door2.png", "window.png", "window_open.png", "window_semiopen.png"]

def load_assets(graphics_system):
    """ Utility function to load graphics assets"""
    for c in charsets:
        graphics_system.load_charset(c, charsets[c])

    for o in orientations:
        graphics_system.load_four_orientations(o)
        
