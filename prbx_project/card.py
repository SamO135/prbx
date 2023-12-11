from pydantic import BaseModel
from prbx_project.settings import Token
import random

class Card(BaseModel):
    id: int
    points: int
    bonus: Token
    price: dict[Token, int]
    tier: int # Tier 1 is cheapest Tier 3 is most expensive


    # Modify this so the generated price matches the card's tier.
    def create_price() -> dict[Token, int]:
        values = [random.randint(0, 3) for i in range(4)]
        tokens = [token for token in Token]
        tokens.remove(Token.YELLOW)
        tokens.remove(random.choice(tokens))
        price = dict(zip(tokens, values))
        return {key: value for key, value in price.items() if value != 0}
        

    @classmethod
    def new_card(self):
        id = random.randint(1, 1000)
        points = random.randint(0, 4)
        bonus = random.choice(list(Token))
        # Generate price
        price = Card.create_price()
        return Card(id = id, points=points, bonus=bonus, price=price, tier=1)
    
