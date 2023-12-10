from pydantic import BaseModel
from board import Board
from player import Player
from settings import Token

class Game(BaseModel):
    board: Board
    players: list[Player]
    current_player: Player = None
    max_points: int = 15

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.current_player = self.players[0]


    def isOver(self):
        for player in self.players:
            if player.points >= self.max_points:
                return True
        return False
    
    def getWinner(self):
        winner = player[0]
        for player in self.players:
            if player.points > winner.points:
                winner = player
        return winner
    
    def collect_tokens(self, tokens: dict[Token, int]):
        self.board.removeTokens(tokens)
        self.current_player.collectTokens(tokens)



