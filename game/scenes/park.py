from ursina import Entity, Text, camera, color, DirectionalLight, Sky, Button, mouse, Vec3, held_keys
import json, os
from ..systems.savegame import save, load_or_init
from ..models.state import GameState
from ..systems.build import place_building, remove_building_at
from ..systems.grid import tiles_for
from ursina import camera, Vec3
from pathlib import Path

TILE_SIZE = 1  # Welt-Einheiten pro Tile (später für Isometrie drehbar)

class Tile(Entity):
    def __init__(self, grid_pos, **kw):
        x, y = grid_pos
        base = color.rgb(80,160,80) if (x + y) % 2 == 0 else color.rgb(60,120,60)
        super().__init__(
            model='cube',
            texture='white_cube',
            color=color.green,
            unlit=True,
            collider='box',
            position=(x*TILE_SIZE, 0.01, y*TILE_SIZE),   # <- 0.01 statt -0.49
            scale=(TILE_SIZE, 0.02, TILE_SIZE),
            **kw
        )
        self.grid_pos = grid_pos

class Park:
    def __init__(self, scene_manager):
        self.sm = scene_manager
        self.ui = None
        self.state: GameState = None
        self.grid_entities = {}
        self.placed_visuals = []
        self.catalog = []
        self.current_idx = 0
        self.preview = None

    def enter(self):
        #test = Entity(model='cube', texture='white_cube', color=color.red, unlit=True,position=(0, 1, 0), scale=2)
        Sky(); 
        DirectionalLight(rotation=(45, -35, 0))
        save_path = str(Path(__file__).resolve().parents[2] / "save_slot1.json")  # immer Projektroot
        self.state = load_or_init(save_path) or GameState()   # Fallback, falls was schiefgeht
        W, H = self.state.grid_size
        

        # Daten laden
        data_path = os.path.join(os.path.dirname(__file__), "..", "data", "attractions.json")
        with open(os.path.normpath(data_path), "r", encoding="utf-8") as f:
            self.catalog = json.load(f)

        # Grid bauen (Topdown)
        W,H = self.state.grid_size
        center = Vec3((W-1)/2, 0, (H-1)/2)

        # Isometrische Ecke: Orthographic + 45° Y, leicht geneigt nach unten
        camera.orthographic = True
        camera.fov = max(W, H) * 1.35          # sichtbarer Ausschnitt (orthographic)
        camera.rotation_x = 55                  # nach unten neigen
        camera.rotation_y = -45                  # aus der Ecke schauen

        # Position so wählen, dass die Ecke passt (Diagonale)
        dist   = max(W, H) * 0.9
        height = max(W, H) * 0.5
        camera.position = (center.x + dist * 0.707, height, center.z - dist * 0.707)
        camera.look_at(center)

        for x in range(W):
            
            for y in range(H):
                t = Tile((x,y))
                self.grid_entities[(x,y)] = t

        # UI
        self.ui = Entity(parent=camera.ui)
        self.lbl = Text(parent=self.ui, text=self._hud_text(), position=(-0.88, 0.46), scale=1.0, color=color.white)
        self.info = Text(parent=self.ui, text=self._info_text(), position=(-0.88, 0.40), scale=0.8, color=color.gray)

        # Preview-Entity (Geister-Bauteil)
        self.preview = Entity(model='cube', color=color.rgba(0,200,255,120), visible=False)

        # Bereits gebaute laden/anzeigen
        self._refresh_visuals()

    def _hud_text(self):
        cur = self.catalog[self.current_idx]
        return f"Geld: {self.state.money}  Fans: {self.state.fans}   [1/2] Wahl: {cur['name']} ({cur['size'][0]}x{cur['size'][1]})"

    def _info_text(self):
        return "Links-Klick: bauen  |  Rechts-Klick: entfernen  |  1/2: Auswahl  |  S: speichern  |  ESC: Menü"

    def _grid_snap(self, world_pos: Vec3):
        # Welt → Grid
        gx = int(round(world_pos.x / TILE_SIZE))
        gy = int(round(world_pos.z / TILE_SIZE))
        return (gx, gy)

    def input(self, key):
        if key == 'escape':
            from .main_menu import MainMenu
            self.sm.set_scene(MainMenu(self.sm))
        elif key == 's':
            save("save_slot1.json", self.state)
        elif key in ('1','2'):
            self.current_idx = 0 if key=='1' else 1
        elif key == 'left mouse down' and mouse.hovered_entity:
            pos = self._grid_snap(mouse.world_point)
            if self._try_place(pos):
                self._refresh_visuals()
        elif key == 'right mouse down' and mouse.hovered_entity:
            pos = self._grid_snap(mouse.world_point)
            if remove_building_at(self.state, pos):
                self._refresh_visuals()

    def update(self):
        if self.lbl: self.lbl.text = self._hud_text()
        # Preview bewegen
        if mouse.hovered_entity:
            pos = self._grid_snap(mouse.world_point)
            cur = self.catalog[self.current_idx]
            w,h = cur["size"]
            # Preview-Mitte auf Fläche
            px = (pos[0] + w/2 - 0.5) * TILE_SIZE
            pz = (pos[1] + h/2 - 0.5) * TILE_SIZE
            self.preview.position = (px, 0.5, pz)
            self.preview.scale = (w*TILE_SIZE, 1, h*TILE_SIZE)
            self.preview.visible = True
        else:
            self.preview.visible = False

    # --- helpers ---
    def _try_place(self, top_left):
        cur = self.catalog[self.current_idx]
        ok = place_building(self.state, cur, top_left)
        return ok

    def _clear_visuals(self):
        for e in self.placed_visuals:
            if e and not getattr(e,'__destroyed', False):
                e.disable(); e.parent=None
        self.placed_visuals.clear()

    def _refresh_visuals(self):
        self._clear_visuals()
        # Bodenfarben kurz highlighten (optional)
        # Gebäude visualisieren als farbige Quader
        id2color = {
            "strawberry_field_v1": color.rgb(200,40,80),
            "bratwurst_stand_v1": color.rgb(200,120,60),
        }
        for b in self.state.buildings:
            w,h = b.size
            px = (b.top_left[0] + w/2 - 0.5) * TILE_SIZE
            pz = (b.top_left[1] + h/2 - 0.5) * TILE_SIZE
            c = id2color.get(b.attraction_id, color.azure)
            e = Entity(model='cube',texture='white_cube',color=c,unlit=True,position=(px, 0.5, pz),scale=(w*TILE_SIZE, 1, h*TILE_SIZE))
            self.placed_visuals.append(e)

    def exit(self):
        if self.ui:
            self.ui.disable(); self.ui.parent=None; self.ui=None



###########################################################################################################



# from ursina import Entity, Text, camera, color, DirectionalLight, Sky
# from ..systems.savegame import save, load
# from ..models.state import GameState

# class Park:
#     def __init__(self, scene_manager):
#         self.sm = scene_manager
#         self.ui = None
#         self.state: GameState = None

#     def enter(self):
#         Sky()
#         DirectionalLight(rotation=(45, -35, 0))
#         self.state = load("save_slot1.json")

#         self.ui = Entity(parent=camera.ui)
#         self.lbl = Text(parent=self.ui, text=self._hud_text(), position=(-0.88, 0.46), scale=1.0, color=color.white)
#         Text(parent=self.ui, text="(Phase 0) Leere Park-Szene\nS: Save  |  ESC: Menü",
#              position=(-0.88, 0.40), scale=0.8, color=color.gray)

#     def _hud_text(self):
#         return f"Geld: {self.state.money}   Fans: {self.state.fans}"

#     def input(self, key):
#         if key == "escape":
#             from .main_menu import MainMenu
#             self.sm.set_scene(MainMenu(self.sm))
#         elif key == "s":
#             save("save_slot1.json", self.state)

#     def update(self):
#         if self.lbl:
#             self.lbl.text = self._hud_text()

#     def exit(self):
#         if self.ui:
#             self.ui.disable()
#             self.ui.parent = None
#             self.ui = None
