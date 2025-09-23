from ursina import Sky, DirectionalLight, Entity, color, camera, destroy, application
from ..ui.hud import HUD
from ..entities.player import make_player
from ..settings import PLAYER_SPEED, PLAYER_GRAVITY, PLAYER_JUMP

class Gameplay:
    def __init__(self, scene_manager):
        self.sm = scene_manager
        self.entities = []
        self.player = None
        self.hud = None

    def enter(self):
        Sky()
        DirectionalLight(shadows=True, rotation=(45, -35, 0))

        ground = Entity(model='plane', scale=64, texture='white_cube',
                        texture_scale=(64, 64), collider='box',
                        color=color.rgb(80, 120, 80))
        self.entities.append(ground)

        # Bunte Blöcke als simple Welt
        for x in range(-4, 5, 2):
            for z in range(-4, 5, 2):
                if x == 0 and z == 0:
                    continue
                cube = Entity(model='cube', position=(x, 0.5, z), collider='box',
                              color=color.hsv((x*10+z*10) % 360, 0.6, 0.9))
                cylinder = Entity(model='cylinder', position=(x, 0.5, z), color=color.hsv((x*10+z*10) % 360, 0.6, 0.9), height=1, direction=(0, 1, 0), mode='triangle')
                self.entities.append(cylinder)

        self.player = make_player(speed=PLAYER_SPEED, gravity=PLAYER_GRAVITY, jump_height=PLAYER_JUMP)
        self.player.y = 2

        self.hud = HUD()  # hängt an camera.ui

    def input(self, key):
        if key == 'escape':
            from .main_menu import MainMenu
            self.sm.set_scene(MainMenu(self.sm))
        if key == 'left_mouse_down':
            self.hud.consume_ammo(1)
        if key == 'h':
            self.hud.damage(5)

    def update(self):
        pass  # Platz für Spiel-Logik

    def exit(self):
        # HUD entfernen
        if self.hud:
            self.hud.destroy()
            self.hud = None
        # Player entfernen
        if self.player and not getattr(self.player, "__destroyed", False):
            destroy(self.player)
            self.player = None
        # Welt entsorgen
        for e in self.entities:
            if e and not getattr(e, "__destroyed", False):
                destroy(e)
        self.entities.clear()
