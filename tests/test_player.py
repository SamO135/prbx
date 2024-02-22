import pytest
from tests.fixtures import *
from prbx_project.card import Card
from prbx_project.game_token import Token
from prbx_project.player import Player
from prbx_project.board import Board


def test_player_init():
    p = Player(name="test")
    assert p.name == "test"
    assert p.hand == []
    assert p.reserved_cards == []
    assert p.points == 0
    assert p.tokens == {Token.RED: 0, Token.BLUE: 0, Token.GREEN: 0, Token.WHITE: 0, Token.BLACK: 0, Token.YELLOW: 0}
    assert p.bonuses == {Token.RED: 0, Token.BLUE: 0, Token.GREEN: 0, Token.WHITE: 0, Token.BLACK: 0, Token.YELLOW: 0}


def test_get_buyable_cards(test_card_set: list[Card], test_player_tokens: dict[Token, int]):
    p = Player(name="test", tokens=test_player_tokens)

    buyable_cards = p.get_buyable_cards(cards=test_card_set)
    assert buyable_cards == [test_card_set[1], test_card_set[3]]

    # test using yellow tokens
    p.tokens = {Token.RED: 1, Token.BLUE: 1, Token.GREEN: 0, Token.WHITE: 0, Token.BLACK: 0, Token.YELLOW: 1}
    buyable_cards = p.get_buyable_cards(cards=test_card_set)
    assert buyable_cards == [test_card_set[1], test_card_set[2]]

    # test with player bonuses and using yellows
    p.bonuses = {Token.RED: 0, Token.BLUE: 0, Token.GREEN: 0, Token.WHITE: 1, Token.BLACK: 1, Token.YELLOW: 0}
    buyable_cards = p.get_buyable_cards(cards=test_card_set)
    assert buyable_cards == [test_card_set[1], test_card_set[2], test_card_set[3]]


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


def test_get_possible_moves(test_card_set: list[Card]):
    p = Player(name="test")
    board = Board()
    board.available_tokens = {Token.RED: 4, Token.GREEN: 4, Token.BLUE: 1, Token.WHITE: 0, Token.BLACK: 0, Token.YELLOW: 5}
    possible_moves = p.get_possible_moves(board.available_tokens, test_card_set)
    possible_moves_answer = [
        {"move_type": "reserve_card", "card": test_card_set[0], "returning": {}},
        {"move_type": "reserve_card", "card": test_card_set[1], "returning": {}},
        {"move_type": "reserve_card", "card": test_card_set[2], "returning": {}},
        {"move_type": "reserve_card", "card": test_card_set[3], "returning": {}},
        {'move_type': 'collect_tokens', 'tokens': {Token.RED: 2}, 'returning': {}},
        {'move_type': 'collect_tokens', 'tokens': {Token.GREEN: 2}, 'returning': {}},
        {'move_type': 'collect_tokens', 'tokens': {Token.RED: 1, Token.GREEN: 1, Token.BLUE: 1}, 'returning': {}},
        ]
    assert possible_moves == possible_moves_answer

    board.available_tokens = {Token.RED: 4, Token.GREEN: 4, Token.BLUE: 1, Token.WHITE: 0, Token.BLACK: 0, Token.YELLOW: 5}
    p.tokens = {Token.RED: 1, Token.GREEN: 1, Token.BLUE: 0, Token.WHITE: 2, Token.BLACK: 4, Token.YELLOW: 0}
    possible_moves = p.get_possible_moves(board.available_tokens, test_card_set)
    # possible_moves_answer = {"buy_card": [test_card_set[1], test_card_set[3]], "reserve_card": board.available_cards, "collect_tokens": p.get_token_collection_moves(board.available_tokens)}
    buy_card_moves = [
        {"move_type": "buy_card", "card": test_card_set[1]},
        {"move_type": "buy_card", "card": test_card_set[3]},
        ]
    possible_moves_answer = buy_card_moves + possible_moves_answer
    possible_moves_answer.pop(-1)
    # The move picks up a blue, so a blue can be returned
    possible_moves_answer.append({'move_type': 'collect_tokens', 'tokens': {Token.RED: 1, Token.GREEN: 1, Token.BLUE: 1}, 'returning': {Token.BLUE: 1}})
    possible_moves_answer.append({'move_type': 'collect_tokens', 'tokens': {Token.RED: 1, Token.GREEN: 1, Token.BLUE: 1}, 'returning': {Token.WHITE: 1}})
    possible_moves_answer.append({'move_type': 'collect_tokens', 'tokens': {Token.RED: 1, Token.GREEN: 1, Token.BLUE: 1}, 'returning': {Token.BLACK: 1}})
    possible_moves_answer.append({'move_type': 'collect_tokens', 'tokens': {Token.RED: 1, Token.GREEN: 1, Token.BLUE: 1}, 'returning': {Token.RED: 1}})
    possible_moves_answer.append({'move_type': 'collect_tokens', 'tokens': {Token.RED: 1, Token.GREEN: 1, Token.BLUE: 1}, 'returning': {Token.GREEN: 1}})

    assert all([move in possible_moves_answer for move in possible_moves]) # order of moves in the list may vary so "==" would not work


# how do you test randomness?
def test_select_random_move():
    pass


def test_collect_tokens():
    p = Player(name="test")
    p.collect_tokens(tokens={Token.RED: 1, Token.GREEN: 1, Token.BLACK: 1})
    assert p.tokens == {Token.RED: 1, Token.BLUE: 0, Token.GREEN: 1, Token.WHITE: 0, Token.BLACK: 1, Token.YELLOW: 0}

    p.collect_tokens(tokens={Token.WHITE: 2, Token.GREEN: 1})
    assert p.tokens == {Token.RED: 1, Token.BLUE: 0, Token.GREEN: 2, Token.WHITE: 2, Token.BLACK: 1, Token.YELLOW: 0}


def test_get_possible_tokens_to_return():
    # TEST 1
    p1 = Player(name="test1", tokens={Token.RED: 2, Token.BLUE: 0, Token.GREEN: 3, Token.WHITE: 2, Token.BLACK: 3, Token.YELLOW: 0})
    possible_tokens_to_return = p1.get_possible_tokens_to_return(additional_tokens={Token.RED: 1, Token.GREEN: 1})
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
    # converting the lists to frozensets so they can be compared even with a different ordering of elements
    possible_tokens_to_return_set = {frozenset(tuple(d.items()) for d in possible_tokens_to_return)}
    answer_set = {frozenset(tuple(d.items()) for d in answer)}
    assert possible_tokens_to_return_set == answer_set

    # TEST 2
    p1 = Player(name="test2", tokens={Token.RED: 2, Token.BLUE: 0, Token.GREEN: 3, Token.WHITE: 0, Token.BLACK: 0, Token.YELLOW: 0})
    possible_tokens_to_return = p1.get_possible_tokens_to_return()
    answer = [{}]
    assert possible_tokens_to_return == answer


def test_remove_tokens():
    p = Player(name="test", tokens={Token.RED: 2, Token.BLUE: 2, Token.GREEN: 2, Token.WHITE: 3, Token.BLACK: 1, Token.YELLOW: 2})
    p.remove_tokens(tokens={Token.RED: 1, Token.GREEN: 1, Token.BLACK: 1})
    assert p.tokens == {Token.RED: 1, Token.BLUE: 2, Token.GREEN: 1, Token.WHITE: 3, Token.BLACK: 0, Token.YELLOW: 2}

    with pytest.raises(ValueError):
        p.remove_tokens(tokens={Token.RED: 2})


def test_reserve_card(test_card_set: list[Card]):
    p = Player(name="test")
    p.reserve_card(test_card_set[0])
    assert p.reserved_cards == [test_card_set[0]]

    p.reserve_card(test_card_set[1])
    p.reserve_card(test_card_set[2])
    assert p.reserved_cards == test_card_set[:3]

    with pytest.raises(ValueError):
        p.reserve_card(test_card_set[3])


def test_remove_reserved_card(test_card_set: list[Card]):
    p = Player(name="test")
    p.reserved_cards = [test_card_set[0], test_card_set[1]]
    p.remove_reserved_card(test_card_set[0])
    assert p.reserved_cards == [test_card_set[1]]

    with pytest.raises(ValueError):
        p.remove_reserved_card(test_card_set[0])


# def test_choose_tokens_to_return():
#     pass


def test_calculate_real_price(test_card_set: list[Card]):
    card = test_card_set[0] # price={Token.RED: 2, Token.BLUE: 3, Token.GREEN: 2, Token.WHITE: 0, Token.BLACK: 0}

    p = Player(name="test", bonuses={Token.RED: 1, Token.BLUE: 2, Token.GREEN: 0, Token.WHITE: 0, Token.BLACK: 0, Token.YELLOW: 0})
    real_price = p.calculate_real_price(card)
    assert real_price == {Token.RED: 0, Token.BLUE: 0, Token.GREEN: 0, Token.WHITE: 0, Token.BLACK: 0, Token.YELLOW: 4}

    p.tokens = {Token.RED: 2, Token.BLUE: 2, Token.GREEN: 2, Token.WHITE: 2, Token.BLACK: 2, Token.YELLOW: 0}
    real_price = p.calculate_real_price(card)
    assert real_price == {Token.RED: 1, Token.BLUE: 1, Token.GREEN: 2, Token.WHITE: 0, Token.BLACK: 0, Token.YELLOW: 0}


# def test_get_payment_combinations(test_card_set):
#     card = test_card_set[0] # price={Token.RED: 2, Token.BLUE: 3, Token.GREEN: 2, Token.WHITE: 0, Token.BLACK: 0}
#     p = Player(name="test", tokens={Token.RED: 2, Token.BLUE: 1, Token.GREEN: 2, Token.WHITE: 0, Token.BLACK: 0, Token.YELLOW: 2})
#     real_price = p.calculate_real_price(card)
#     payment_combinations = p.get_payment_combinations(real_price)
#     for payment in payment_combinations:
#         print(f"payment: {payment}")
#     assert False

