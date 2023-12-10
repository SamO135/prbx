from pydantic import BaseModel
from player import Player
from settings import Token
from card import Card

class Board(BaseModel):
    available_tokens: dict[Token, int] = {Token.RED: 4, Token.GREEN: 4, Token.BLUE: 4, 
                                          Token.WHITE: 4, Token.BLACK: 4, Token.YELLOW: 5}
    available_cards: list[Card] = [Card.new_card() for i in range(12)]

    def removeTokens(self, tokens: dict[Token, int]):
        for token, amount in tokens.items():
            if token in self.available_tokens:
                self.available_tokens[token] -= amount
        return self.available_tokens
    