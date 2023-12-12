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
    
    def recieve_tokens(self, tokens: dict[Token, int]):
        for token, amount in tokens.items():
            self.available_tokens[token] += amount
        return self.available_tokens
    
    def replace_card(self, card: Card, reserved: bool = False) -> Card:
        """Replace one of the available cards with a new random card of the same tier.
        
        Args:
            card (Card): The card to be replaced
            reserved (bool): True if the card is being reserved, False if the card is being purchased
            
        Return:
            Card: The newly generated card
        """
        self.available_cards.remove(card)
        self.available_cards += [Card.new_card()]
        if reserved and self.available_tokens[Token.YELLOW] > 0:
            self.remove_tokens(tokens={Token.YELLOW: 1})