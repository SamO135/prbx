from pydantic import BaseModel
from prbx_project.board import Board
from prbx_project.player import Player
from prbx_project.settings import Token

class Game(BaseModel):
    """A class representing the entire gamestate."""

    board: Board
    players: list[Player]
    current_player: Player = None
    max_points: int = 15

    def __init__(self, *args, **kwargs):
        """Constructor method."""
        super().__init__(*args, **kwargs)
        self.current_player = self.players[0]


    def isOver(self):
        """Checks if a player has reached the winning score.
        
        Return:
            bool: True if game has finished, False otherwise.
        """
        for player in self.players:
            if player.points >= self.max_points:
                return True
        return False
    
    # Still need to implement the logic for the case where 2 people finish on the same turn and have the same number of points
    def getWinner(self):
        """Gets the winner of the game.
        
        Return:
            Player: The winning player"""
        winner = player[0]
        for player in self.players:
            if player.points > winner.points:
                winner = player
        return winner
    
    def collect_tokens(self, tokens: dict[Token, int]):
        """Updates the player and board when a player is collecting tokens.
        
        Args:
            tokens (dict[Token, int]): A dictionary of the tokens the player will collect.
        """
        self.board.removeTokens(tokens)
        self.current_player.collectTokens(tokens)



