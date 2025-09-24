class InputMap:
    def __init__(self, park):
        self.p = park
        self.actions = {
            'escape'          : self.p._to_menu,
            's'               : self.p._save,
            '1'               : lambda: self.p.build.select(0),
            '2'               : lambda: self.p.build.select(1),
            'left mouse down' : self.p._place_at_cursor,
            'right mouse down': self.p._remove_at_cursor,
            'scroll up'       : lambda: self.p.cam.zoom_ortho(-2),
            'scroll down'     : lambda: self.p.cam.zoom_ortho( 2),
        }

    def handle(self, key):
        fn = self.actions.get(key)
        if fn: fn()
