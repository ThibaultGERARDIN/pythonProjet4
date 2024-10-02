"""Define a round."""

from datetime import datetime
from typing import List
from .matches import Match


class Round:
    """Round.

    Has a list of matches, a name, a start and end time"""

    def __init__(self, matches: List[Match], round_number):
        self.matches = matches
        self.round_number = round_number
        self.round_name = f"Round {self.round_number}"
        self.start_time = datetime.now().strftime("%a %d %b %Y, %H:%M")
        self.result = []
        self.end_time = "Round en cours"

    def finish_round(self):
        self.end_time = datetime.now().strftime("%a %d %b %Y, %H:%M")

    def record_result(self, match_index, winner):
        self.result.append(f"Match {match_index} : {winner}")

    def __str__(self):
        """Used in print."""
        return f"{self.round_name}\n{self.matches}\n{self.result}\n"

    def __repr__(self):
        """Used in print."""
        return str(self)
