from ursina.prefabs.first_person_controller import FirstPersonController

def make_player(speed=5, gravity=1, jump_height=1):
    return FirstPersonController(speed=speed, gravity=gravity, jump_height=jump_height, collider='box')
