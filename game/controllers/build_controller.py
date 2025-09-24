from ursina import Entity, color, load_texture
from pathlib import Path
from ..systems.build import place_building, remove_building_at

class BuildController:
    def __init__(self, state, catalog, tile_size=1):
        self.state = state
        self.catalog = catalog
        self.idx = 0
        self.t = tile_size
        # Textur fürs Erdbeerfeld laden
        tex_path = Path(__file__).resolve().parents[2] / "game" / "resources" / "textures" / "strawberry_field_v1.png"
        self.tex_strawberry = self.tex_strawberry = load_texture('game/resources/textures/strawberry_field_v1.png')
        if not self.tex_strawberry:
            print("[WARN] Textur nicht gefunden:", tex_path)

        self.preview = Entity(model='cube', color=color.rgba(0,200,255,120), unlit=True, visible=False)
        self.visuals = []

    def select(self, index: int):
        self.idx = max(0, min(index, len(self.catalog)-1))

    def try_place(self, top_left):
        cur = self.catalog[self.idx]
        ok = place_building(self.state, cur, top_left)
        print("TRY_PLACE:", ok, "at", top_left, "id:", cur["id"], "money:", self.state.money)
        if ok:
            self.refresh_visuals()
            return True
        return False
    

    def try_remove(self, pos):
        if remove_building_at(self.state, pos):
            self.refresh_visuals()
            return True
        return False

    def refresh_visuals(self):
        # alte Visuals wegräumen
        for e in self.visuals:
            if e and not getattr(e, '__destroyed', False):
                e.disable(); e.parent = None
        self.visuals.clear()

        styles = {
            "strawberry_field_v1": dict(
                texture='game/resources/textures/strawberry_field_v1.png',
                color=color.white,     # wichtig: white → damit Texture nicht verfärbt wird
            ),
            "bratwurst_stand_v1": dict(
                texture='brick',
                color=color.rgb(200,120,60),
            ),
        }


        for b in self.state.buildings:
            w, h = b.size
            px = (b.top_left[0] + w/2 - 0.5) * self.t
            pz = (b.top_left[1] + h/2 - 0.5) * self.t

            if b.attraction_id == "strawberry_field_v1":
                # Nur die Top-Fläche als „Teppich“ zeichnen
                e = Entity(
                    model='quad',
                    rotation_x=90,              # in die XZ-Ebene drehen
                    position=(px, 0.021, pz),   # knapp über dem Grid (kein Z-Fighting)
                    scale=(w*self.t, h*self.t), # Fläche = w×h Tiles
                    texture=self.tex_strawberry or 'white_cube',
                    texture_scale=(w, h),       # Textur über die Fläche kacheln
                    color=color.white,
                    unlit=True,
                )
            else:
                # Default: einfacher Block (z.B. Bratwurststand)
                e = Entity(
                    model='cube',
                    position=(px, 0.5, pz),
                    scale=(w*self.t, 1, h*self.t),
                    texture='brick',
                    color=color.rgb(200,120,60),
                    unlit=True,
                )

            self.visuals.append(e)
            

    def update_preview(self, gp):
        if gp is None:
            self.preview.visible = False
            return
        cur = self.catalog[self.idx]
        w,h = cur["size"]
        px = (gp[0] + w/2 - 0.5) * self.t
        pz = (gp[1] + h/2 - 0.5) * self.t
        self.preview.position = (px, 0.5, pz)
        self.preview.scale    = (w*self.t, 1, h*self.t)
        self.preview.visible  = True
