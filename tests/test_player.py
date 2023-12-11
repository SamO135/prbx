import pytest
from prbx_project.card import Card
from prbx_project.settings import Token
from prbx_project.player import Player


def test_player_init():
    pass


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
    
    p = Player(name="test", tokens={Token.RED: 3, Token.BLUE: 0, Token.GREEN: 2, Token.WHITE: 2, Token.BLACK: 2, Token.YELLOW: 0})

    buyable_cards = p.get_buyable_cards(cards=cards)
    assert buyable_cards == [cards[1], cards[3]]


def test_get_token_collection_moves():
    available_tokens = {Token.RED: 4, Token.BLUE: 0, Token.GREEN: 4, Token.WHITE: 1, Token.BLACK: 3, Token.YELLOW: 3}
    p = Player(name="test")

    token_collection_moves = p.get_token_collection_moves(available_tokens)

    assert token_collection_moves == [{Token.RED: 2}, 
                                      {Token.GREEN: 2}, 
                                      {Token.RED: 1, Token.GREEN: 1, Token.WHITE: 1}, 
                                      {Token.RED: 1, Token.GREEN: 1, Token.BLACK: 1},
                                      {Token.RED: 1, Token.WHITE: 1, Token.BLACK: 1},
                                      {Token.BLACK: 1, Token.GREEN: 1, Token.WHITE: 1}]


def test_get_possible_moves():
    pass


# how do you test randomness?
def test_select_random_move():
    pass


def test_collect_tokens():
    pass


def test_get_possible_tokens_to_return():
    # TEST 1
    p1 = Player(name="test1", tokens={Token.RED: 3, Token.BLUE: 0, Token.GREEN: 4, Token.WHITE: 2, Token.BLACK: 3, Token.YELLOW: 0})
    possible_tokens_to_return = p1.get_possible_tokens_to_return()
    answer = [
        {Token.RED: 2}, 
        {Token.GREEN: 2}, 
        {Token.WHITE: 2}, 
        {Token.BLACK: 2},
        {Token.RED: 1, Token.GREEN: 1},
        {Token.RED: 1, Token.WHITE: 1},
        {Token.RED: 1, Token.BLACK: 1},
        {Token.GREEN: 1, Token.WHITE: 1},
        {Token.GREEN: 1, Token.BLACK: 1},
        {Token.WHITE: 1, Token.BLACK: 1},
    ]
    # convert the lists to frozensets so they can be compared even with a different ordering of elements
    possible_tokens_to_return_set = {frozenset(tuple(d.items()) for d in possible_tokens_to_return)}
    answer_set = {frozenset(tuple(d.items()) for d in answer)}
    assert possible_tokens_to_return_set == answer_set

    # TEST 2
    p1 = Player(name="test2", tokens={Token.RED: 2, Token.BLUE: 0, Token.GREEN: 3, Token.WHITE: 0, Token.BLACK: 0, Token.YELLOW: 0})
    possible_tokens_to_return = p1.get_possible_tokens_to_return()
    answer = []
    assert possible_tokens_to_return == answer