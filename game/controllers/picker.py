from ursina import Entity, color, mouse

class Picker:
    def __init__(self, w: int, h: int, tile_size=1):
        self.tile = tile_size
        self.plane = Entity(
            model='quad', rotation_x=90, position=(w/2-0.5, 0, h/2-0.5),
            scale=max(w, h) + 10, color=color.rgba(0,0,0,0), collider='box', unlit=True, visible=False
        )

    def grid_pos(self):
        if mouse.hovered_entity is not self.plane or mouse.world_point is None:
            return None
        wp = mouse.world_point
        gx = int(round(wp.x / self.tile))
        gz = int(round(wp.z / self.tile))
        return (gx, gz)
