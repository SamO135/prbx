import random
from pydantic import BaseModel
from prbx_project.all_cards import all_cards
from prbx_project.game_token import Token
from prbx_project.card import Card

class Board(BaseModel):
    """A class representing the board."""

    all_cards: list[list[Card]] = all_cards
    available_tokens: dict[Token, int] = {Token.RED: 4, Token.GREEN: 4, Token.BLUE: 4,
                                          Token.WHITE: 4, Token.BLACK: 4, Token.YELLOW: 5}
    available_cards: list[Card] = []

    def __init__(self, *args, **kwargs):
        """Constructor method."""
        super().__init__(*args, **kwargs)
        self.available_cards: list[Card] = [self.all_cards[tier].pop(random.randrange(len(self.all_cards[tier]))) for _ in range(4) for tier in range(3)] # randomly select 4 cards from each tier of cards

    def remove_tokens(self, tokens: dict[Token, int]):
        """Removes tokens from the board.
        
        Args:
            tokens (dict[Token, int]): A dictionary of the tokens to remove from the board
            
        Return:
            dict[Token, int]: The remaining tokens on the board
        """
        for token, amount in tokens.items():
            if amount < 0:
                raise ValueError("Board cannot remove negative tokens.")
            if token in self.available_tokens:
                if amount > self.available_tokens[token]:
                    raise ValueError("Board cannot remove more tokens than are present.")
                self.available_tokens[token] -= amount
        return self.available_tokens
    
    def recieve_tokens(self, tokens: dict[Token, int]):
        """Adds tokens to the board.
        
        Args:
            tokens (dict[Token, int]): A dictionary of the tokens to add to the board
            
        Return:
            dict[Token, int]: The tokens on the board
        """
        for token, amount in tokens.items():
            if amount < 0:
                raise ValueError("Board cannot receive negative tokens.")
            if token in self.available_tokens:
                self.available_tokens[token] += amount
        return self.available_tokens

    def remove_card(self, card: Card):
        """Remove card from the board.
        
        Args:
            card (Card): The card to remove
        
        Return:
            list[Card]: The list of cards afterwards
            
        """
        self.available_cards.remove(card)
        return self.available_cards

    def add_new_card(self, tier: int):
        """Add a new card to the board.
        
        Args:
            tier: The tier of card to add (0 - 2)
            
        Return:
            Card: The new card
        """
        new_card = random.choice(self.all_cards[tier])
        self.available_cards += [new_card]
        self.all_cards[tier].remove(new_card)
        return new_card