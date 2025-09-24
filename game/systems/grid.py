# game/systems/grid.py
from typing import Tuple, List
from ..models.state import PlacedBuilding, GameState

Coord = Tuple[int, int]

def in_bounds(state: GameState, size: Tuple[int,int], pos: Coord) -> bool:
    W, H = state.grid_size
    w, h = size
    x, y = pos
    return 0 <= x and 0 <= y and x + w <= W and y + h <= H

def tiles_for(size: Tuple[int,int], pos: Coord) -> List[Coord]:
    w, h = size; x0, y0 = pos
    return [(x, y) for x in range(x0, x0+w) for y in range(y0, y0+h)]

def overlaps(state: GameState, size: Tuple[int,int], pos: Coord) -> bool:
    need = set(tiles_for(size, pos))
    for b in state.buildings:
        if need & set(tiles_for(b.size, b.top_left)):
            return True
    return False

def can_place(state: GameState, size: Tuple[int,int], pos: Coord) -> bool:
    return in_bounds(state, size, pos) and not overlaps(state, size, pos)
