from ursina import Entity, Text, camera, color, DirectionalLight, Sky
from ..systems.savegame import save, load
from ..models.state import GameState

class Park:
    def __init__(self, scene_manager):
        self.sm = scene_manager
        self.ui = None
        self.state: GameState = None

    def enter(self):
        Sky()
        DirectionalLight(rotation=(45, -35, 0))
        self.state = load("save_slot1.json")

        self.ui = Entity(parent=camera.ui)
        self.lbl = Text(parent=self.ui, text=self._hud_text(), position=(-0.88, 0.46), scale=1.0, color=color.white)
        Text(parent=self.ui, text="(Phase 0) Leere Park-Szene\nS: Save  |  ESC: Menü",
             position=(-0.88, 0.40), scale=0.8, color=color.gray)

    def _hud_text(self):
        return f"Geld: {self.state.money}   Fans: {self.state.fans}"

    def input(self, key):
        if key == "escape":
            from .main_menu import MainMenu
            self.sm.set_scene(MainMenu(self.sm))
        elif key == "s":
            save("save_slot1.json", self.state)

    def update(self):
        if self.lbl:
            self.lbl.text = self._hud_text()

    def exit(self):
        if self.ui:
            self.ui.disable()
            self.ui.parent = None
            self.ui = None
