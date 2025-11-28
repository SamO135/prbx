from prbx_project.simulation.gamestate import GameState
from prbx_project.simulation.player import Player
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
                self.value += player.points
            # else:
            #     self.value -= player.points

    def update_value(self, terminal_value: int) -> None:
        self.value = ((self.value * self.num_visits) + terminal_value) / (
            self.num_visits + 1
        )
