import pytest
from prbx_project.card import Card
from prbx_project.settings import Token
from prbx_project.player import Player


def test_get_buyable_cards():
    cards = [Card(id=289, 
                  points=2, 
                  bonus=Token.BLACK, 
                  price={Token.RED: 2, Token.BLUE: 3, Token.GREEN: 2}, 
                  tier=1), 
            Card(id=796, 
                 points=3, 
                 bonus=Token.YELLOW, 
                 price={Token.RED: 1, Token.GREEN: 1}, 
                 tier=1), 
            Card(id=734, 
                 points=2, 
                 bonus=Token.WHITE, 
                 price={Token.BLUE: 2}, tier=1), 
            Card(id=306, 
                 points=1, 
                 bonus=Token.WHITE, 
                 price={Token.RED: 1, Token.WHITE: 1, Token.BLACK: 2}, 
                 tier=1)]
    
    p = Player(tokens={Token.RED: 3, Token.BLUE: 0, Token.GREEN: 2, Token.WHITE: 2, Token.BLACK: 2, Token.YELLOW: 0})
    print(p.tokens)

    buyable_cards = p.get_buyable_cards(cards=cards)
    assert buyable_cards == [cards[1], cards[3]]
