from prbx_project.gamestate import GameState
from pydantic import BaseModel
from typing import Optional

class Node(BaseModel):
    parent: Optional["Node"]
    action: dict
    gamestate: GameState
    children: list["Node"]
    value: int
    num_visits: int

    def calculate_value(self) -> None:
        for player in self.gamestate.players:
            if player == self.gamestate.current_player:
                self.value +=  (player.points * 5)
                self.value += sum(player.tokens.values())
            else:
                self.value -= (player.points * 5)
                self.value -= sum(player.tokens.values())
            