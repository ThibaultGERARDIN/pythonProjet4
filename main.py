import json
import os
from models.tournament import Tournament
from controllers.base import Controller
from controllers.manage_data import (
    LoadTournament,
    CURRENT_TOURNAMENT_PATH,
)
from controllers.manage_players import AddPlayers
from controllers.manage_tournaments import ReloadTounament
from views.base import Menu

players_data = open("./data/test_players.json")
players_list = json.load(players_data)


tournament_players = AddPlayers(players_list).tournament_players()

# name = input("Tapez le nom du tournoi : ")
# location = input("Tapez le lieu du tournoi : ")
# description = input("Tapez la description du tournoi : ")
name = "test"
location = "test"
description = "test"

# new_player = CreatePlayer()

# new_player.new_player()
# new_player.new_player()


loader = LoadTournament()

if os.path.isdir(f"{CURRENT_TOURNAMENT_PATH}"):
    while True:
        ask_reload = input("Voulez-vous reprendre le tournoi en cours ? (y/n)")
        if ask_reload == "y":
            unfinished_tournament = loader.load_state()
            tournament = ReloadTounament(
                unfinished_tournament["tournament_players"],
                unfinished_tournament["tournament_infos"],
                unfinished_tournament["tournament_rounds"],
            ).recreate_tournament()
            break
        elif ask_reload == "n":
            while True:
                ask_erase = input(
                    "Démarrer un nouveau tournoi ecrasera les données"
                    " du tournoi non terminé, voulez-vous continuer ? (y/n)"
                )
                if ask_erase == "y":
                    tournament = Tournament(
                        name, location, tournament_players, description
                    )
                    break
                elif ask_erase == "n":
                    unfinished_tournament = loader.load_state()
                    tournament = ReloadTounament(
                        unfinished_tournament["tournament_players"],
                        unfinished_tournament["tournament_infos"],
                        unfinished_tournament["tournament_rounds"],
                    ).recreate_tournament()
                    break
                else:
                    print("Merci de répondre par y ou n")
            break
        else:
            print("Merci de répondre par y ou n")
else:
    tournament = Tournament(name, location, tournament_players, description)


controller = Controller(tournament)

controller.start_tournament(tournament)

tournament_result = tournament.result()

view = Menu()
# view.display_menu()i


# tournament_data = json.dumps(tournament.__dict__)
# with open("tournament.json", "w") as json_file:
#     json.dump(tournament_data, json_file)
