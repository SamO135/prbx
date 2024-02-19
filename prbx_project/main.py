from prbx_project.game import Game
from prbx_project.player import Player
from prbx_project.board import Board
from prbx_project.card import Card
from prbx_project.game_token import Token

if __name__ == "__main__":
    # for i in range(100):
    player1 = Player(name="player1")
    player2 = Player(name="player2")

    game = Game(board=Board(), players=[player1, player2])

    # GENERAL GAMEPLAY LOOP
    count = 0
    while (not game.is_over()):
        for current_player in game.players:
            game.current_player = current_player
            # Select move
            try:
                all_moves = current_player.get_possible_moves(game.board.available_tokens, game.board.available_cards) # For debugging
                player_move = current_player.select_random_move(all_moves)
                game.current_player.locked = False
            except:
                game.current_player.locked = True
                if (all([player.locked for player in game.players])):
                    print("NO LEGAL MOVES FOR EITHER PLAYER, FORCE ENDING GAME")
                    game.force_end = True
                    break
                else:
                    print(f"NO LEGAL MOVES FOR {game.current_player.name}")
                continue

            # Play move
            match player_move["move_type"]:
                case "buy_card":
                    card: Card = player_move["card"]
                    game.buy_card(current_player, game.board, card)
                case "reserve_card":
                    card: Card = player_move["card"]
                    game.reserve_card(current_player, game.board, card, player_move["returning"])
                case "collect_tokens":
                    tokens: dict[Token, int] = player_move["tokens"]
                    game.collect_tokens(current_player, game.board, tokens, player_move["returning"])
        count += 1


    # Game has finished
    if not game.force_end:
        winner = game.get_winner()
        print(f"Winner after {count} turns: {winner.name}")
        # print(f"{game.players[0].name} ({game.players[0].points} points):{game.players[0].tokens}")
        # print(f"{game.players[1].name} ({game.players[1].points} points):{game.players[1].tokens}")
    print()