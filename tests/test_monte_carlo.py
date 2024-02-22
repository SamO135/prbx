import pytest
from tests.fixtures import *
from tests.fixtures import test_game_setup as game
from prbx_project.node import Node
from prbx_project.monte_carlo import *
from prbx_project.player import Player

def test_expansion(game: GameState):
    node = Node(parent=None, action={}, gamestate=game, children=[], value=0, num_visits=0)
    new_node = expansion(node)
    possible_moves = game.current_player.get_possible_moves(game.board.available_tokens, game.board.available_cards)
    for index, move in enumerate(possible_moves):
        assert move == node.children[index].action
    new_node.children = []
    assert new_node == node

    