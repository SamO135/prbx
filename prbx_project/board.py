from pydantic import BaseModel
from prbx_project.player import Player
from prbx_project.settings import Token
from prbx_project.card import Card

class Board(BaseModel):
    """A class representing the board."""

    available_tokens: dict[Token, int] = {Token.RED: 4, Token.GREEN: 4, Token.BLUE: 4, 
                                          Token.WHITE: 4, Token.BLACK: 4, Token.YELLOW: 5}
    available_cards: list[Card] = [Card.new_card() for i in range(12)]

    def remove_tokens(self, tokens: dict[Token, int]):
        """Removes tokens to the board.
        
        Args:
            tokens (dict[Token, int]): A dictionary of the tokens to remove from the board
            
        Return:
            dict[Token, int]: The remaining tokens on the board
        """
        for token, amount in tokens.items():
            if token in self.available_tokens:
                self.available_tokens[token] -= amount
        return self.available_tokens
    