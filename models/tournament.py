"""Define a tournament."""

from datetime import datetime
from .players import Player
from .rounds import Round
from typing import List


class Tournament:
    """Tournament."""

    def __init__(
        self,
        name,
        location,
        players: List[Player],
        description,
        number_of_rounds=4,
        current_round=0,
    ):
        self.name = name
        self.location = location
        self.start_date = datetime.now().strftime("%a %d %b %Y")
        self.rounds: List[Round] = []
        self.players = players
        self.description = description
        self.number_of_rounds = number_of_rounds
        self.current_round = current_round

    def finish_tournament(self):
        self.end_date = datetime.now().strftime("%a %d %b %Y")
