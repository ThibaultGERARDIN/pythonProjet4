"""Controllers to manage player related operations."""

import os
import json
import re
from models.players import Player, DD_MM_YYYY, YYYY_MM_DD

INE_CHECK = re.compile(r"^([A-Z]{2})([0-9]{5}$)")


class AddPlayers:

    def __init__(self, players_list):
        self.players_list = players_list

    def tournament_players(self):
        """Add players to list"""
        tournament_players = []
        players_list = self.players_list
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


class CreatePlayer:
    """Create a player from inputs"""

    def __init__(self):
        """Create the players.json file if not existing"""
        self.player_path = "./data/players.json"
        if not os.path.isfile(self.player_path):
            with open(self.player_path, "w") as file:
                json.dump([], file, indent=4)

    def new_player(self):
        player_list = []
        print(
            "Compléter les données demandées ci-dessous"
            " pour ajouter un joueur à la base de données :"
        )
        lastname = input("Nom :")
        firstname = input("Prénom :")
        date_of_birth = input("Date de naissance :")
        while not DD_MM_YYYY.match(date_of_birth) and not YYYY_MM_DD.match(
            date_of_birth
        ):
            date_of_birth = input(
                "Date non reconnue, merci de donner une date"
                " au format DD(-/)MM(-/)YYYY ou YYYY(-/)MM(-/)DD :"
            )
        national_chess_id = input("Identifiant National d'Echec :")
        while not INE_CHECK.match(national_chess_id):
            national_chess_id = input(
                "INE incorrect, doit correspondre à"
                " 2 lettres suivies de 5 chiffres (ex:AB12345) :"
            )
        player = Player(lastname, firstname, date_of_birth, national_chess_id)
        with open(self.player_path, "r") as file:
            try:
                player_list = json.load(file)
            except ValueError:
                pass
            player_list.append(player.__dict__)
            with open(self.player_path, "w") as file:
                json.dump(player_list, file, indent=4)
        print(
            f"Le joueur {player.name} a bien été ajouté à la base de données."
        )
