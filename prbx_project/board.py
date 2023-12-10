from pydantic import BaseModel
from player import Player
from settings import Token
from card import Card

class Board(BaseModel):
    players: list[Player]
    # current_turn: Player = players[0]
    available_tokens: dict[Token, int] = {Token.RED: 4, Token.GREEN: 4, Token.BLUE: 4, 
                                          Token.WHITE: 4, Token.BLACK: 4, Token.YELLOW: 5}
    available_cards: list[Card] = [Card.new_card() for i in range(12)]