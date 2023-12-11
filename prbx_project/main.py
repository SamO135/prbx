import random
from prbx_project.game import Game
from prbx_project.player import Player
from prbx_project.board import Board

if __name__ == "__main__":
    player1 = Player(name="player1")
    player2 = Player(name="player2")

    board = Board()

    game = Game(board=board, players=[player1, player2])

    # while (not game.is_over()):
    #     player_move = game.current_player.select_random_move(game.board.available_tokens, game.board.available_cards)
    #     if player_move[1] == "collect_tokens":
    #         break

    # print(f"Game board: {game.board.available_tokens}")
    # print()
    # game.current_player.collect_tokens(player_move[0])
    # game.board.remove_tokens(player_move[0])
    # print(f"player move: {player_move}")
    # print(f"board after: {game.board.available_tokens}")
    # print(f"player after: {game.current_player.tokens}")


    # GENERAL GAMEPLAY LOOP

    for i in range(10):
        for current_player in game.players:
            # Select move
            player_move = current_player.select_random_move(game.board.available_tokens, game.board.available_cards)

            # Play move
            match player_move[1]:
                case "buy_card":
                    # current_player.buy_card(player_move[0])
                    # game.board.replace_card(player_move[0])
                    pass
                case "reserve_card":
                    # current_player.reserve_card(player_move[0])
                    # game.board.replace_card(player_move[0])
                    pass
                case "collect_tokens":
                    current_player.collect_tokens(player_move[0])
                    game.board.remove_tokens(player_move[0])
                    if len(current_player.tokens) > 10:
                        tokens_to_return = random.choice(current_player.get_possible_tokens_to_return())
                        print(f"returned: {tokens_to_return}")
                        current_player.return_tokens(tokens_to_return)
                        game.board.recieve_tokens(tokens_to_return)
                    print(f"{current_player.name}'s tokens: {current_player.tokens}")
        print()

    # Game has finished
    # winner = game.get_winner()
    # print(winner)

    print(f"{game.players[0].tokens}\n")
    print(f"{game.players[1].tokens}")