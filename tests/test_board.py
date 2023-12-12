import pytest
from tests.fixtures import *
from prbx_project.board import Board

def test_board_init():
    pass


def test_remove_tokens():
    pass


def test_receive_tokens():
    pass


def test_replace_card():
    board = Board()
    card_to_replace = board.available_cards[0]
    board.replace_card(card_to_replace)

    assert card_to_replace not in board.available_cards
    assert len(board.available_cards) == 12