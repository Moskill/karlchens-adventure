from ursina import Entity, Panel, Text, Button, color, camera
from .gameplay import Gameplay

class MainMenu:
    def __init__(self, scene_manager):
        self.sm = scene_manager
        self.ui_root = None

    def enter(self):
        self.ui_root = Entity(parent=camera.ui)
        Panel(parent=self.ui_root, z=0.1, scale=(0.7, 0.6),
              color=color.rgba(0, 0, 0, 180), model='quad', roundness=0.02)

        Text("Karlchens Adventure", parent=self.ui_root, y=0.2, origin=(0,0), scale=2, color=color.azure)

        start_btn = Button(text='Spiel starten', parent=self.ui_root, y=0.05, scale=(0.4, 0.08))
        start_btn.on_click = lambda: self.sm.set_scene(Gameplay(self.sm))

        options_btn = Button(text='Optionen (Stub)', parent=self.ui_root, y=-0.08, scale=(0.4, 0.08))
        options_btn.on_click = lambda: print('TODO: Optionen')

        quit_btn = Button(text='Beenden', parent=self.ui_root, y=-0.21, scale=(0.4, 0.08))
        quit_btn.on_click = lambda: __import__('ursina').ursina.application.quit()

        Text("ESC: Beenden", parent=self.ui_root, y=-0.33, color=color.gray)

    def input(self, key):
        if key == 'escape':
            __import__('ursina').ursina.application.quit()

    def exit(self):
        if self.ui_root:
            self.ui_root.disable()
            self.ui_root.parent = None
            self.ui_root = None
