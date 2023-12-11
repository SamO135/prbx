from pydantic import BaseModel
from prbx_project.card import Card
from prbx_project.settings import Token
from itertools import combinations
import random
import copy

class Player(BaseModel):
    hand: list[Card] = None
    reserved: list[Card] = None
    points: int = 0
    tokens: dict[Token, int] = {Token.RED: 0, Token.BLUE: 0, Token.GREEN: 0, Token.WHITE: 0, Token.BLACK: 0, Token.YELLOW: 0}
    bonuses: dict[Token, int] = {Token.RED: 0, Token.BLUE: 0, Token.GREEN: 0, Token.WHITE: 0, Token.BLACK: 0, Token.YELLOW: 0}


    def get_buyable_cards(self, cards: list[Card]):
        buyable_cards = []
        for card in cards:
            buyable = True
            for card_token, token_amount in card.price.items():
                if self.tokens[card_token] + self.bonuses[card_token] < token_amount:
                    buyable = False
                    break
            if buyable:
                buyable_cards.append(card)
        return buyable_cards
    
    def get_token_collection_moves(self, available_tokens: dict[Token, int]) -> list[dict[Token, int]]:
        available_tokens_copy = copy.deepcopy(available_tokens)
        if Token.YELLOW in available_tokens_copy:
            collectable_tokens = available_tokens_copy.pop(Token.YELLOW)
        collectable_tokens = {token: num for token, num in available_tokens_copy.items() if num > 0}
        token_collection_moves = []
        # 2 of same type
        token_collection_moves = [{token: 2} for token, available in collectable_tokens.items() if available >= 4]
        # 1 of three different types
        token_collection_moves += [{token: 1 for token in combo} for combo in combinations(collectable_tokens, 3)]
        return token_collection_moves

    def get_possible_moves(self, available_tokens, available_cards):
        buyable_cards = self.get_buyable_cards(available_cards) # + reserved cards
        reservable_cards = available_cards # + 3 face down cards
        collectable_tokens = self.get_token_collection_moves(available_tokens)
        possible_moves = {"buy_card": buyable_cards, "reserve_card": reservable_cards, "collect_tokens": collectable_tokens}
        if possible_moves['buy_card'] == []:
            possible_moves.pop('buy_card')
        return possible_moves

    # This is where the monte carlo stuff would go maybe
    def select_move(self, available_tokens, available_cards):
        possible_moves = self.get_possible_moves(available_tokens, available_cards)
        move_type = random.choice(list(possible_moves.keys()))
        move = random.choice(possible_moves[move_type])
        return (move, move_type)
    
    def collectTokens(self, tokens: dict[Token, int]):
        for token, amount in tokens.items():
            if token in self.tokens:
                self.tokens[token] += amount
        return self.tokens