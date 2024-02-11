from pydantic import BaseModel
from prbx_project.board import Board
from prbx_project.player import Player
from prbx_project.card import Card
from prbx_project.settings import Token

class Game(BaseModel):
    """A class representing the entire gamestate."""

    board: Board
    players: list[Player]
    current_player: Player = None
    max_points: int = 15
    force_end: bool = False

    def __init__(self, *args, **kwargs):
        """Constructor method."""
        super().__init__(*args, **kwargs)
        self.current_player = self.players[0]


    def is_over(self):
        """Checks if a player has reached the winning score.
        
        Return:
            bool: True if game has finished, False otherwise.
        """
        if self.force_end:
            return True
        for player in self.players:
            if player.points >= self.max_points:
                return True
        return False
    
    # Still need to implement the logic for the case where 2 people finish on the same turn and have the same number of points
    def get_winner(self):
        """Gets the winner of the game.
        
        Return:
            Player: The winning player"""
        winner = self.players[0]
        for player in self.players:
            if player.points > winner.points:
                winner = player
        return winner
    
    def replace_card(self, board: Board, card: Card):
        """Replace a card with its corresponding tier.
        
        Args:
            board (Board): The board object
            card (Card): The card to be replaced

        Return:
            Card: The new card
        """
        # board remove card
        board.remove_card(card)
        # board add new card
        try:
            return board.add_new_card(card.tier-1)
        except:
            print(f"No more tier {card.tier} cards in the deck, could not replace.")
            return None

    def collect_tokens(self, player: Player, board: Board, tokens: dict[Token, int]):
        """Perform the 'collect tokens' move.
        
        Args:
            player (Player): The player that is collecting tokens
            board (Board): The board object
            tokens (Token): The tokens the player is collecting
        """
        # player collect tokens
        player.collect_tokens(tokens)
        # board remove tokens
        board.remove_tokens(tokens)
        # check player excess tokens
        if sum(player.tokens.values()) > 10:
            # decide which tokens to return
            tokens_to_return = player.choose_tokens_to_return()
            # player remove tokens
            player.remove_tokens(tokens_to_return)
            # board collect tokens
            board.recieve_tokens(tokens_to_return)

    def reserve_card(self, player: Player, board: Board, card: Card):
        """Perform the 'reserve card' move.
        
        Args:
            player (Player): The player that is reserving a card
            board (Board): The board object
            card (Card): The card the player is reserving
        """
        # player collect card to reserved hand
        player.reserve_card(card)

        # board replace card
        self.replace_card(board, card)

        # collect yellow token. collect_token should cover all the steps for this
        if (board.available_tokens[Token.YELLOW] > 0):
            self.collect_tokens(player, board, {Token.YELLOW: 1})

    def buy_card(self, player: Player, board: Board, card: Card):
        """Perform the 'buy card' move.
        
        Args:
            player (Player): The player that is buying a card
            board (Board): The board object
            card (Card): The card the player is buying
        """
        # calculate effective price of card given players tokens and bonuses
        real_price = player.calculate_real_price(card)

        # player remove tokens
        player.remove_tokens(real_price)

        # board collect tokens
        board.recieve_tokens(real_price)

        # player collect card to hand
        player.collect_card(card)

        # board replace card
        if card in player.reserved_cards:
            player.remove_reserved_card(card)
        else:
            self.replace_card(board, card)


    def num_tokens_in_play(self, board: Board, player1: Player, player2: Player):
        """Debugging method to calculate the number of tokens in the game to make sure it is consistent."""
        num_tokens = 0
        num_tokens += sum(board.available_tokens.values())
        num_tokens += sum(player1.tokens.values())
        num_tokens += sum(player2.tokens.values())

        tokens = board.available_tokens
        for token, _ in tokens.items():
            tokens[token] += player1.tokens[token]
            tokens[token] += player2.tokens[token]
        return tokens, num_tokens
