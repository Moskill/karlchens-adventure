from ursina import Entity, color

class GridView:
    def __init__(self, tile_size=1):
        self.t = tile_size
        self.tiles = []


    def build(self, w: int, h: int):
        for x in range(w):
            for y in range(h):
                base = color.rgb(80,160,80) if (x+y)%2==0 else color.rgb(60,120,60)
                self.tiles.append(Entity(model='cube', 
                                        color=base, 
                                        unlit=True, 
                                        collider=None,
                                        position=(x*self.t, 0.01, y*self.t),
                                        scale=(self.t, 0.02, self.t)))
        # Grid-Linien
        for x in range(w+1):
            Entity(model='cube', 
                   color=color.black, 
                   unlit=True, 
                   collider=None,
                   position=(x*self.t - 0.5*self.t, 0.02, (h*self.t - self.t)/2),
                   scale=(0.02, 0.02, h*self.t))
        for y in range(h+1):
            Entity(model='cube', 
                   color=color.black, 
                   unlit=True, 
                   collider=None,
                   position=((w*self.t - self.t)/2, 0.02, y*self.t - 0.5*self.t),
                   scale=(w*self.t, 0.02, 0.02))