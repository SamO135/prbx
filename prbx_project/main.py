from board import Board
from player import Player


player1 = Player()
player2 = Player()

game = Board(players = [player1, player2])

current_player = game.players[0]

print(player1.select_move(game.available_tokens, game.available_cards))


