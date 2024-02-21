import pytest
from tests.fixtures import test_game_setup as game, test_card_set
from prbx_project.gamestate import GameState
from prbx_project.game_token import Token
from prbx_project.card import Card


def test_game_init(game: GameState):
    board = game.board
    assert len(board.available_cards) == 12
    assert board.available_tokens == {Token.RED: 4, Token.BLUE: 4, Token.GREEN: 4,
                                      Token.WHITE: 4, Token.BLACK: 4, Token.YELLOW: 5}
    assert game.current_player == game.players[0]
    assert game.max_points == 15


def test_is_over(game: GameState):
    assert game.is_over() == False

    game.current_player.points = 15
    assert game.is_over() == True

    game.current_player.points = 0
    game.force_end = True
    assert game.is_over() == True


# Still need to implement the logic for the case where 2 people finish on the same turn and have the same number of points
def test_get_winner(game: GameState, test_card_set: list[Card]):
    # test player 1 more points
    game.players[0].points = 15
    game.players[1].points = 12
    assert game.get_winner() == game.players[0]

    # test player 2 more points
    game.players[0].points = 12
    game.players[1].points = 15
    assert game.get_winner() == game.players[1]

    # test no player reached winning points
    with pytest.raises(ValueError):
        game.players[0].points = 12
        game.players[1].points = 12
        assert game.get_winner() == game.players[1]

    # test both players finished with same points but different number of dev cards
    game.players[0].points = 15
    game.players[1].points = 15
    game.players[0].hand = [test_card_set[0], test_card_set[1]]
    game.players[1].hand = [test_card_set[2]]
    assert game.get_winner() == game.players[1]

    # test both players finished with same points and same num of dev cards
    game.players[0].points = 15
    game.players[1].points = 15
    game.players[0].hand = [test_card_set[0], test_card_set[1]]
    game.players[1].hand = [test_card_set[2],test_card_set[3]]
    assert game.get_winner() == None


def test_replace_card(game: GameState):
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
    assert len(game.board.available_cards) == 11


def test_collect_tokens(game: GameState):
    assert game.board.available_tokens == {Token.RED: 4, Token.BLUE: 4, Token.GREEN: 4,Token.WHITE: 4, Token.BLACK: 4, Token.YELLOW: 5}
    
    game.collect_tokens(game.players[0], game.board, {Token.RED: 1, Token.BLUE: 1, Token.GREEN: 1, Token.WHITE: 0, Token.BLACK: 0, Token.YELLOW: 0}, returning={})
    assert game.players[0].tokens == {Token.RED: 1, Token.BLUE: 1, Token.GREEN: 1, Token.WHITE: 0, Token.BLACK: 0, Token.YELLOW: 0}
    assert game.board.available_tokens == {Token.RED: 3, Token.BLUE: 3, Token.GREEN: 3, Token.WHITE: 4, Token.BLACK: 4, Token.YELLOW: 5}

    game.players[0].tokens = {Token.RED: 2, Token.BLUE: 2, Token.GREEN: 2, Token.WHITE: 2, Token.BLACK: 1, Token.YELLOW: 1}
    assert sum(game.board.available_tokens.values()) == 22
    game.collect_tokens(game.players[0], game.board, {Token.RED: 1, Token.BLUE: 1, Token.GREEN: 1, Token.WHITE: 0, Token.BLACK: 0, Token.YELLOW: 0}, returning={Token.RED: 2, Token.BLACK: 1})
    assert sum(game.players[0].tokens.values()) == 10
    assert sum(game.board.available_tokens.values()) == 22


def test_reserve_card(game: GameState):
    assert game.players[0].reserved_cards == []
    card = game.board.available_cards[0]

    # normal reserve card move, with returning a token
    game.players[0].tokens = {Token.RED: 2, Token.BLUE: 2, Token.GREEN: 2, Token.WHITE: 2, Token.BLACK: 2, Token.YELLOW: 0}
    game.reserve_card(game.players[0], game.board, card, returning={Token.RED: 1 })
    assert game.players[0].reserved_cards == [card]
    assert card not in game.board.available_cards
    assert len(game.board.available_cards) == 12
    assert game.players[0].tokens == {Token.RED: 1, Token.BLUE: 2, Token.GREEN: 2, Token.WHITE: 2, Token.BLACK: 2, Token.YELLOW: 1}
    assert game.board.available_tokens[Token.YELLOW] == 4

    # test reserve card when player already has 3 reserved cards
    with pytest.raises(ValueError):
        game.players[0].reserved_cards = [game.board.available_cards[0], game.board.available_cards[1], game.board.available_cards[2]]
        card = game.board.available_cards[3]
        game.reserve_card(game.players[0], game.board, card, returning={})


    # reserve card when no more cards in deck to replace with
    game.players[0].reserved_cards = [game.board.available_cards[0]]
    game.board.available_tokens[Token.YELLOW] = 0
    game.board.all_cards = [[], [], []]
    card = game.board.available_cards[0]
    game.reserve_card(game.players[0], game.board, card, returning={})
    assert card not in game.board.available_cards
    assert len(game.board.available_cards) == 11
    assert game.players[0].tokens[Token.YELLOW] == 1
    assert game.board.available_tokens[Token.YELLOW] == 0


def test_buy_card(game: GameState):
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
    game.reserve_card(game.players[0], game.board, game.board.available_cards[0], returning={})
    card = game.players[0].reserved_cards[0]
    game.players[0].tokens = card.price
    assert card not in game.board.available_cards
    game.buy_card(game.players[0], game.board, card)
    assert card not in game.board.available_cards
    assert card not in game.players[0].reserved_cards
    assert sum(game.players[0].tokens.values()) == 0