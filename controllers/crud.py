"""Create Read Update Delete operations controller."""

import json
import os

CURRENT_TOURNAMENT_PATH = "./data/tournaments/current_tournament/"
PAST_TOURNAMENT_PATH = "./data/tournaments/past_tournaments/"


class SaveTournament:
    """Save current tournament data in JSON files."""

    def __init__(self, tournament):
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
        self.previous_matches = tournament.previous_matches

    def save_state(self):
        """Save current state of tournament into JSON files"""
        if not os.path.isdir(f"{CURRENT_TOURNAMENT_PATH}"):
            os.makedirs(f"{CURRENT_TOURNAMENT_PATH}")
        tournament_infos = self.static_infos
        tournament_infos["current_round"] = self.current_round
        tournament_players = []
        tournament_rounds = []
        tournament_previous_matches = []
        with open(f"{CURRENT_TOURNAMENT_PATH}static_infos.json", "w") as file:
            json.dump(tournament_infos, file, indent=4)

        for player in self.players:
            tournament_players.append(player.__dict__)
        with open(
            f"{CURRENT_TOURNAMENT_PATH}tournament_players.json", "w"
        ) as file:
            json.dump(tournament_players, file, indent=4)
        for round in self.rounds:
            round_dict = {}
            round_dict["round_number"] = round.round_number
            round_dict["round_name"] = round.round_name
            round_dict["start_time"] = round.start_time
            round_dict["matches"] = []
            for match in round.matches:
                round_dict["matches"].append(match.pairing)
            round_dict["result"] = round.result
            round_dict["end_time"] = round.end_time
            tournament_rounds.append(round_dict)
        with open(
            f"{CURRENT_TOURNAMENT_PATH}tournament_rounds.json", "w"
        ) as file:
            json.dump(tournament_rounds, file, indent=4)
        for match in self.previous_matches:
            tournament_previous_matches.append(match.pairing)
        with open(
            f"{CURRENT_TOURNAMENT_PATH}tournament_previous_matches.json", "w"
        ) as file:
            json.dump(tournament_previous_matches, file, indent=4)

    def end_save(self):
        """
        Save tournament at the end.

        Combine all current tournament files into one
        Delete current tournament files and folder
        """
        if not os.path.isdir(f"{PAST_TOURNAMENT_PATH}"):
            os.makedirs(f"{PAST_TOURNAMENT_PATH}")
        self.save_state()
        state_files = [
            f"{CURRENT_TOURNAMENT_PATH}static_infos.json",
            f"{CURRENT_TOURNAMENT_PATH}tournament_players.json",
            f"{CURRENT_TOURNAMENT_PATH}tournament_rounds.json",
        ]
        files_to_save = []
        for file in state_files:
            with open(file, "r") as f:
                files_to_save.append(json.load(f))
        end_file = {}
        end_file['static_infos'] = files_to_save[0]
        end_file['tournament_players'] = files_to_save[1]
        end_file['tournament_rounds'] = files_to_save[2]
        with open(
            f"{PAST_TOURNAMENT_PATH}{self.static_infos["name"]}.json", "w"
        ) as file:
            json.dump(end_file, file, indent=4)
        for json_file in os.listdir(f"{CURRENT_TOURNAMENT_PATH}"):
            os.remove(f"{CURRENT_TOURNAMENT_PATH}{json_file}")
        os.rmdir(f"{CURRENT_TOURNAMENT_PATH}")


class LoadTournament:

    def load_state(self):
        """Load current state from the files, return a dict with all infos"""
        if os.path.isdir(f"{CURRENT_TOURNAMENT_PATH}"):
            unfinished_tournament = {}
            with open(
                f"{CURRENT_TOURNAMENT_PATH}static_infos.json", "r"
            ) as file:
                tournament_infos = json.load(file)
            with open(
                f"{CURRENT_TOURNAMENT_PATH}tournament_players.json", "r"
            ) as file:
                tournament_players = json.load(file)
            with open(
                f"{CURRENT_TOURNAMENT_PATH}tournament_rounds.json", "r"
            ) as file:
                tournament_rounds = json.load(file)
            with open(
                f"{CURRENT_TOURNAMENT_PATH}"
                "tournament_previous_matches.json", "r"
            ) as file:
                tournament_previous_matches = json.load(file)
            unfinished_tournament["tournament_infos"] = tournament_infos
            unfinished_tournament["tournament_players"] = tournament_players
            unfinished_tournament["tournament_rounds"] = tournament_rounds
            unfinished_tournament[
                "tournament_previous_matches"
            ] = tournament_previous_matches
            return unfinished_tournament
        else:
            print("No unfinished tournament found.")
