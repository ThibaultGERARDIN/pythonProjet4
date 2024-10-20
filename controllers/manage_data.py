"""Controllers to manage data related operations."""

import os
import time
import re
from helpers.helpers import Helper

CURRENT_TOURNAMENT_PATH = "./data/tournaments/current_tournament/"
PAST_TOURNAMENT_PATH = "./data/tournaments/past_tournaments/"


class SaveData:
    """Save data in JSON files."""

    def __init__(self, tournament):
        """Initialize with tournament data."""
        self.static_infos = {}
        self.static_infos["name"] = tournament.name
        self.static_infos["location"] = tournament.location
        self.static_infos["start_date"] = tournament.start_date
        self.static_infos["description"] = tournament.description
        self.static_infos["number_of_rounds"] = tournament.number_of_rounds
        self.rounds = tournament.rounds
        self.players = sorted(
            tournament.players,
            key=lambda player: player.score,
            reverse=True,
        )
        self.current_round = tournament.current_round
        self.tournament = tournament

    def save_state(self):
        """
        Save current state of tournament into JSON files

        Create 3 files to save all current data :
        static_infos.json
        tournament_players.json
        tournament_rounds.json
        """
        helper = Helper()
        if not os.path.isdir(CURRENT_TOURNAMENT_PATH):
            os.makedirs(CURRENT_TOURNAMENT_PATH)
        tournament_infos = self.static_infos
        tournament_infos["current_round"] = self.current_round
        tournament_players = []
        tournament_rounds = []
        helper.save_file(
            f"{CURRENT_TOURNAMENT_PATH}static_infos.json", tournament_infos
        )

        for player in self.players:
            tournament_players.append(player.__dict__)
        helper.save_file(
            f"{CURRENT_TOURNAMENT_PATH}tournament_players.json",
            tournament_players,
        )
        for round in self.rounds:
            round_dict = {}
            round_dict["round_number"] = round.round_number
            round_dict["round_name"] = round.round_name
            round_dict["start_time"] = round.start_time
            round_dict["matches"] = []
            for match in round.matches:
                round_dict["matches"].append(match.save_pairing)
            round_dict["result"] = round.result
            round_dict["end_time"] = round.end_time
            tournament_rounds.append(round_dict)
        helper.save_file(
            f"{CURRENT_TOURNAMENT_PATH}tournament_rounds.json",
            tournament_rounds,
        )

    def end_save(self, finished_tournament=None):
        """
        Close current tournament and save data

        Combine all current tournament files into one
        Delete current tournament files and folder
        If given a finished tournament, replace tournament_players
        with tournament_ranking.
        """
        helper = Helper()
        if not os.path.isdir(PAST_TOURNAMENT_PATH):
            os.makedirs(PAST_TOURNAMENT_PATH)
        self.save_state()
        if finished_tournament:
            end_rankings = finished_tournament.ranking
            tournament_winner = finished_tournament.winner
            tournament_result = [
                f"Gagnant : {tournament_winner.lastname}"
                f" {tournament_winner.firstname}"
            ]
            for player in end_rankings:
                tournament_result.append(player.__dict__)
            helper.save_file(
                f"{CURRENT_TOURNAMENT_PATH}tournament_result.json",
                tournament_result,
            )
            state_files = [
                f"{CURRENT_TOURNAMENT_PATH}static_infos.json",
                f"{CURRENT_TOURNAMENT_PATH}tournament_result.json",
                f"{CURRENT_TOURNAMENT_PATH}tournament_rounds.json",
            ]
        else:
            state_files = [
                f"{CURRENT_TOURNAMENT_PATH}static_infos.json",
                f"{CURRENT_TOURNAMENT_PATH}tournament_players.json",
                f"{CURRENT_TOURNAMENT_PATH}tournament_rounds.json",
            ]
        files_to_save = []
        for file in state_files:
            files_to_save.append(helper.load_file(file))
        end_file = {}
        end_file["static_infos"] = files_to_save[0]
        if finished_tournament:
            end_file["static_infos"]["end_date"] = finished_tournament.end_date
            end_file["tournament_result"] = files_to_save[1]
        else:
            end_file["tournament_players"] = files_to_save[1]
        end_file["tournament_rounds"] = files_to_save[2]
        if (
            end_file["static_infos"]["current_round"]
            < end_file["static_infos"]["number_of_rounds"]
        ):
            tournament_name = re.sub(" ", "-", self.static_infos["name"])
            end_save_name = (
                tournament_name.lower()
                + "-ANNULE"
                + "__"
                + time.strftime("%d%m%Y-%H%M%S")
            )
        else:
            tournament_name = re.sub(" ", "-", self.static_infos["name"])
            end_save_name = (
                tournament_name.lower() + "__" + time.strftime("%d%m%Y-%H%M%S")
            )
        helper.save_file(
            f"{PAST_TOURNAMENT_PATH}{end_save_name}.json", end_file
        )
        for json_file in os.listdir(CURRENT_TOURNAMENT_PATH):
            os.remove(f"{CURRENT_TOURNAMENT_PATH}{json_file}")
        os.rmdir(CURRENT_TOURNAMENT_PATH)


class LoadData:
    """Load data from the saved JSON files."""

    def load_state(self):
        """Load current state from the files, return a dict with all infos"""
        helper = Helper()
        if os.path.isdir(CURRENT_TOURNAMENT_PATH):
            unfinished_tournament = {}
            unfinished_tournament["tournament_infos"] = helper.load_file(
                f"{CURRENT_TOURNAMENT_PATH}static_infos.json"
            )
            unfinished_tournament["tournament_players"] = helper.load_file(
                f"{CURRENT_TOURNAMENT_PATH}tournament_players.json"
            )
            unfinished_tournament["tournament_rounds"] = helper.load_file(
                f"{CURRENT_TOURNAMENT_PATH}tournament_rounds.json"
            )
            return unfinished_tournament
        else:
            print("No unfinished tournament found.")
