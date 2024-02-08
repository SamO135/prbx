import random
from pydantic import BaseModel
from prbx_project.all_cards import all_cards
from prbx_project.settings import Token
from prbx_project.card import Card

class Board(BaseModel):
    """A class representing the board."""

    available_tokens: dict[Token, int] = {Token.RED: 4, Token.BLUE: 4, Token.GREEN: 4,
                                          Token.WHITE: 4, Token.BLACK: 4, Token.YELLOW: 5}
    available_cards: list[Card] = [random.choice(all_cards[tier]) for _ in range(4) for tier in range(3)] # randomly select 4 cards from each tier of cards

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
            Card: The new card
        """
        if len(all_cards[card.tier-1]) <= 0:
            print(f"NO MORE TIER {card.tier} CARDS")
            quit()
        self.available_cards.remove(card)
        card_index = random.randint(0, len(all_cards[card.tier-1])-1)
        self.available_cards += [all_cards[card.tier-1][card_index]]
        all_cards[card.tier-1].pop(card_index)
        if reserved and self.available_tokens[Token.YELLOW] > 0:
            self.remove_tokens(tokens={Token.YELLOW: 1})