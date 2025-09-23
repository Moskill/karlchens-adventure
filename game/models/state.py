from dataclasses import dataclass, field

@dataclass
class GameState:
    money: int = 500
    fans: int = 10
    save_slot: str = "save_slot1.json"
