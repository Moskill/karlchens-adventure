from ursina import Entity, color
from ..systems.build import place_building, remove_building_at

class BuildController:
    def __init__(self, state, catalog, tile_size=1):
        self.state = state
        self.catalog = catalog
        self.idx = 0
        self.t = tile_size
        self.preview = Entity(model='cube', color=color.rgba(0,200,255,120), unlit=True, visible=False)
        self.visuals = []

    def select(self, index: int):
        self.idx = max(0, min(index, len(self.catalog)-1))

    def try_place(self, top_left):
        cur = self.catalog[self.idx]
        if place_building(self.state, cur, top_left):
            self.refresh_visuals()
            return True
        return False

    def try_remove(self, pos):
        if remove_building_at(self.state, pos):
            self.refresh_visuals()
            return True
        return False

    def refresh_visuals(self):
        for e in self.visuals:
            if e and not getattr(e,'__destroyed', False):
                e.disable(); e.parent=None
        self.visuals.clear()
        id2color = {
            "strawberry_field_v1": color.rgb(200,40,80),
            "bratwurst_stand_v1": color.rgb(200,120,60),
        }
        for b in self.state.buildings:
            w,h = b.size
            px = (b.top_left[0] + w/2 - 0.5) * self.t
            pz = (b.top_left[1] + h/2 - 0.5) * self.t
            c = id2color.get(b.attraction_id, color.azure)
            self.visuals.append(
                Entity(model='cube', color=c, unlit=True, position=(px,0.5,pz), scale=(w*self.t,1,h*self.t))
            )

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
