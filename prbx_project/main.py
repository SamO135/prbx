from prbx_project.gamestate import GameState
from prbx_project.player import Player
from prbx_project.board import Board
from prbx_project.node import Node
from prbx_project.monte_carlo import select_move_with_mcts, expansion
from prbx_project.stats import Stats
from collections import Counter
import yaml

def play_round(current_node: Node):
    for current_player in current_node.gamestate.players:
        # Select move
        try:
            match current_player.name:
                case "random":
                    all_moves = current_player.get_possible_moves(current_node.gamestate.board.available_tokens, current_node.gamestate.board.available_cards, reduced=config["reduced"])
                    player_move = current_player.select_random_move(all_moves)
                case "mcts_vanilla":
                    current_node = expansion(current_node, sample_size=config["sample_size"], weights=config["sample_weights"])
                    player_move = select_move_with_mcts(current_node, config["mcts_budget"])
                case "mcts_rave":
                    current_node = expansion(current_node, sample_size=config["sample_size"], weights=config["sample_weights"])
                    player_move = select_move_with_mcts(current_node, config["mcts_budget"], enhancement="rave")
            current_node.gamestate.current_player.locked = False
        except Exception as e:
            # print(e)
            current_node.gamestate.current_player.locked = True
            if (all([player.locked for player in current_node.gamestate.players])):
                if config["logs"]:
                    print("NO LEGAL MOVES FOR EITHER PLAYER, FORCE ENDING GAME")
                current_node.gamestate.force_end = True
                break
            else:
                if config["logs"]:
                    print(f"NO LEGAL MOVES FOR {current_node.gamestate.current_player.name}")
            current_node.gamestate.next_player()
            continue

        # Play move
        try:
            current_node.gamestate.play_move(player_move, log=config["logs"])
            current_node.gamestate.next_player()
        except:
            pass
        current_node = Node(parent=None, action=player_move, gamestate=current_node.gamestate, children=[], value=0, num_visits=0)

    return current_node


if __name__ == "__main__":
    with open("prbx_project/config.yaml") as file:
        config = yaml.safe_load(file)

    winner_list = []
    draws = 0
    avg_num_turns = 0
    discarded_games = 0
    elapsed_simulations = 1
    sum_avg_rollouts = 0
    stats = Stats()
    while elapsed_simulations <= config["simulations"]:
        stats.reset_stats()
        print(f"-- Simulation {elapsed_simulations} --")
        player1 = Player(name=config["player1_alg"])
        player2 = Player(name=config["player2_alg"])

        gamestate = GameState(board=Board(), players=[player1, player2])

        # GENERAL GAMEPLAY LOOP
        turn_count = 0
        current_node = Node(parent=None, action={}, gamestate=gamestate, children=[], value=0, num_visits=0) # root node
        while (not gamestate.is_over()):
            current_node = play_round(current_node)
            turn_count += 1


        # Game has finished
        if not gamestate.force_end:
            elapsed_simulations += 1
            winner = gamestate.get_winner()
            avg_num_turns += turn_count
            avg_rollouts = stats.rollouts/turn_count
            sum_avg_rollouts += avg_rollouts
            if winner == None:
                draws += 1
            else:
                winner_list.append(winner.name)
                print(f"winner: {winner.name}")
                if config["logs"]:
                    print(f"average rollouts: {avg_rollouts}")
        else:
            print("discarded game")
            discarded_games += 1



# Print statistics
print()
win_counts = Counter(winner_list)
if len(win_counts) == 1:
    if config["player1_alg"] in win_counts.keys():
        win_counts[config["player2_alg"]] = 0
    else:
        win_counts[config["player1_alg"]] = 0

for alg, wins in win_counts.items():
    print(f"{alg} won {wins} time{'s' if wins !=1 else ''}")
if draws > 0:
    print(f"there were {draws} draws")
print()

avg_num_turns = avg_num_turns / (config["simulations"] - discarded_games)
print(f"Average number of turns per simulation: {avg_num_turns}")
print(f"average rollouts per search phase: {sum_avg_rollouts/config["simulations"]}")
print(f"Number of discarded games: {discarded_games}")