import pytest
from prbx_project.card import Card
from prbx_project.settings import Token
from prbx_project.player import Player
from prbx_project.game import Game
from prbx_project.board import Board

{Token.RED: 3, Token.GREEN: 0, Token.BLUE: 3, Token.WHITE: 5, Token.BLACK: 3}
@pytest.fixture
def test_card_set():
    cards = [Card(id=289, 
                  points=2, 
                  bonus=Token.BLACK, 
                  price={Token.RED: 2, Token.GREEN: 2, Token.BLUE: 3, Token.WHITE: 0, Token.BLACK: 0}, 
                  tier=1), 
            Card(id=796, 
                 points=3, 
                 bonus=Token.YELLOW, 
                 price={Token.RED: 1, Token.GREEN: 1, Token.BLUE: 0, Token.WHITE: 0, Token.BLACK: 0}, 
                 tier=2), 
            Card(id=734, 
                 points=2, 
                 bonus=Token.WHITE, 
                 price={Token.RED:  0, Token.GREEN: 0, Token.BLUE: 2, Token.WHITE: 0, Token.BLACK: 0}, tier=1), 
            Card(id=306, 
                 points=1, 
                 bonus=Token.WHITE, 
                 price={Token.RED: 1, Token.GREEN: 0, Token.BLUE: 0, Token.WHITE: 1, Token.BLACK: 2}, 
                 tier=1)]
    return cards

@pytest.fixture
def test_player_tokens():
    tokens = {Token.RED: 3, Token.BLUE: 0, Token.GREEN: 2, Token.WHITE: 2, Token.BLACK: 2, Token.YELLOW: 0}
    return tokens


@pytest.fixture
def test_game_setup():
    """Game setup for a 2 player game."""
    player1 = Player(name="player1")
    player2 = Player(name="player2")
    game = Game(board=Board(), players=[player1, player2])
    return game