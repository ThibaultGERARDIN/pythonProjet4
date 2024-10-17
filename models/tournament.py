"""Define a tournament."""

from typing import List
from datetime import datetime
from .players import Player
from .rounds import Round
from helpers.helpers import Helper
from views.tournament_menu import TournamentMenu


class Tournament:
    """
    Define a Tournament object.

    Has a name, location, description.
    List of Player objects.
    Number of rounds (determines the number of players).
    Tracks current round number.
    """

    def __init__(
        self,
        name,
        location,
        players: List[Player],
        description,
        number_of_rounds=4,
        current_round=0,
    ):
        """
        Instanciate a new Tournament from data.

        Start date, and rounds dinamically added.
        """
        self.name = name
        self.location = location
        self.start_date = datetime.now().strftime("%a %d %b %Y")
        self.end_date = None
        self.rounds: List[Round] = []
        self.players = players
        self.description = description
        self.number_of_rounds = number_of_rounds
        self.current_round = current_round
        self.view = TournamentMenu()
        self.helper = Helper()

    def finish_tournament(self):
        """Finish the tournament, record result and end date"""
        self.end_date = datetime.now().strftime("%a %d %b %Y")
        self.result()

    def result(self):
        """Print the result of the tournament"""
        self.ranking = sorted(
            self.players,
            key=lambda player: player.score,
            reverse=True,
        )
        self.winner = self.ranking[0]
        winner_name = self.winner.lastname + " " + self.winner.firstname
        self.view.display_tournament_result(winner_name, self.ranking)
