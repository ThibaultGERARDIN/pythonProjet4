"""Define a match."""

from .players import Player


class Match:
    """Define the Match object."""

    def __init__(self, player_1: Player, player_2: Player):
        """Instanciate a new Match from two Player objects."""
        self.players = [player_1, player_2]
        self.pairing = (
            [player_1.name, player_1.score],
            [player_2.name, player_2.score],
        )
        self.save_pairing = (
            [player_1.name, player_1.national_chess_id, player_1.score],
            [player_2.name, player_2.national_chess_id, player_2.score],
        )

    def __str__(self):
        """Used in print."""
        return f"{self.pairing[0]} vs {self.pairing[1]}"

    def __repr__(self):
        """Used in print."""
        return str(self)
