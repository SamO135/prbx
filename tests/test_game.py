import pytest
from tests.fixtures import test_game_setup
from prbx_project.game import Game
from prbx_project.settings import Token


def test_game_init(test_game_setup: Game):
    game = test_game_setup
    board = game.board
    assert len(board.available_cards) == 12
    assert board.available_tokens == {Token.RED: 4, Token.BLUE: 4, Token.GREEN: 4,
                                      Token.WHITE: 4, Token.BLACK: 4, Token.YELLOW: 5}
    assert game.current_player == game.players[0]
    assert game.max_points == 15


def test_is_over():
    pass


def test_get_winner():
    pass


def test_replace_card():
    pass


def test_collect_tokens():
    pass


def test_reserve_card():
    pass


def test_buy_card():
    pass