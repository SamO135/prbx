from pydantic import BaseModel
from prbx_project.card import Card
from prbx_project.settings import Token
from itertools import combinations, product
import random
import copy

class Player(BaseModel):
    """A class representing a player."""

    name: str
    hand: list[Card] = []
    reserved_cards: list[Card] = []
    points: int = 0
    tokens: dict[Token, int] = {Token.RED: 0, Token.BLUE: 0, Token.GREEN: 0, Token.WHITE: 0, Token.BLACK: 0, Token.YELLOW: 0}
    bonuses: dict[Token, int] = {Token.RED: 0, Token.BLUE: 0, Token.GREEN: 0, Token.WHITE: 0, Token.BLACK: 0, Token.YELLOW: 0}


    def get_buyable_cards(self, cards: list[Card]) -> list[Card]:
        """Checks which cards the player is able to buy.
    
        Args:
            cards (list[Card]): A list of Card objects
            
        Returns:
            list[Card]: A list of Card objects that the player is able to buy
        """
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
        """Gets all the combination of moves the player can do involving collecting tokens.
        
        Args:
            available_tokens (dict[Token, int]): A dictionary of all the tokens available on the board
            
        Return:
            list[dict[Token, int]]: A list of all the combinations of tokens the player can collect on their turn
        """
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

    def get_possible_moves(self, available_tokens: dict[Token, int], available_cards: list[Card]):
        """Gets all the possible moves the player can make on their turn.
        
        Args:
            available_tokens (dict[Token, int]): A dictionary of all the tokens available on the board
            available_cards (list[Card]): A list of all the cards on the board
            
        Return:
            A dictionary of all the possible moves the player can make on their turn
        """
        buyable_cards = self.get_buyable_cards(available_cards) + self.get_buyable_cards(self.reserved_cards)
        reservable_cards = available_cards if len(self.reserved_cards) < 3 else [] # + 3 face down cards
        collectable_tokens = self.get_token_collection_moves(available_tokens)
        possible_moves = {"buy_card": buyable_cards, "reserve_card": reservable_cards, "collect_tokens": collectable_tokens}
        # remove move_type if there are no possible moves for that type
        possible_moves = {move_type: moves for move_type, moves in possible_moves.items() if moves != []}
        # print(possible_moves["collect_tokens"])
        return possible_moves

    # This is where the monte carlo stuff would go maybe
    def select_random_move(self, available_tokens: dict[Token, int], available_cards: list[Card]):
        """Selects a random move from the possible list of moves the player can perform on their turn.
        
        Args:
            available_tokens (dict[Token, int]): A dictionary of all the tokens available on the board
            available_cards (list[Card]): A list of all the cards on the board
            
        Return:
            A tuple of the move and the category of the move
        """
        possible_moves = self.get_possible_moves(available_tokens, available_cards)
        try:
            move_type = random.choice(list(possible_moves.keys()))
        except IndexError as e:
            print("NO LEGAL MOVES")
            print(f"Available tokens: {available_tokens}")
            quit()
        # print(f"possible_moves[{move_type}]: {possible_moves[move_type]}")
        move = random.choice(possible_moves[move_type])
        return (move, move_type)
    
    def collect_tokens(self, tokens: dict[Token, int]) -> dict[Token, int]:
        """Adds tokens to the player's collection.
        
        Args:
            tokens (dict[Token, int]): A dictionary of the tokens to add to the player's collection
            
        Return:
            dict[Token, int]: The player's collection of tokens
        """
        for token, amount in tokens.items():
            if token in self.tokens:
                self.tokens[token] += amount

        # return excess tokens
        if sum([amount for amount in self.tokens.values()]) > 10:
            tokens_to_return = random.choice(self.get_possible_tokens_to_return())
            self.return_tokens(tokens_to_return)

        # while(len(self.tokens) > 10):
        #     token = random.choice([token for token, amount in tokens.items() if amount > 0]) # This needs to be changed somehow when the player is not picking random moves
        #     self.return_token(token)
        return self.tokens
    
    def get_possible_tokens_to_return(self) -> list[dict[Token, int]]:
        """Get all possible combinations of tokens the player can return when over 10 tokens. This includes yellow tokens.
        
        Return:
            list[dict[Token, int]]: All combinations as a list of dictionaries
        """
        num_to_return = sum([amount for amount in self.tokens.values()]) - 10
        if num_to_return <= 0:
            return []
        tokens_flat_list = [token for token, amount in self.tokens.items() for _ in range(amount)]
        valid_combinations_tuples = set(list(combinations(tokens_flat_list, r=num_to_return)))
        valid_combinations = [
            {token: combo.count(token) for token in combo}
            for combo in valid_combinations_tuples
        ]
        return valid_combinations
        
    def return_tokens(self, tokens: dict[Token, int]) -> dict[Token, int]:
        """Remove tokens from the player's collection, used when the player buys a card or has more than 10 tokens.
        
        Args:
            tokens (dict[Token, int]): A dictionary of the tokens to return
            
        Return:
            dict[Token, int]: The player's tokens
        """
        for token, amount in tokens.items():
            self.tokens[token] -= amount
        if any(amount for amount in self.tokens.values()) < 0:
            raise ValueError("Player cannot return more tokens than they own")
        return self.tokens
    
    def reserve_card(self, card: Card, available_tokens: dict[Token, int]) -> list[Card]:
        """Add a card to the players reserved cards list and give them a yellow token if one is available.
        
        Args:
            card (Card): The card the player is reserving
            available_tokens (dict[Token, int]): The available tokens on the board
            
        Return:
            list[Card]: The player's list of reserved cards
        """
        if not isinstance(card, Card):
            raise ValueError(f"Method expected {Card} but got {type(card)}")
        if len(self.reserved_cards) >= 3:
            raise IndexError(f"Player ({self.name}) already has 3 reserved cards")
        
        self.reserved_cards += [card]
        if available_tokens[Token.YELLOW] > 0:
            self.collect_tokens({Token.YELLOW: 1})
        return self.reserved_cards
    
    def calculate_real_price(self, card: Card) -> dict[Token, int]:
        real_price = copy.deepcopy(card.price)
        for token, price in card.price.items():
            real_price[token] -= self.bonuses[token]
        return real_price
    
    def buy_card(self, card: Card) -> bool:
        """Add a card to the players hand.
        
        Args:
            card (Card): The card the player is buying
            
        Return:
            bool: True if card is reserved, False otherwise"""
        if not isinstance(card, Card):
            raise ValueError(f"Method expected {Card} but got {type(card)}")
        self.hand += [card]

        # check if the card is one of the reserved cards
        reserved = False
        if card in self.reserved_cards:
            self.reserved_cards.remove(card)
            reserved = True

        # add prestige points
        self.points += card.points

        # pay/return the tokens
        self.return_tokens(self.calculate_real_price(card))

        # add bonuses
        self.bonuses[card.bonus] += 1

        return reserved
