from prbx_project.gamestate import GameState
from pydantic import BaseModel
from typing import Optional

class Node(BaseModel):
    parent: Optional["Node"]
    action: Optional[dict]
    gamestate: GameState
    children: list["Node"] = []
    value: int = 0
    num_visits: int = 0 
