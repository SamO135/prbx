from pydantic import BaseModel
from card import Card
from settings import Token
from itertools import combinations
import random

class Player(BaseModel):
    _hand: list[Card] = None
    _reserved: list[Card] = None
    _points: int = None
    _tokens: list[dict[Token, int]] = None
    _bonuses: list[dict[Token, int]] = None


    def _get_buyable_cards(self, cards: list[Card]):
        cards = []
        for card in cards:
            for token, price in card.price.items():
                if self._tokens[token] + self._bonuses[token] > price:
                    cards.append(card)
        return cards
    
    def _get_token_collection_moves(self, available_tokens: dict[Token, int]) -> list[dict[Token, int]]:
        collectable_tokens = available_tokens.pop(Token.YELLOW)
        collectable_tokens = {token: num for token, num in available_tokens.items() if num > 0}
        token_collection_moves = []
        # 2 of same type
        token_collection_moves = [{token: 2} for token, available in collectable_tokens.items() if available >= 4]
        # 1 of three different types
        token_collection_moves += [{token: 1 for token in combo} for combo in combinations(collectable_tokens, 3)]
        return token_collection_moves

    def _get_possible_moves(self, available_tokens, available_cards):
        buyable_cards = self._get_buyable_cards(available_cards) # + _reserved cards
        reservable_cards = available_cards # + 3 face down cards
        collectable_tokens = self._get_token_collection_moves(available_tokens)
        possible_moves = {"buy_card": buyable_cards, "reserve_card": reservable_cards, "collect_tokens": collectable_tokens}
        if possible_moves['buy_card'] == []:
            possible_moves.pop('buy_card')
        return possible_moves


    # This is where the monte carlo stuff would go maybe
    def select_move(self, available_tokens, available_cards):
        possible_moves = self._get_possible_moves(available_tokens, available_cards)
        move_type = random.choice(list(possible_moves.keys()))
        move = random.choice(possible_moves[move_type])
        return (move, move_type)