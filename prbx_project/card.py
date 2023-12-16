from pydantic import BaseModel
from prbx_project.settings import Token
import random

class Card(BaseModel):
    """A class representing a development card."""

    id: int = 0
    points: int
    bonus: Token
    price: dict[Token, int]
    tier: int # Tier 1 is cheapest Tier 3 is most expensive


    # Modify this so the generated price matches the card's tier.
    # def create_price() -> dict[Token, int]:
    #     """Create a random price for the card.
        
    #     Return:
    #         dict[Token, int]: A dictionary containing the price of the card
    #     """
    #     values = [random.randint(0, 3) for i in range(4)]
    #     tokens = [token for token in Token]
    #     tokens.remove(Token.YELLOW)
    #     tokens.remove(random.choice(tokens))
    #     price = dict(zip(tokens, values))
    #     return {key: value for key, value in price.items() if value != 0}
        

    # @classmethod
    # def new_card(cls, tier=1):
    #     """A factory method to create new cards.
        
    #     Return:
    #         Card: A new card object
    #     """
    #     id = random.randint(1, 1000)
    #     points = random.randint(0, 4)
    #     tokens = list(Token)
    #     tokens.remove(Token.YELLOW)
    #     bonus = random.choice(tokens)
    #     # Generate price
    #     price = Card.create_price()
    #     return Card(id = id, points=points, bonus=bonus, price=price, tier=1)
    
