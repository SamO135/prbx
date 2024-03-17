from prbx_project.gamestate import GameState
from prbx_project.player import Player
from prbx_project.board import Board
from prbx_project.node import Node
from prbx_project.monte_carlo import select_move_with_mcts, expansion
from collections import Counter
import sys
import copy

def play_round(current_node: Node):
    for current_player in current_node.gamestate.players:
        # Select move
        try:
            match current_player.name:
                case "random":
                    all_moves = current_player.get_possible_moves(current_node.gamestate.board.available_tokens, current_node.gamestate.board.available_cards)
                    player_move = current_player.select_random_move(all_moves)
                case "mcts_vanilla":
                    player_move = select_move_with_mcts(current_node)
            current_node.gamestate.current_player.locked = False
        except Exception as e:
            print(e)
            current_node.gamestate.current_player.locked = True
            if (all([player.locked for player in current_node.gamestate.players])):
                print("NO LEGAL MOVES FOR EITHER PLAYER, FORCE ENDING GAME")
                current_node.gamestate.force_end = True
                break
            else:
                print(f"NO LEGAL MOVES FOR {current_node.gamestate.current_player.name}")
            current_node.gamestate.next_player()
            continue

        # Play move
        try:
            current_node.gamestate.play_move(player_move, log=True)
        except:
            pass
        current_node = Node(parent=None, action=player_move, gamestate=current_node.gamestate, children=[], value=0, num_visits=0)

        # Enumerate children for initial node of MCTS
        if current_node.gamestate.current_player.name == "mcts_vanilla":
            current_node = expansion(current_node)
    return current_node


if __name__ == "__main__":
    simulations = int(sys.argv[1])
    player1_alg = sys.argv[2]
    player2_alg = sys.argv[3]

    winner_list = []
    draws = 0
    avg_num_turns = 0
    discarded_games = 0
    for i in range(simulations):
        player1 = Player(name=player1_alg)
        player2 = Player(name=player2_alg)

        gamestate = GameState(board=Board(), players=[player1, player2])

        # GENERAL GAMEPLAY LOOP
        turn_count = 0
        current_node = Node(parent=None, action={}, gamestate=gamestate, children=[], value=0, num_visits=0) # root node
        current_node = expansion(current_node)
        while (not gamestate.is_over()):
            current_node = play_round(current_node)
            turn_count += 1
            # print(f"round: {turn_count}")


        # Game has finished
        if not gamestate.force_end:
            winner = gamestate.get_winner()
            avg_num_turns += turn_count
            if winner == None:
                # print(f"Game ended in a draw after {count} turns")
                draws += 1
            else:
                winner_list.append(winner.name)
                # print()
                # print(f"Winner after {turn_count} turns: {winner.name}")
                # print(f"{gamestate.players[0].name}: {gamestate.players[0].points} points")
                # print(f"{gamestate.players[1].name}: {gamestate.players[1].points} points")
        else:
            discarded_games += 1
        print(f"-- Simulation {i} --")



# Print statistics
win_counts = Counter(winner_list)
if len(win_counts) == 1:
    if player1_alg in win_counts.keys():
        win_counts[player2_alg] = 0
    else:
        win_counts[player1_alg] = 0

for alg, wins in win_counts.items():
    print(f"{alg} won {wins} time{'s' if wins !=1 else ''}")
print()

avg_num_turns = avg_num_turns / simulations
print(f"Average number of turns per simulation: {avg_num_turns}")
print(f"Number of discarded games: {discarded_games}")