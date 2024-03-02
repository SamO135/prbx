from prbx_project.node import Node
from prbx_project.player import Player
from datetime import datetime, timedelta
import copy
import math
import random


def tree_policy(node: Node) -> float:
    try:
        return (node.value + 2 * (math.log(node.parent.num_visits) / node.num_visits))
    except Exception as e:
        # print(type(e))
        return 1000

def selection(current_node: Node) -> Node:
    while current_node.children:
        max_tree_policy_value = -1000
        for child in current_node.children:
            tree_policy_value = tree_policy(child)
            if tree_policy_value > max_tree_policy_value:
                best_child = child
                max_tree_policy_value = tree_policy_value
        try:
            current_node = best_child
        except:
            print("Error in selection method.")
            quit()
    return current_node

def expansion(current_node: Node) -> Node:
    available_tokens = current_node.gamestate.board.available_tokens
    available_cards = current_node.gamestate.board.available_cards
    possible_moves = current_node.gamestate.current_player.get_possible_moves(available_tokens, available_cards)
    # sampled_moves = sample_moves(possible_moves, k=10)
    children = []
    for move in possible_moves:
        gamestate_copy = copy.deepcopy(current_node.gamestate)
        new_gamestate = gamestate_copy.play_move(move, log=False)
        new_child = Node(parent=current_node, action=move, gamestate=new_gamestate, children=[], value=0, num_visits=0)
        children.append(new_child)
    current_node.children = children
    return current_node

# random playout simulation
def rollout(current_node: Node, pov: Player) -> Node:
    game = copy.deepcopy(current_node.gamestate)
    while not game.is_over():
        for _ in game.players:
            try:
                all_moves = game.current_player.get_possible_moves(game.board.available_tokens, game.board.available_cards)
                player_move = game.current_player.select_random_move(all_moves)
                game.current_player.locked = False
            except Exception as e:
                # print(e)
                game.current_player.locked = True
                if (all([player.locked for player in game.players])):
                    # print("NO LEGAL MOVES FOR EITHER PLAYER, FORCE ENDING GAME")
                    game.force_end = True
                    break
                # else:
                    # print(f"NO LEGAL MOVES FOR {game.current_player.name}")
                game.next_player()
                continue

            # Play move
            try:
                game.play_move(player_move, log=False)
            except Exception as e:
                print(f"Couldn't play the move. Error: {e}")
            current_node = Node(parent=None, action=player_move, gamestate=game, children=[], value=0, num_visits=0)

            # Enumerate children for initial node of MCTS
            # if game.current_player.name == "mcts_agent":
            #     current_node = expansion(current_node)
    current_node.calculate_value(pov)
    return current_node

def back_propagate(current_node: Node, terminal_value: int) -> Node:
    rollout_node = current_node
    while current_node:
        current_node.value += terminal_value
        current_node.num_visits += 1
        current_node = current_node.parent
    return rollout_node

def mcts(current_node: Node) -> Node:
    # selection
    next_node = selection(current_node)

    # expansion
    if next_node.num_visits > 0:
        next_node = expansion(next_node)
        next_node = selection(next_node)

    # rollout
    terminal_node = rollout(next_node, current_node.gamestate.current_player)

    # backpropagation
    next_node = back_propagate(next_node, terminal_node.value)
    return current_node

def select_move_with_mcts(current_node: Node):
    current_node = copy.deepcopy(current_node)
    current_node.gamestate.players.reverse()
    # start_time = datetime.utcnow()
    # while datetime.utcnow() - start_time < timedelta(seconds=0.5):
    for i in range(len(current_node.children)):
        current_node = mcts(current_node)


    # calculate best child
    max_tree_policy_value = -1000
    for child in current_node.children:
        tree_policy_value = tree_policy(child)
        if tree_policy_value > max_tree_policy_value:
            best_child = child
            max_tree_policy_value = tree_policy_value
    try:
        return best_child.action
    except:
        print(f"Error in other method: best_child={best_child}.")
        quit()

def sample_moves(all_moves: list[dict], k: int) -> list[dict]:
    """Sample a list of moves.
    
    Args:
        all_moves (list[dict]): The list of possible moves to be sampled
        k (int): The number of moves to sample
        
    Return:
        list[dict]: The list of sampled moves"""
    if k > len(all_moves):
        k = len(all_moves)
    weights = []
    unique_sampled_moves = []
    for move in all_moves:
        if move["move_type"] == "buy_card":
            weights.append(100)
        else:
            weights.append(1)
    while len(unique_sampled_moves) < k:
        sampled_moves = random.choices(all_moves, weights=weights, k=(k-len(unique_sampled_moves)))
        for move in sampled_moves:
            if move not in unique_sampled_moves:
                unique_sampled_moves.append(move)

    return unique_sampled_moves
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
