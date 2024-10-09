"""Controllers to manage tournament related operations."""

import json
import re
from models.tournament import Tournament
from models.matches import Match
from models.rounds import Round
from controllers.manage_players import ManagePlayers
from controllers.base import Controller
from controllers.manage_data import SaveData
from views.player_menu import PlayerMenu


class ReloadTounament:
    """Reacreate tournament from current tournament infos."""

    def __init__(
        self,
        players_list,
        tournament_infos,
        tournament_rounds,
    ):
        self.players_list = players_list
        self.infos = tournament_infos
        self.rounds = tournament_rounds
        self.manage_players = ManagePlayers()

    def get_players(self):
        tournament_players = self.manage_players.tournament_players(
            self.players_list
        )
        return tournament_players

    def recreate_match(self, list_of_matches):
        tournament_players = self.get_players()
        match_list = []
        for match in list_of_matches:
            player_1_name = match[0][0]
            player_2_name = match[1][0]
            player_1_score = match[0][1]
            player_2_score = match[1][1]
            for player in tournament_players:
                if player_1_name == player.name:
                    player_1 = player
                elif player_2_name == player.name:
                    player_2 = player
            player_1.score = player_1_score
            player_2.score = player_2_score
            match_in = Match(player_1, player_2)
            match_list.append(match_in)
        return match_list

    def recreate_tournament(self):
        tournament_players = self.get_players()
        name = self.infos["name"]
        description = self.infos["description"]
        start_date = self.infos["start_date"]
        location = self.infos["location"]
        number_of_rounds = self.infos["number_of_rounds"]
        current_round = self.infos["current_round"]
        tournament = Tournament(
            name,
            location,
            tournament_players,
            description,
            number_of_rounds,
            current_round,
        )
        tournament.start_date = start_date
        for round in self.rounds:
            match_list = self.recreate_match(round["matches"])
            round_number = round["round_number"]
            round_start_time = round["start_time"]
            round_result = round["result"]
            round_end_time = round["end_time"]
            round_in = Round(match_list, round_number)
            round_in.start_time = round_start_time
            round_in.result = round_result
            round_in.end_time = round_end_time
            tournament.rounds.append(round_in)
        return tournament


class CreateTournament:
    """Create new tournament."""

    def __init__(self):
        self.player_menu = PlayerMenu()
        self.manage_players = ManagePlayers()
        self.tournament_name = input("Nom du tournoi :")
        self.tournament_location = input("Lieu du tournoi :")
        self.tournament_description = input("Description :")
        self.tournament_players = self.select_players()

    def select_players(self):
        tournament_players = []
        while True:
            source_choice = self.player_menu.player_selection_prompt()
            if source_choice == "1":
                with open("./data/players.json", "r") as file:
                    try:
                        players_list = json.load(file)
                    except ValueError:
                        print("Erreur : liste de joueurs inexistante.")
                        pass
                self.player_menu.display_choice_list(players_list)
                player_choice = self.player_menu.player_choice_add_prompt()
                selected_indexes = re.split(r",|\.| ", player_choice)
                try:
                    selected_indexes.remove('')
                except ValueError:
                    pass
                for index in selected_indexes:
                    if int(index) <= len(players_list):
                        player = players_list[int(index)]
                        if player in tournament_players:
                            print(
                                f"Le joueur {player["name"]}"
                                " est déjà inscrit"
                            )
                        else:
                            tournament_players.append(player)
                            print(
                                f"Le joueur {player["name"]}"
                                " a été ajouté au tournoi."
                            )
                    else:
                        print(f"Choix {index} invalide.")
            elif source_choice == "2":
                new_player = self.manage_players.new_player()
                while not new_player:
                    new_player = self.manage_players.new_player()
                tournament_players.append(new_player.__dict__)
                print(
                    f"Le joueur {new_player.__dict__["name"]}"
                    " a été ajouté au tournoi."
                )
            elif source_choice == "3":
                self.player_menu.display_choice_list(tournament_players)
            elif source_choice == "4":
                self.player_menu.display_choice_list(tournament_players)
                validate = input(
                    "Validez-vous la liste ci-dessus pour"
                    " la création du tournoi ? (y/n)"
                )
                if validate == "y":
                    self.tournament_players = (
                        self.manage_players.tournament_players(
                            tournament_players
                        )
                    )
                    tournament = Tournament(
                        self.tournament_name,
                        self.tournament_location,
                        self.tournament_players,
                        self.tournament_description,
                    )
                    ask_start = input(
                        "Tournoi créé ! Voulez-vous"
                        " le lancer ?(y/n)"
                    )
                    if ask_start == "y":
                        controller = Controller(tournament)
                        controller.start_tournament()
                        break
                    elif ask_start == "n":
                        saver = SaveData(tournament)
                        saver.save_state()
                        break
                elif validate == "n":
                    print("Retour au choix des participants")
                    source_choice = self.player_menu.player_selection_prompt()
            elif source_choice == "0":
                break
            else:
                source_choice = input("Choix invalide, veuillez réessayer.")
