"""Define a round."""

from datetime import datetime
from typing import List
from .matches import Match


class Round:
    """Round.

    Has a list of matches, a name, a start and end time"""

    def __init__(self, matches: List[Match], round_name):
        self.matches = matches
        self.round_name = round_name
        self.start_time = datetime.now().strftime("%a %d %b %Y, %H:%M")

    def finish_round(self):
        self.end_time = datetime.now()

    def __str__(self):
        """Used in print."""
        return f"{self.round_name}\n" f"{self.matches}\n"

    def __repr__(self):
        """Used in print."""
        return str(self)
