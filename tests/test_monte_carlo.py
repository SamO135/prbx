import pytest
from tests.fixtures import *
from tests.fixtures import test_game_setup as game, test_game_tree as game_tree
from prbx_project.node import Node
from prbx_project.monte_carlo import *
from prbx_project.player import Player

def test_selection(game_tree: Node):
    selected_node = selection(game_tree)
    assert selected_node == game_tree.children[0].children[0]

def test_expansion(game: GameState):
    node = Node(parent=None, action={}, gamestate=game, children=[], value=0, num_visits=0)
    new_node = expansion(node)
    possible_moves = game.current_player.get_possible_moves(game.board.available_tokens, game.board.available_cards)
    for index, move in enumerate(possible_moves):
        assert move == node.children[index].action
    new_node.children = []
    assert new_node.gamestate == node.gamestate
    assert new_node == node

def test_back_propagate(game_tree: Node):
    rollout_node = game_tree.children[0].children[0]
    rollout_node.value = 0
    rollout_node.num_visits = 0
    terminal_value = 12
    parent_value_old  = rollout_node.parent.value
    parent_num_visits_old = rollout_node.parent.num_visits
    grandparent_value_old = rollout_node.parent.parent.value
    grandparent_num_visits_old = rollout_node.parent.parent.num_visits
    rollout_node = back_propagate(rollout_node, terminal_value)
    assert rollout_node.value == terminal_value
    assert rollout_node.num_visits == 1
    assert rollout_node.parent.value == parent_value_old + terminal_value
    assert rollout_node.parent.num_visits == parent_num_visits_old + 1
    assert rollout_node.parent.parent.value == grandparent_value_old + terminal_value
    assert rollout_node.parent.parent.num_visits ==  grandparent_num_visits_old + 1
    
def test_rollout(game_tree: Node):
    rollout_node = selection(game_tree)
    rollout_node_copy = copy.deepcopy(rollout_node)
    assert rollout_node.gamestate == rollout_node_copy.gamestate
    terminal_node = rollout(rollout_node)
    assert rollout_node.gamestate == rollout_node_copy.gamestate
    assert terminal_node.gamestate.is_over()