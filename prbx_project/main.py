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
        print(f"turn {count}")
        for current_player in game.players:
            # DEBUG
            if count == 30:
                pass

            # Select move
            player_move = current_player.select_random_move(game.board.available_tokens, game.board.available_cards)
            # print(f"{current_player.name}: {player_move}")

            # Play move
            match player_move[1]:
                case "buy_card":
                    card: Card = player_move[0]
                    reserved = current_player.buy_card(card)
                    game.board.recieve_tokens(card.price)
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
                    # if sum([amount for amount in current_player.tokens.values()]) > 10:
                    #     tokens_to_return = random.choice(current_player.get_possible_tokens_to_return())
                    #     current_player.return_tokens(tokens_to_return)
                    #     game.board.recieve_tokens(tokens_to_return)
        count += 1


    # Game has finished
    # winner = game.get_winner()
    # print(winner.name)

    print()
    print(f"{game.players[0].name} ({game.players[0].points} points):{game.players[0].tokens}")
    print(f"{game.players[1].name} ({game.players[1].points} points):{game.players[1].tokens}")