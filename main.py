import json
from models.tournament import Tournament
from controllers.base import (
    Controller,
    CreateTounament,
)
from controllers.crud import SaveTournament

players_data = open("./data/test_players.json")
players_list = json.load(players_data)


tournament_players = CreateTounament(players_list).tournament_players()

# name = input("Tapez le nom du tournoi : ")
# location = input("Tapez le lieu du tournoi : ")
# description = input("Tapez la description du tournoi : ")
name = "test"
location = "test"
description = "test"


tournament = Tournament(name, location, tournament_players, description)
controller = Controller(tournament)


controller.start_tournament(tournament)

tournament_result = tournament.result()

saver = SaveTournament(tournament)
saver.save_state()
# saver.end_save()


# print(tournament.rounds[0].matches[0].pairing)
# view = Menu()
# view.display_menu()


# tournament_data = json.dumps(tournament.__dict__)
# with open("tournament.json", "w") as json_file:
#     json.dump(tournament_data, json_file)
