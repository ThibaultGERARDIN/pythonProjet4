"""Define a round."""

from datetime import datetime
from typing import List
from .matches import Match


class Round:
    """
    Define Round object.

    Has a list of matches, a name, a start and end time
    """

    def __init__(self, matches: List[Match], round_number):
        """
        Instanciate new Round from list of matches and number.

        Generate start time automatically.
        End time tracking if round ended or not.
        """
        self.matches = matches
        self.round_number = round_number
        self.round_name = f"Round {self.round_number}"
        self.start_time = datetime.now().strftime("%a %d %b %Y, %H:%M")
        self.result = []
        self.end_time = "Round en cours"

    def finish_round(self):
        """Set end_time of round."""
        self.end_time = datetime.now().strftime("%a %d %b %Y, %H:%M")

    def record_result(self, match_index, winner):
        """Set result of match in round.result"""
        if winner == "draw":
            self.result.append(f"Match {match_index} : match nul")
        else:
            self.result.append(f"Match {match_index} : {winner.name}")

    def __str__(self):
        """Define the print version of a round"""
        return f"{self.round_name}\n{self.matches}\n{self.result}\n"

    def __repr__(self):
        """Used in print."""
        return str(self)
