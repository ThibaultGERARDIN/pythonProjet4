"""Controllers to manage player related operations."""

import os
import json
from models.players import Player
from views.player_menu import PlayerMenu
from helpers.helpers import Helper

PLAYER_DATA_PATH = "./data/players.json"


class ManagePlayers:
    """Utilities to manage players"""

    def __init__(self):
        if not os.path.isfile(PLAYER_DATA_PATH):
            with open(PLAYER_DATA_PATH, "w") as file:
                json.dump([], file, indent=4)
        self.view = PlayerMenu()
        self.helper = Helper()

    def tournament_players(self, players_list):
        """Add players to list"""
        tournament_players = []
        for player in players_list:
            player_in = Player(
                player["lastname"],
                player["firstname"],
                player["date_of_birth"],
                player["national_chess_id"],
            )
            player_in.score = player["score"]
            tournament_players.append(player_in)
        return tournament_players

    def new_player(self):
        player_list = []
        new_player_data = self.view.create_player_prompt()
        lastname = new_player_data["lastname"]
        firstname = new_player_data["firstname"]
        date_of_birth = new_player_data["date_of_birth"]
        national_chess_id = new_player_data["national_chess_id"]
        player = Player(lastname, firstname, date_of_birth, national_chess_id)
        with open(PLAYER_DATA_PATH, "r") as file:
            try:
                player_list = json.load(file)
            except ValueError:
                pass
            if not any(
                d["national_chess_id"] == f"{player.national_chess_id}"
                for d in player_list
            ):
                player_list.append(player.__dict__)
                self.helper.save_file(PLAYER_DATA_PATH, player_list)
                print(
                    f"Le joueur {player.name} a bien"
                    " été ajouté à la base de données."
                )
                return player
            else:
                print(
                    f"Un joueur avec l'INE {player.national_chess_id}"
                    " est déjà dans la liste, veuillez réessayer."
                )
                return None

    def search_player(self):
        players_found = []
        players_list = self.helper.load_file(PLAYER_DATA_PATH)
        while True:
            search_by = self.view.search_player_prompt()
            if search_by == "1":
                player_name = self.view.search_name_prompt()
                for player in players_list:
                    if player_name.upper() == player["lastname"].upper():
                        players_found.append(player)
                if len(players_found) == 0:
                    print(f"Pas de joueur {player_name} dans la liste.")
                self.view.display_complete_list(players_found)
                break
            elif search_by == "2":
                player_ine = self.view.search_ine_prompt()
                for player in players_list:
                    if player_ine.upper() == player["national_chess_id"]:
                        players_found.append(player)
                if len(players_found) == 0:
                    print(f"Pas de joueur {player_ine} dans la liste.")
                self.view.display_complete_list(players_found)
                break
            elif search_by == "0":
                self.view.display_main_menu()
            else:
                search_by = input("Choix invalide, veuillez réessayer.")
        if len(players_found) > 0:
            return players_found
        else:
            print("Aucun joueur trouvé, veuillez le rajouter.")
            return None

    def update_player(self, player_to_update: dict):
        players_list = self.helper.load_file(PLAYER_DATA_PATH)
        index = players_list.index(player_to_update)
        updated_player_data = self.view.update_player_prompt(player_to_update)
        updated_player = Player(
            updated_player_data["lastname"],
            updated_player_data["firstname"],
            updated_player_data["date_of_birth"],
            updated_player_data["national_chess_id"],
        )
        confirm_update = self.view.confirm_player_update(
            player_to_update, updated_player_data
        )
        print(confirm_update)
        if confirm_update == "y":
            players_list[index] = updated_player.__dict__
            self.helper.save_file(PLAYER_DATA_PATH, players_list)
            print("Modification enregistrée.")
        else:
            print("Modification annulée.")

    def select_player_to_update(self):
        players_found = self.search_player()
        if players_found and len(players_found) > 1:
            self.view.display_choice_list(players_found)
            player_choice = int(self.view.player_choice_update_prompt())
            player_to_update = players_found[player_choice]
        else:
            player_to_update = players_found[0]
        return player_to_update
