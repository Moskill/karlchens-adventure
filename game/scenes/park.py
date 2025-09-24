from ursina import Entity, Text, camera, color, Vec3, held_keys, Sky, DirectionalLight
import json, os
from pathlib import Path
from ..systems.savegame import save, load_or_init
from ..models.state import GameState
from ..controllers.camera_controller import CameraController
from ..controllers.input_map import InputMap
from ..controllers.picker import Picker
from ..controllers.build_controller import BuildController
from ..views.grid_view import GridView

TILE = 1

class Park:
    def __init__(self, scene_manager):
        self.sm = scene_manager
        self.state: GameState = None

    def enter(self):
        Sky(); DirectionalLight(rotation=(45, -35, 0))

        # State laden
        save_path = Path(__file__).resolve().parents[2] / "save_slot1.json"
        self.state = load_or_init(str(save_path)) or GameState()
        W, H = self.state.grid_size
        center = Vec3((W-1)/2, 0, (H-1)/2)

        # Kamera-Controller (inkl. rechteckiger Screen-Bounds)
        self.cam = CameraController(center, W, H, padding=2.0)
        self.cam.setup_iso()              # yaw=-45, pitch=55 etc.
        self.cam.set_extra_bottom(2.0)    # wie besprochen: nach unten weiter erlauben

        # Grid zeichnen (ohne Collider)
        self.grid = GridView(TILE)
        self.grid.build(W, H)

        # Daten laden
        data_path = os.path.join(os.path.dirname(__file__), "..", "data", "attractions.json")
        with open(os.path.normpath(data_path), "r", encoding="utf-8") as f:
            self.catalog = json.load(f)

        # Picker + Build
        self.picker = Picker(W, H, TILE)
        self.build = BuildController(self.state, self.catalog, TILE)
        self.build.refresh_visuals()

        # UI
        self.ui = Entity(parent=camera.ui)
        self.lbl = Text(parent=self.ui, text=self._hud_text(), position=(-0.88, 0.46), scale=1.0, color=color.white)
        self.info = Text(parent=self.ui, text="L: bauen | R: entfernen | 1/2 wählen | Rad: Zoom | Pfeile/WASD: Pan",
                         position=(-0.88, 0.40), scale=0.8, color=color.gray)

        # Input map
        self.input_map = InputMap(self)

    def _hud_text(self):
        cur = self.catalog[self.build.idx]
        return f"Geld: {self.state.money}  Fans: {self.state.fans}   Wahl: {cur['name']} ({cur['size'][0]}x{cur['size'][1]})"

    # --- Input ---
    def input(self, key):
        self.input_map.handle(key)

    # --- InputMap-Helper ---
    def _to_menu(self):
        from .main_menu import MainMenu
        self.sm.set_scene(MainMenu(self.sm))

    def _save(self):
        save("save_slot1.json", self.state)

    def _place_at_cursor(self):
        gp = self.picker.grid_pos()
        if gp is not None:
            self.build.try_place(gp)

    def _remove_at_cursor(self):
        gp = self.picker.grid_pos()
        if gp is not None:
            self.build.try_remove(gp)

    # --- Update ---
    def update(self):
        # Panning (screen-space)
        step = self.cam.pan_step()
        dx = (held_keys['right arrow'] or held_keys['d']) - (held_keys['left arrow'] or held_keys['a'])
        dy = (held_keys['up arrow']    or held_keys['w']) - (held_keys['down arrow']  or held_keys['s'])
        if dx or dy:
            self.cam.pan_screen(dx*step, dy*step)

        # Preview + HUD
        self.build.update_preview(self.picker.grid_pos())
        self.lbl.text = self._hud_text()

    def exit(self):
        if getattr(self, 'ui', None):
            self.ui.disable(); self.ui.parent=None; self.ui=None
