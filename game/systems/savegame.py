import json
from ..models.state import GameState

SAVE_VERSION = 1

def save(path: str, state: GameState):
    data = {"version": SAVE_VERSION, "money": state.money, "fans": state.fans}
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def load(path: str) -> GameState:
    try:
        with open(path, "r", encoding="utf-8") as f:
            d = json.load(f)
        return GameState(money=d.get("money", 0), fans=d.get("fans", 0))
    except FileNotFoundError:
        return GameState()
