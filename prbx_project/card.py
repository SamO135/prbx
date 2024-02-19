from pydantic import BaseModel
from prbx_project.game_token import Token

class Card(BaseModel):
    """A class representing a development card."""

    id: int = 0
    points: int
    bonus: Token
    price: dict[Token, int]
    tier: int # Tier 1 is cheapest Tier 3 is most expensive
