"""Define a match."""

from .players import Player


class Match:
    """Match."""

    def __init__(self, player_1: Player, player_2: Player):
        self.players = (
            [player_1.name, player_1.score],
            [player_2.name, player_2.score],
        )

    def __str__(self):
        """Used in print."""
        return f"Match {self.players[0]} vs {self.players[1]}"

    def __repr__(self):
        """Used in print."""
        return str(self)
