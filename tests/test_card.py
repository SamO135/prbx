import pytest
from prbx_project.card import Card
from prbx_project.game_token import Token


def test_card_init():
    card = Card(points=2, 
                bonus=Token.BLACK, 
                price={Token.RED: 2, Token.GREEN: 2, Token.BLUE: 3, Token.WHITE: 0, Token.BLACK: 0, Token.YELLOW: 0}, 
                tier=1)
    
    assert card.points == 2
    assert card.bonus == Token.BLACK
    assert card.price == {Token.RED: 2, Token.GREEN: 2, Token.BLUE: 3, Token.WHITE: 0, Token.BLACK: 0, Token.YELLOW: 0}
    assert card.tier == 1
