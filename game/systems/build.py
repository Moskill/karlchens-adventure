# game/systems/build.py
from typing import Dict, Tuple
from ..models.state import GameState, PlacedBuilding
from .grid import can_place

def place_building(state: GameState, attraction: Dict, pos: Tuple[int,int]) -> bool:
    size = tuple(attraction["size"])
    if not can_place(state, size, pos):
        return False
    price = int(attraction.get("price", 0))
    if state.money < price:
        return False
    state.money -= price
    state.buildings.append(PlacedBuilding(
        attraction_id=attraction["id"], size=size, top_left=pos
    ))
    return True

def remove_building_at(state: GameState, pos: Tuple[int,int]) -> bool:
    for i, b in enumerate(state.buildings):
        x0, y0 = b.top_left; w, h = b.size
        if x0 <= pos[0] < x0+w and y0 <= pos[1] < y0+h:
            state.buildings.pop(i)
            return True
    return False
