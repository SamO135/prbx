from pydantic import BaseModel
from prbx_project.card import Card
from prbx_project.game_token import Token
from itertools import combinations
from collections import Counter
import random
import copy

class Player(BaseModel):
    """A class representing a player."""

    name: str
    hand: list[Card] = []
    reserved_cards: list[Card] = []
    points: int = 0
    tokens: dict[Token, int] = {Token.RED: 0, Token.GREEN: 0, Token.BLUE: 0, Token.WHITE: 0, Token.BLACK: 0, Token.YELLOW: 0}
    bonuses: dict[Token, int] = {Token.RED: 0, Token.GREEN: 0, Token.BLUE: 0, Token.WHITE: 0, Token.BLACK: 0, Token.YELLOW: 0}
    locked: bool = False


    def get_buyable_cards(self, cards: list[Card]) -> list[Card]:
        """Calculates which cards the player is able to buy.
    
        Args:
            cards (list[Card]): A list of Card objects
            
        Returns:
            list[Card]: A list of Card objects that the player is able to buy
        """
        buyable_cards = []
        for card in cards:
            real_price = self.calculate_real_price(card)
            # From the result of calculate_real_price, the only way the player can buy the card is if they have enough 
            # yellow tokens, so this is all I need to check for
            if self.tokens[Token.YELLOW] >= real_price[Token.YELLOW]:
                buyable_cards.append(card)
        return buyable_cards
    
    def get_token_collection_moves(self, available_tokens: dict[Token, int]) -> list[dict[Token, int]]:
        """Gets all the combinations of tokens the player can collect from the board.
        
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

    def get_possible_moves(self, available_tokens: dict[Token, int], available_cards: list[Card], reduced=True) -> list[dict]:
        """Gets all the possible moves the player can make on their turn.
        
        Args:
            available_tokens (dict[Token, int]): A dictionary of all the tokens available on the board
            available_cards (list[Card]): A list of all the cards on the board
            
        Return:
            A list of all the possible moves the player can make on their turn
        """
        buyable_cards = self.get_buyable_cards(available_cards) + self.get_buyable_cards(self.reserved_cards)
        # buy_card_moves = [{"move_type": "buy_card", "card": card, "payment": tokens} for card in buyable_cards for tokens in ]
        buy_card_moves = [{"move_type": "buy_card", "card": card, "payment": self.calculate_real_price(card)} for card in buyable_cards]
        if not reduced:
            buy_card_moves += [{"move_type": "buy_card", "card": card, "payment": payment} for card in buyable_cards for payment in self.get_payment_combinations(self.calculate_real_price(card), self.tokens[Token.YELLOW]-self.calculate_real_price(card)[Token.YELLOW])]
        unique_moves = []
        [unique_moves.append(move) for move in buy_card_moves if move not in unique_moves]
        buy_card_moves = unique_moves

        reservable_cards = available_cards if len(self.reserved_cards) < 3 else [] # + 3 face down cards
        returnable_tokens = [{token:  1} for token in self.tokens if self.tokens[token] > 0] if sum(self.tokens.values()) + 1 > 10 else [{}]
        reserve_card_moves = [{"move_type": "reserve_card", "card": card, "returning": returning} for card in reservable_cards for returning in returnable_tokens]
        
        collectable_tokens = self.get_token_collection_moves(available_tokens)
        collection_moves = [{"move_type": "collect_tokens", "tokens": tokens, "returning": returning} for tokens in collectable_tokens for returning in self.get_possible_tokens_to_return(additional_tokens=tokens)]
        
        possible_moves = buy_card_moves + reserve_card_moves + collection_moves
        return possible_moves

    # This is where the monte carlo stuff would go maybe
    def select_random_move(self, possible_moves: list[dict]) ->  dict:
        """Selects a random move from the possible list of moves the player can perform on their turn.
        
        Args:
            available_tokens (dict[Token, int]): A dictionary of all the tokens available on the board
            available_cards (list[Card]): A list of all the cards on the board
            
        Return:
            A dictionary detailing the move
        """
        move = random.choice(possible_moves)
        return move
    
    def collect_tokens(self, tokens: dict[Token, int]) -> dict[Token, int]:
        """Adds tokens to the player's collection.
        
        Args:
            tokens (dict[Token, int]): A dictionary of the tokens to add to the player's collection
        """
        for token, amount in tokens.items():
            if token in self.tokens:
                self.tokens[token] += amount
    
    def remove_tokens(self, tokens: dict[Token, int]) -> dict[Token, int]:
        """Removes tokens from the player's collection.
        
        Args:
            tokens (dict[Token, int]): A dictionary of the tokens to remove from the player's collection
        """
        for token, amount in tokens.items():
            self.tokens[token] = self.tokens[token] - amount
            if self.tokens[token] < 0:
                raise ValueError("Player cannot have negative tokens.")

    def collect_card(self, card: Card) -> None:
        """Adds a card to hand. Collects the bonus and points.
        
        Args:
            card (Card): The card the player is collecting
        """
        self.hand += [card]
        self.bonuses[card.bonus] += 1
        self.points += card.points


    def reserve_card(self, card: Card) -> None:
        """Adds a card to reserved cards.
        
        Args:
            card (Card): The card the player is collecting
        """
        if len(self.reserved_cards) >= 3:
            raise ValueError("A player cannot have more than 3 cards reserved at once.")
        self.reserved_cards += [card]

    def remove_reserved_card(self, card: Card) -> None:
        """Removes a card from reserved cards.
        
        Args:
            card (Card): The card to remove
        """
        self.reserved_cards.remove(card)

    
    def get_possible_tokens_to_return(self, additional_tokens: dict[Token, int] = {}) -> list[dict[Token, int]]:
        """Gets all possible combinations of tokens the player can return when over 10 tokens. This includes yellow tokens.
        
        Args:
            additional_tokens (dict[Token, int]): The additional tokens the player may have if they chose to collect tokens as their move

        Return:
            list[dict[Token, int]]: All combinations as a list of dictionaries
        """
        tokens =  copy.deepcopy(self.tokens)
        for token, amount in additional_tokens.items():
            tokens[token] += amount

        num_to_return = sum(tokens.values()) - 10
        if num_to_return <= 0:
            return [{}]
        tokens_flat_list = [token for token, amount in tokens.items() for _ in range(amount)]
        valid_combinations_tuples = set(list(combinations(tokens_flat_list, r=num_to_return)))
        valid_combinations = [
            {token: combo.count(token) for token in combo}
            for combo in valid_combinations_tuples
        ]
        return valid_combinations
    
    # def choose_tokens_to_return(self) -> dict[Token, int]:
    #     """Method to choose the combination of tokens to return when the player has over 10 tokens."""
    #     tokens = random.choice(self.get_possible_tokens_to_return())
    #     return tokens
    
    def calculate_real_price(self, card: Card) -> dict[Token, int]:
        """Applies the discount from the player's bonuses to the card's price, and includes the 
        minimum number of yellow tokens needed by the player to buy the card.
        
        Args:
            card (Card): The card the price is being calculated for
            
        Return:
            dict[Token, int]: The effective price of the card for the player
        """
        # calculate price given player's bonuses
        real_price = copy.deepcopy(card.price)
        for token, price in card.price.items():
            real_price[token] = max((real_price[token] - self.bonuses[token]), 0)
        
        # calculate the number of yellow tokens needed to buy the card
        num_yellows_needed = 0
        for token, price in real_price.items():
            if self.tokens[token] < price:
                num_missing_tokens = price - self.tokens[token]
                num_yellows_needed += num_missing_tokens
                real_price[token] = self.tokens[token]
        real_price[Token.YELLOW] = num_yellows_needed

        return real_price
    
    def get_payment_combinations(self, tokens: dict[Token, int], num_yellows: int) -> list[dict[Token, int]]:
        """Calculate all the combinations of tokens that can be used to pay for a card if a player were to 
        use any of their yellow tokens in place of any other token.

        Args:
            tokens (dict[Token, int]): the tokens to calculate combinations of
            num_yellows (int): the maximum number of yellow tokens that could be used in the payment

        Return:
            list[dict[Token, int]]: a list of all possible ways a card can be payed for given the price and the number of yellow tokens potentially used.
        """
        tokens_copy = copy.deepcopy(tokens)
        tokens_copy.pop(Token.YELLOW)
        tokens_flat_list = [token for token, amount in tokens_copy.items() for _ in range(amount)]
        unique_combos = []
        for i in range(1, num_yellows+1):
            combos = combinations(tokens_flat_list, max(len(tokens_flat_list)-i, 0))
            for j in combos:
                if j not in unique_combos:
                    payment = dict(Counter(j))
                    payment[Token.YELLOW] = i
                    for token in Token:
                        if token not in payment:
                            payment[token] = 0
                    unique_combos.append(payment)
        return unique_combos
    
    # def get_payment_combinations(self, real_price: dict[Token, int]):
    #     real_price_copy: dict[Token, int] = copy.deepcopy(real_price)
    #     real_price_copy.pop(Token.YELLOW)
    #     tokens_flat_list = [token for token, amount in real_price_copy.items() for _ in range(amount)]
    #     payment_combinations = []
    #     for num_yellows in range(real_price[Token.YELLOW]):
    #         payment_combinations += [[token for token in combo] for combo in combinations(tokens_flat_list, len(tokens_flat_list) - num_yellows)]

    #     return payment_combinations
