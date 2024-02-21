from prbx_project.node import Node
from prbx_project.gamestate import GameState
from datetime import datetime, timedelta
import copy

def tree_policy(node: Node):
    pass

def selection(current_node: Node) -> Node:
    while current_node.children:
        max_tree_policy_value = 0
        for child in current_node.children:
            tree_policy_value = tree_policy(child)
            if tree_policy_value > max_tree_policy_value:
                best_child = child
                max_tree_policy_value = tree_policy_value
        current_node = best_child
    return current_node

def expansion(current_node: Node) -> Node:
    available_tokens = current_node.gamestate.board.available_tokens
    available_cards = current_node.gamestate.board.available_cards
    possible_moves = current_node.gamestate.current_player.get_possible_moves(available_tokens, available_cards)
    children = []
    for move in possible_moves:
        gamestate_copy = copy.deepcopy(current_node.gamestate)
        new_gamestate = gamestate_copy.play_move(move)
        new_child = Node(parent=current_node, action=move, gamestate=new_gamestate, children=[], value=0, num_visits=0)
        children.append(new_child)
    current_node.children = children

def rollout(current_node: Node) -> int:
    pass

def back_propagate(current_node: Node, value: int) -> Node:
    pass

def mcts(current_node: Node) -> Node:
    # selection
    next_node = selection(current_node)

    # expansion
    if next_node.num_visits > 0:
        next_node = expansion(next_node)

    # rollout
    terminal_value = rollout(next_node)

    # backpropagation
    back_propagate(next_node, terminal_value)
    return current_node

def select_move_with_mcts(current_node: Node):
    print("TEST")
    start_time = datetime.utcnow()
    while datetime.utcnow() - start_time < timedelta(seconds=1):
        current_node = mcts(current_node)

    # calculate best child
    for child in current_node.children:
        max_tree_policy_value = 0
        tree_policy_value = tree_policy(child)
        if tree_policy_value > max_tree_policy_value:
            best_child = child
            max_tree_policy_value = tree_policy_value

    return best_child.action

"""
-- SELECTION --
while current_node has children
calculate the next_node using the tree policy (e.g. UCB1)
-- SELECTION --

if next_node has been visited before

-- EXPANSION --
add new state as a child for each available action
-- EXPANSION --

elif next_node has not been visted before
perform rollout

-- ROLLOUT --
while node does not represent terminal state
pick random action from possible action
perform action to arrive at new node

-- BACKPROPAGATION --
calculate value of terminal node
use value to estimate value of initial node of rollout
"""
