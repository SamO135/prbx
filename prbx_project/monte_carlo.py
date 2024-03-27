from prbx_project.node import Node
from prbx_project.player import Player
from datetime import datetime, timedelta
import copy
import math
import random
import yaml


with open("prbx_project/config.yaml") as file:
        config = yaml.safe_load(file)

def tree_policy(node: Node) -> float:
    try:
        return (node.value + 2 * (math.log(node.parent.num_visits) / node.num_visits))
    except Exception as e:
        # print(type(e))
        return 1000

def selection(current_node: Node) -> Node:
    while current_node.children:
        max_tree_policy_value = tree_policy(current_node.children[0]) - 1
        for child in current_node.children:
            tree_policy_value = tree_policy(child)
            if tree_policy_value > max_tree_policy_value:
                best_child1 = child
                max_tree_policy_value = tree_policy_value
        try:
            current_node = best_child1
        except Exception as e:
            print(f"Error in selection method: {e}")
            quit()
    return current_node

def expansion(current_node: Node, sample_size: int=-1, weights: list[int]=[1, 1, 1]) -> Node:
    if sample_size < -1 or sample_size == 0:
        raise ValueError("Invalid number of samples chosen for expansion.")
    available_tokens = current_node.gamestate.board.available_tokens
    available_cards = current_node.gamestate.board.available_cards
    possible_moves = current_node.gamestate.current_player.get_possible_moves(available_tokens, available_cards, reduced=config["reduced"])
    if sample_size > 0:
        sampled_moves = sample_moves(possible_moves, k=sample_size, weights=weights)
    else:
        sampled_moves = possible_moves
    children = []
    for move in sampled_moves:
        gamestate_copy = copy.deepcopy(current_node.gamestate)
        new_gamestate = gamestate_copy.play_move(move, log=False)
        new_gamestate.next_player()
        new_child = Node(parent=current_node, action=move, gamestate=new_gamestate, children=[], value=0, num_visits=0)
        children.append(new_child)
    current_node.children = children
    return current_node

# random playout simulation
def rollout(current_node: Node, pov: Player) -> Node:
    game = copy.deepcopy(current_node.gamestate)
    while not game.is_over():
        for _ in game.players:
            # Select move
            try:
                all_moves = game.current_player.get_possible_moves(game.board.available_tokens, game.board.available_cards, reduced=config["reduced"])
                player_move = game.current_player.select_random_move(all_moves)
                game.current_player.locked = False
            except Exception as e:
                game.current_player.locked = True
                if (all([player.locked for player in game.players])):
                    game.force_end = True
                    break
                game.next_player()
                continue

            # Play move
            try:
                game.play_move(player_move, log=False)
                game.next_player()
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

def select_move_with_mcts(current_node: Node, mcts_budget: int):
    # if current_node.children == []:
    possible_moves = current_node.gamestate.current_player.get_possible_moves(current_node.gamestate.board.available_tokens, current_node.gamestate.board.available_cards, reduced=config["reduced"])
    if len(possible_moves) == 0:
        raise ValueError("Cannot select a move from a node with no children")
    current_node = copy.deepcopy(current_node)
    current_node.gamestate.players.reverse()
    if config["time_limit"]:
        start_time = datetime.utcnow()
        while datetime.utcnow() - start_time < timedelta(seconds=mcts_budget):
            current_node = mcts(current_node)
    else:
        for _ in range(mcts_budget):
            current_node = mcts(current_node)


    # calculate best child
    max_tree_policy_value = tree_policy(current_node.children[0]) - 1
    for child in current_node.children:
        tree_policy_value = tree_policy(child)
        if tree_policy_value > max_tree_policy_value:
            best_child2 = child
            max_tree_policy_value = tree_policy_value
    try:
        return best_child2.action
    except Exception as e:
        if len(current_node.children) == 0:
            raise ValueError("Cannot select a move from an empty list")
        else:
            print(f"Error in 'select_move_with_mcts': {e}")
            quit()
        # print(f"number of children: {len(current_node.children)}")
        # print(current_node)
        # print(f"Error in other select_move_with_mcts: best_child={best_child2}.")
        # quit()

def sample_moves(all_moves: list[dict], k: int, weights: list[int]=[1, 1, 1]) -> list[dict]:
    """Sample a list of moves.
    
    Args:
        all_moves (list[dict]): The list of possible moves to be sampled
        k (int): The number of moves to sample. If k >= total moves, it will just return total moves
        weights (list[int]): The relative likelihood to sample each move type. First number is for 'buy_card', 
        second number is for 'reserve_card' and third number is for 'collect_tokens'. Defaults to equal chance i.e. [1, 1, 1]
        
    Return:
        list[dict]: The list of sampled moves"""
    if k >= len(all_moves):
        return all_moves
    w = []
    unique_sampled_moves = []
    for move in all_moves:
        if move["move_type"] == "buy_card":
            w.append(weights[0])
        elif move["move_type"] == "reserve_card":
            w.append(weights[1])
        else: # move_type = collect_tokens
            w.append(weights[2])
    while len(unique_sampled_moves) < k:
        sampled_moves = random.choices(all_moves, weights=w, k=(k-len(unique_sampled_moves)))
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
