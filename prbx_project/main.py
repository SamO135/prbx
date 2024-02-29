from prbx_project.gamestate import GameState
from prbx_project.player import Player
from prbx_project.board import Board
from prbx_project.node import Node
from prbx_project.monte_carlo import select_move_with_mcts, expansion
import copy

def play_round(current_node: Node):
    for current_player in current_node.gamestate.players:
        # current_node.gamestate.current_player = current_player
        # Select move
        try:
            # player_move = current_player.select_random_move(all_moves)
            if current_player.name == "mcts_agent":
                player_move = select_move_with_mcts(current_node)
                # all_moves = current_player.get_possible_moves(current_node.gamestate.board.available_tokens, current_node.gamestate.board.available_cards)
                # player_move = current_player.select_random_move(all_moves)
            elif current_player.name == "random_agent":
                all_moves = current_player.get_possible_moves(current_node.gamestate.board.available_tokens, current_node.gamestate.board.available_cards)
                player_move = current_player.select_random_move(all_moves)
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
        if current_node.gamestate.current_player.name == "mcts_agent":
            current_node = expansion(current_node)
    return current_node


if __name__ == "__main__":
    # for i in range(100):
    player1 = Player(name="mcts_agent")
    player2 = Player(name="random_agent")

    gamestate = GameState(board=Board(), players=[player1, player2])

    # GENERAL GAMEPLAY LOOP
    count = 0
    current_node = Node(parent=None, action={}, gamestate=gamestate, children=[], value=0, num_visits=0) # root node
    current_node = expansion(current_node)
    while (not gamestate.is_over()):
        current_node = play_round(current_node)
        count += 1
        print(f"round: {count}")


    # Game has finished
    if not gamestate.force_end:
        winner = gamestate.get_winner()
        if winner == None:
            print(f"Game ended in a draw after {count} turns")
        else:
            print()
            print(f"Winner after {count} turns: {winner.name}")
            print(f"{gamestate.players[0].name}: {gamestate.players[0].points} points")
            print(f"{gamestate.players[1].name}: {gamestate.players[1].points} points")
    print()