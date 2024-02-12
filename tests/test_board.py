import pytest
from tests.fixtures import *
from prbx_project.all_cards import all_cards
from prbx_project.board import Board


def test_board_init():
    board = Board()
    assert len(board.all_cards[0]) == len(all_cards[0]) - 4
    assert len(board.all_cards[1]) == len(all_cards[1]) - 4
    assert len(board.all_cards[2]) == len(all_cards[2]) - 4

    assert board.available_tokens == {Token.RED: 4, Token.GREEN: 4, Token.BLUE: 4, Token.WHITE: 4, Token.BLACK: 4, Token.YELLOW: 5}
    assert len(board.available_cards) == 12
    all_cards_flattened = board.all_cards[0] + board.all_cards[1] + board.all_cards[2]
    assert any([card in all_cards_flattened for card in board.available_cards]) == False


def test_remove_tokens():
    board = Board()
    board.remove_tokens({Token.RED: 1, Token.GREEN: 0, Token.BLUE: 0, Token.WHITE: 0, Token.BLACK: 0, Token.YELLOW: 0})
    assert board.available_tokens == {Token.RED: 3, Token.GREEN: 4, Token.BLUE: 4, Token.WHITE: 4, Token.BLACK: 4, Token.YELLOW: 5}

    board = Board()
    board.remove_tokens({Token.RED: 4, Token.GREEN: 4, Token.BLUE: 4, Token.WHITE: 4, Token.BLACK: 4, Token.YELLOW: 5})
    assert board.available_tokens == {Token.RED: 0, Token.GREEN: 0, Token.BLUE: 0, Token.WHITE: 0, Token.BLACK: 0, Token.YELLOW: 0}

    with pytest.raises(ValueError):
        board = Board()
        board.remove_tokens({Token.RED: 5, Token.GREEN: 0, Token.BLUE: 0, Token.WHITE: 0, Token.BLACK: 0, Token.YELLOW: 0})
    
    with pytest.raises(ValueError):
        board = Board()
        board.remove_tokens({Token.RED: -1, Token.GREEN: 0, Token.BLUE: 0, Token.WHITE: 0, Token.BLACK: 0, Token.YELLOW: 0})



def test_receive_tokens():
    board = Board()
    board.recieve_tokens({Token.RED: 1, Token.GREEN: 0, Token.BLUE: 0, Token.WHITE: 0, Token.BLACK: 0, Token.YELLOW: 0})
    assert board.available_tokens == {Token.RED: 5, Token.GREEN: 4, Token.BLUE: 4, Token.WHITE: 4, Token.BLACK: 4, Token.YELLOW: 5}

    board = Board()
    board.recieve_tokens({Token.RED: 1, Token.GREEN: 2, Token.BLUE: 3, Token.WHITE: 1, Token.BLACK: 2, Token.YELLOW: 1})
    assert board.available_tokens == {Token.RED: 5, Token.GREEN: 6, Token.BLUE: 7, Token.WHITE: 5, Token.BLACK: 6, Token.YELLOW: 6}

    with pytest.raises(ValueError):
        board = Board()
        board.recieve_tokens({Token.RED: -1, Token.GREEN: 0, Token.BLUE: 0, Token.WHITE: 0, Token.BLACK: 0, Token.YELLOW: 0})


def test_remove_card():
    board = Board()
    card = board.available_cards[0]
    board.remove_card(card)
    assert card not in board.available_cards
    assert len(board.available_cards) == 11

    with pytest.raises(ValueError):
        board.remove_card(card)


def test_add_new_card():
    board = Board()
    old_card = board.available_cards[0]
    board.remove_card(old_card)
    assert old_card not in board.all_cards[old_card.tier-1]
    new_card = board.add_new_card(old_card.tier-1)
    assert new_card in board.available_cards
    assert new_card not in board.all_cards[old_card.tier-1]
    assert old_card != new_card