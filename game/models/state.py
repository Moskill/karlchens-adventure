# game/models/state.py
from dataclasses import dataclass, field
from typing import List, Tuple

@dataclass
class PlacedBuilding:
    attraction_id: str
    size: Tuple[int,int]
    top_left: Tuple[int,int]

@dataclass
class GameState:
    money: int = 500
    fans: int = 10
    save_slot: str = "save_slot1.json"
    grid_size: Tuple[int,int] = (20, 20)
    buildings: List[PlacedBuilding] = field(default_factory=list)
