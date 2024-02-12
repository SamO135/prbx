from tests.fixtures import test_game_setup as game
from prbx_project.game import Game
from prbx_project.settings import Token
from prbx_project.card import Card


def test_game_init(game: Game):
    board = game.board
    assert len(board.available_cards) == 12
    assert board.available_tokens == {Token.RED: 4, Token.BLUE: 4, Token.GREEN: 4,
                                      Token.WHITE: 4, Token.BLACK: 4, Token.YELLOW: 5}
    assert game.current_player == game.players[0]
    assert game.max_points == 15


def test_is_over(game: Game):
    assert game.is_over() == False

    game.current_player.points = 15
    assert game.is_over() == True

    game.current_player.points = 0
    game.force_end = True
    assert game.is_over() == True


# Still need to implement the logic for the case where 2 people finish on the same turn and have the same number of points
def test_get_winner(game: Game):
    game.players[0].points = 15
    game.players[1].points = 12
    assert game.get_winner() == game.players[0]

    game.players[0].points = 12
    game.players[1].points = 15
    assert game.get_winner() == game.players[1]

    # game.players[0].points = 15
    # game.players[1].points = 15
    # assert game.get_winner() == ???


def test_replace_card(game: Game):
    old_card: Card = game.board.available_cards[0]
    assert old_card in game.board.available_cards

    new_card: Card = game.replace_card(game.board, old_card)
    assert old_card not in game.board.available_cards
    assert new_card in game.board.available_cards
    assert new_card.tier == old_card.tier
    assert new_card != old_card

    game.board.all_cards = [[], [], []]
    old_card: Card = game.board.available_cards[0]
    new_card: Card = game.replace_card(game.board, old_card)
    assert old_card not in game.board.available_cards
    assert new_card == None
    print(game.board.available_cards)
    assert len(game.board.available_cards) == 11


def test_collect_tokens(game: Game):
    assert game.board.available_tokens == {Token.RED: 4, Token.BLUE: 4, Token.GREEN: 4,Token.WHITE: 4, Token.BLACK: 4, Token.YELLOW: 5}
    
    game.collect_tokens(game.players[0], game.board, {Token.RED: 1, Token.BLUE: 1, Token.GREEN: 1, Token.WHITE: 0, Token.BLACK: 0, Token.YELLOW: 0})
    assert game.players[0].tokens == {Token.RED: 1, Token.BLUE: 1, Token.GREEN: 1, Token.WHITE: 0, Token.BLACK: 0, Token.YELLOW: 0}
    assert game.board.available_tokens == {Token.RED: 3, Token.BLUE: 3, Token.GREEN: 3, Token.WHITE: 4, Token.BLACK: 4, Token.YELLOW: 5}

    game.players[0].tokens = {Token.RED: 2, Token.BLUE: 2, Token.GREEN: 2, Token.WHITE: 2, Token.BLACK: 1, Token.YELLOW: 1}
    assert sum(game.board.available_tokens.values()) == 22
    game.collect_tokens(game.players[0], game.board, {Token.RED: 1, Token.BLUE: 1, Token.GREEN: 1, Token.WHITE: 0, Token.BLACK: 0, Token.YELLOW: 0})
    assert sum(game.players[0].tokens.values()) == 10
    assert sum(game.board.available_tokens.values()) == 22


def test_reserve_card(game: Game):
    assert game.players[0].reserved_cards == []
    card = game.board.available_cards[0]

    game.reserve_card(game.players[0], game.board, card)
    assert game.players[0].reserved_cards == [card]
    assert card not in game.board.available_cards
    assert len(game.board.available_cards) == 12
    assert game.players[0].tokens[Token.YELLOW] == 1
    assert game.board.available_tokens[Token.YELLOW] == 4

    game.board.available_tokens[Token.YELLOW] = 0
    game.board.all_cards = [[], [], []]
    card = game.board.available_cards[0]
    game.reserve_card(game.players[0], game.board, card)
    assert card not in game.board.available_cards
    assert len(game.board.available_cards) == 11
    assert game.players[0].tokens[Token.YELLOW] == 1
    assert game.board.available_tokens[Token.YELLOW] == 0


def test_buy_card(game: Game):
    assert game.players[0].hand == []
    
    card = game.board.available_cards[0]
    game.players[0].tokens = card.price # set players owned tokens equal to the price of the card
    game.buy_card(game.players[0], game.board, card)
    assert game.players[0].hand == [card]
    assert card not in game.board.available_cards
    assert sum(game.players[0].tokens.values()) == 0 # after purchasing the card, they should have exactly 0 tokens remaining
    assert game.players[0].bonuses[card.bonus] == 1
    assert game.players[0].points == card.points

    game.players[0].bonuses = {Token.RED: 0, Token.BLUE: 0, Token.GREEN: 0, Token.WHITE: 0, Token.BLACK: 0, Token.YELLOW: 0} #reset the bonuses
    game.reserve_card(game.players[0], game.board, game.board.available_cards[0])
    card = game.players[0].reserved_cards[0]
    game.players[0].tokens = card.price
    assert card not in game.board.available_cards
    game.buy_card(game.players[0], game.board, card)
    assert card not in game.board.available_cards
    assert card not in game.players[0].reserved_cards
    assert sum(game.players[0].tokens.values()) == 0