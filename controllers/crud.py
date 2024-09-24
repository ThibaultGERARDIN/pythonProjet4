"""Create Read Update Delete operations controller."""

import json

CURRENT_PATH = "./data/tournaments/current_tournament/"
PAST_PATH = "./data/tournaments/past_toournaments/"


class SaveTournament:
    """Save current tournament data in JSON files."""

    def __init__(self, tournament):
        self.name = tournament.name
        self.location = tournament.location
        self.start_date = tournament.start_date
        self.rounds = tournament.rounds
        self.players = tournament.players
        self.description = tournament.description
        self.number_of_rounds = tournament.number_of_rounds
        self.current_round = tournament.current_round
        self.previous_matches = tournament.previous_matches

    def save_state(self):
        tournament_static_infos = {}
        tournament_static_infos["name"] = self.name
        tournament_static_infos["location"] = self.location
        tournament_static_infos["start_date"] = self.start_date
        tournament_static_infos["description"] = self.description
        tournament_static_infos["number_of_rounds"] = self.number_of_rounds

        with open(f"{CURRENT_PATH}static_infos.json", "w") as file:
            json.dump(tournament_static_infos, file)
