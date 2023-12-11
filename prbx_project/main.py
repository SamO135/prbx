from prbx_project.game import Game
from prbx_project.player import Player
from prbx_project.board import Board

if __name__ == "__main__":
    player1 = Player()
    player2 = Player()

    board = Board()

    game = Game(board=board, players=[player1, player2])

    while (not game.isOver()):
        player_move = game.current_player.select_move(game.board.available_tokens, game.board.available_cards)
        if player_move[1] == "collect_tokens":
            break

    print(f"Game board: {game.board.available_tokens}")
    print()
    game.collect_tokens(player_move[0])
    print(f"player move: {player_move}")
    print(f"board after: {game.board.available_tokens}")
    print(f"player after: {game.current_player.tokens}")

