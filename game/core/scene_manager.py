from ursina import Entity

class SceneManager(Entity):
    def __init__(self):
        super().__init__()
        self.current = None

    def set_scene(self, scene):
        if self.current and hasattr(self.current, "exit"):
            self.current.exit()
        self.current = scene
        if hasattr(self.current, "enter"):
            self.current.enter()

    def update(self):
        if self.current and hasattr(self.current, "update"):
            self.current.update()

    def input(self, key):
        if self.current and hasattr(self.current, "input"):
            self.current.input(key)
