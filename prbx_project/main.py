from prbx_project.gamestate import GameState
from prbx_project.player import Player
from prbx_project.board import Board
from prbx_project.node import Node
# from prbx_project.monte_carlo import select_move_with_mcts

if __name__ == "__main__":
    # for i in range(100):
    player1 = Player(name="player1")
    player2 = Player(name="player2")

    gamestate = GameState(board=Board(), players=[player1, player2])

    # GENERAL GAMEPLAY LOOP
    count = 0
    current_node = Node(parent=None, action=None, gamestate=gamestate, children=[], value=0, num_visits=1) # root node
    while (not gamestate.is_over()):
        for current_player in gamestate.players:
            gamestate.current_player = current_player
            # Select move
            try:
                all_moves = current_player.get_possible_moves(gamestate.board.available_tokens, gamestate.board.available_cards)
                player_move = current_player.select_random_move(all_moves)
                # player_move = select_move_with_mcts(current_node)
                gamestate.current_player.locked = False
            except Exception as e:
                print(e)
                gamestate.current_player.locked = True
                if (all([player.locked for player in gamestate.players])):
                    print("NO LEGAL MOVES FOR EITHER PLAYER, FORCE ENDING GAME")
                    gamestate.force_end = True
                    break
                else:
                    print(f"NO LEGAL MOVES FOR {gamestate.current_player.name}")
                continue

            # Play move
            gamestate.play_move(player_move)
        count += 1
        current_node = Node(parent=current_node, action=player_move, gamestate=gamestate, children=[], value=0, num_visits=0)



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