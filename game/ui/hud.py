from ursina import Entity, Text, camera, color

class HUD:
    def __init__(self):
        self.root = Entity(parent=camera.ui)
        self.health = 100
        self.ammo = 30

        self.txt_hp   = Text(parent=self.root, text=f"HP: {self.health}", position=(-0.88, 0.47), scale=1.2)
        self.txt_ammo = Text(parent=self.root, text=f"Munition: {self.ammo}", position=(-0.88, 0.42), scale=1.0)
        self.cross    = Text(parent=self.root, text='+', origin=(0,0), position=(0,0), scale=2, color=color.white)
        self.txt_info = Text(parent=self.root, text='WASD bewegen, Maus schauen, SPACE springen, ESC Menü',
                             position=(-0.88, -0.47), scale=0.8, color=color.gray)

    def consume_ammo(self, n):
        self.ammo = max(0, self.ammo - n)
        self.txt_ammo.text = f"Munition: {self.ammo}"
        if self.ammo == 0:
            self.txt_info.text = 'Keine Munition! (Demo)'

    def damage(self, n):
        self.health = max(0, self.health - n)
        self.txt_hp.text = f"HP: {self.health}"

    def destroy(self):
        if self.root:
            self.root.disable()
            self.root.parent = None
            self.root = None
