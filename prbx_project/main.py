import random
from prbx_project.game import Game
from prbx_project.player import Player
from prbx_project.board import Board
from prbx_project.card import Card
from prbx_project.settings import Token

if __name__ == "__main__":
    player1 = Player(name="player1")
    player2 = Player(name="player2")

    board = Board()

    game = Game(board=board, players=[player1, player2])

    # GENERAL GAMEPLAY LOOP
    count = 0
    while (not game.is_over()):
        for current_player in game.players:
            # Select move
            player_move = current_player.select_random_move(game.board.available_tokens, game.board.available_cards)
            # print(f"{current_player.name}: {player_move}")

            # Play move
            match player_move[1]:
                case "buy_card":
                    card: Card = player_move[0]
                    real_price = current_player.calculate_real_price(card)
                    reserved = current_player.buy_card(card)
                    game.board.recieve_tokens(real_price)
                    if not reserved:
                        game.board.replace_card(card)
                case "reserve_card":
                    card: Card = player_move[0]
                    current_player.reserve_card(card, board.available_tokens)
                    game.board.replace_card(card, reserved=True)
                case "collect_tokens":
                    tokens: dict[Token, int] = player_move[0]
                    current_player.collect_tokens(tokens)
                    game.board.remove_tokens(tokens)
        count += 1


    # Game has finished
    winner = game.get_winner()
    print(f"Winner after {count} turns: {winner.name}")

    print()
    print(f"{game.players[0].name} ({game.players[0].points} points):{game.players[0].tokens}")
    print(f"{game.players[1].name} ({game.players[1].points} points):{game.players[1].tokens}")