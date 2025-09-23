from ursina import Ursina, window, color
from .core.scene_manager import SceneManager
from .settings import WINDOW_TITLE
from .scenes.main_menu import MainMenu

def boot_app():
    app = Ursina()
    window.title = WINDOW_TITLE
    window.borderless = False
    window.fullscreen = False
    window.color = color.rgb(25, 28, 35)

    # Szenenmanager ist ein Entity und kriegt update/input automatisch
    sm = SceneManager()
    sm.set_scene(MainMenu(sm))
    app.scene_manager = sm  # Referenz halten (optional)

    return app
