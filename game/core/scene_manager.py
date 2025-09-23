from ursina import Entity, destroy

class SceneManager(Entity):
    def __init__(self):
        super().__init__()
        self.current = None

    def set_scene(self, scene):
        # Alte Szene sauber schließen
        if self.current:
            try:
                self.current.exit()
            except Exception as e:
                print("Scene exit error:", e)
        self.current = scene
        self.current.enter()

    # Wird von Ursina automatisch aufgerufen (weil Entity)
    def update(self):
        if self.current and hasattr(self.current, "update"):
            self.current.update()

    def input(self, key):
        if self.current and hasattr(self.current, "input"):
            self.current.input(key)
