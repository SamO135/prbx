from pydantic import BaseModel
from prbx_project.board import Board
from prbx_project.player import Player
from prbx_project.card import Card
from prbx_project.game_token import Token

class GameState(BaseModel):
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


    def is_over(self) -> bool:
        """Checks if the game has ended.
        
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
    def get_winner(self) -> Player:
        """Gets the winner of the game.
        
        Return:
            Player: The winning player"""
        player1 = self.players[0]
        player2 = self.players[1]
        if player1.points < 15 and player2.points < 15:
            raise ValueError(f"Game has not finished, no players have reached {self.max_points} points")
        
        if player1.points > player2.points:
            winner = self.players[0]
        elif player1.points < player2.points:
            winner = self.players[1]
        else:
            if len(player1.hand) < len(player2.hand):
                winner = player1
            elif len(player1.hand) > len(player2.hand):
                winner = player2
            else:
                winner = None # The game ended in a draw
        return winner
    
    def replace_card(self, board: Board, card: Card, log: bool = False)  -> (Card | None):
        """Replace a card with another of its corresponding tier.
        
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
            if log:
                print(f"No more tier {card.tier} cards in the deck, could not replace.", end=" ")
            return None

    def collect_tokens(self, player: Player, board: Board, tokens: dict[Token, int], returning: dict[Token, int])  -> None:
        """Perform the 'collect tokens' move.
        
        Args:
            player (Player): The player that is collecting tokens
            board (Board): The board object
            tokens (Token): The tokens the player is collecting
            returning (dict[Token, int]): The tokens the player will return as part of this move
        """
        # player collect tokens
        player.collect_tokens(tokens)
        # board remove tokens
        board.remove_tokens(tokens)

        # player remove excess tokens
        player.remove_tokens(returning)
        # board collect excess tokens
        board.recieve_tokens(returning)

    def reserve_card(self, player: Player, board: Board, card: Card, returning: dict[Token, int], log: bool = False) -> None:
        """Perform the 'reserve card' move.
        
        Args:
            player (Player): The player that is reserving a card
            board (Board): The board object
            card (Card): The card the player is reserving
            returning (dict[Token, int]): The tokens the player will return as part of this move
        """
        if len(player.reserved_cards) >= 3:
            raise ValueError("A player cannot have more than 3 cards reserved at once.")
        
        # player collect card to reserved hand
        player.reserve_card(card)

        # board replace card
        new_card =  self.replace_card(board, card, log)
        if new_card is None and log:
            print(f"{player.name} tried to reserve a card.")

        # collect yellow token. collect_token should cover all the steps for this
        if (board.available_tokens[Token.YELLOW] > 0):
            self.collect_tokens(player, board, {Token.YELLOW: 1}, returning)

    def buy_card(self, player: Player, board: Board, card: Card, payment: dict[Token, int], log: bool = False) -> None:
        """Perform the 'buy card' move.
        
        Args:
            player (Player): The player that is buying a card
            board (Board): The board object
            card (Card): The card the player is buying
        """
        # calculate effective price of card given players tokens and bonuses
        # real_price = player.calculate_real_price(card)

        # player remove tokens
        player.remove_tokens(payment)

        # board collect tokens
        board.recieve_tokens(payment)

        # player collect card to hand
        player.collect_card(card)

        # board replace card
        if card in player.reserved_cards:
            player.remove_reserved_card(card)
        else:
            new_card = self.replace_card(board, card, log)
            if new_card is None and log:
                print(f"{player.name} tried to buy a card.")

    def play_move(self, move: dict, log: bool = False):
        match move["move_type"]:
                case "buy_card":
                    card: Card = move["card"]
                    self.buy_card(self.current_player, self.board, card, move["payment"], log)
                case "reserve_card":
                    card: Card = move["card"]
                    self.reserve_card(self.current_player, self.board, card, move["returning"], log)
                case "collect_tokens":
                    tokens: dict[Token, int] = move["tokens"]
                    self.collect_tokens(self.current_player, self.board, tokens, move["returning"])
        # self.next_player()
        return self
    
    def next_player(self):
        if self.current_player == self.players[0]:
            self.current_player = self.players[1]
        else:
            self.current_player = self.players[0]


    def num_tokens_in_play(self, board: Board, player1: Player, player2: Player) -> tuple[dict[Token, int], int]:
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
