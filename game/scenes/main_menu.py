from ursina import Entity, Panel, Text, Button, color, camera, application
from .park import Park

class MainMenu:
    def __init__(self, scene_manager):
        self.sm = scene_manager
        self.ui = None

    def enter(self):
        self.ui = Entity(parent=camera.ui)
        Panel(parent=self.ui, z=0.1, scale=(0.7, 0.55),
              color=color.rgba(0, 0, 0, 180), roundness=0.02)
        Text("Karlchens Adventure", parent=self.ui, x=-0.32, y=0.38, scale=2.6, color=color.azure)

        b1 = Button(text="Spiel starten", parent=self.ui, y=0.05, scale=(0.45, 0.08))
        b1.on_click = lambda: self.sm.set_scene(Park(self.sm))

        b2 = Button(text="Fortsetzen", parent=self.ui, y=-0.07, scale=(0.45, 0.08))
        b2.on_click = lambda: self.sm.set_scene(Park(self.sm))  # später: Savegame laden

        b3 = Button(text="Beenden", parent=self.ui, y=-0.19, scale=(0.45, 0.08))
        b3.on_click = application.quit

        Text("ESC: Beenden", parent=self.ui, y=-0.3, color=color.gray)

    def input(self, key):
        if key == "escape":
            from ursina import application
            application.quit()

    def exit(self):
        if self.ui:
            self.ui.disable()
            self.ui.parent = None
            self.ui = None
