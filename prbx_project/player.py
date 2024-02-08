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
            real_price = self.calculate_real_price(card)
            # From the result of calculate_real_price, the only way the player can buy the card is if they have enough 
            # yellow tokens, so this is all I need to check for
            if self.tokens[Token.YELLOW] >= real_price[Token.YELLOW]:
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
    def select_random_move(self, available_tokens: dict[Token, int], available_cards: list[Card], players): # players parameter is just for debugging purposes
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
            print(f"available tokens: {available_tokens}")
            print(f"player1 tokens:   {players[0].tokens}")
            print(f"player2 tokens:   {players[1].tokens}")
            quit()
        move = random.choice(possible_moves[move_type])
        return (move, move_type)
    
    def collect_tokens(self, tokens: dict[Token, int]) -> dict[Token, int]:
        """Adds tokens to the player's collection.
        
        Args:
            tokens (dict[Token, int]): A dictionary of the tokens to add to the player's collection
        """
        for token, amount in tokens.items():
            if token in self.tokens:
                self.tokens[token] += amount
    
    def remove_tokens(self, tokens: dict[Token, int]) -> dict[Token, int]:
        """Removed tokens from the player's collection.
        
        Args:
            tokens (dict[Token, int]): A dictionary of the tokens to remove from the player's collection
        """
        for token, amount in tokens.items():
            if token in self.tokens:
                self.tokens[token] = max(self.tokens[token] - amount, 0)

    def collect_card(self, card: Card):
        """Add card to hand. Collect the bonus and points.
        
        Args:
            card (Card): The card the player is collecting
        """
        self.hand += [card]
        self.bonuses[card.bonus] += 1
        self.points += card.points


    def reserve_card(self, card):
        """Add card to reserved cards.
        
        Args:
            card (Card): The card the player is collecting
        """
        self.reserved_cards += [card]

    def remove_reserved_card(self, card):
        """Remove card from reserved cards.
        
        Args:
            card (Card): The card to remove
        """
        self.reserved_cards.remove(card)

    
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
    
    def choose_tokens_to_return(self) -> dict[Token, int]:
        """Method to choose the combination of tokens to return when the player has over 10 tokens."""
        tokens = random.choice(self.get_possible_tokens_to_return())
        return tokens
    
    def calculate_real_price(self, card: Card) -> dict[Token, int]:
        """Given the player's current tokens and bonuses, what is the effective price of the card? 
        This includes yellows should the player's other tokens not cover the cost.
        
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
