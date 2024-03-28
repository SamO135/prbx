from prbx_project.gamestate import GameState
from prbx_project.player import Player
from pydantic import BaseModel
from typing import Optional

class Node(BaseModel):
    parent: Optional["Node"]
    action: dict
    gamestate: GameState
    children: list["Node"]
    value: int
    num_visits: int

    def calculate_value(self, pov: Player) -> None:
        self.value = 0
        for player in self.gamestate.players:
            if player.name == pov.name:
                self.value +=  (player.points * 5)
                self.value += sum(player.tokens.values())
            else:
                self.value -= (player.points * 5)
                self.value -= sum(player.tokens.values())
            