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


    def is_over(self):
        """Checks if a player has reached the winning score.
        
        Return:
            bool: True if game has finished, False otherwise.
        """
        for player in self.players:
            if player.points >= self.max_points:
                return True
        return False
    
    # Still need to implement the logic for the case where 2 people finish on the same turn and have the same number of points
    def get_winner(self):
        """Gets the winner of the game.
        
        Return:
            Player: The winning player"""
        winner = self.players[0]
        for player in self.players:
            if player.points > winner.points:
                winner = player
        return winner
    
    # def collect_tokens(self, tokens: dict[Token, int]):
    #     """Updates the player and board when a player is collecting tokens.
        
    #     Args:
    #         tokens (dict[Token, int]): A dictionary of the tokens the player will collect.
    #     """
    #     self.board.remove_tokens(tokens)
    #     self.current_player.collect_tokens(tokens)

    def num_tokens_in_play(self, board: Board, player1: Player, player2: Player):
        num_tokens = 0
        num_tokens += sum(board.available_tokens.values())
        num_tokens += sum(player1.tokens.values())
        num_tokens += sum(player2.tokens.values())

        tokens = board.available_tokens
        for token, _ in tokens.items():
            tokens[token] += player1.tokens[token]
            tokens[token] += player2.tokens[token]
        return tokens, num_tokens


    def collect_tokens():
        pass

    def reserve_card():
        pass

    def buy_card():
        pass