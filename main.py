import json

# from models.players import Player
# from models.matches import Match
from models.rounds import Round
from models.tournament import Tournament
from controllers.base import MatchResult, Controller, TournamentResults


players_data = open("./data/players.json")
players_list = json.load(players_data)

controller = Controller(players_list)
tournament_players = controller.add_players()

# name = input("Tapez le nom du tournoi : ")
# location = input("Tapez le lieu du tournoi : ")
# description = input("Tapez la description du tournoi : ")
name = "test"
location = "test"
description = "test"


tournament = Tournament(name, location, tournament_players, description)


for i in range(tournament.number_of_rounds):

    tournament.current_round = i + 1
    match_list = controller.draw_matches(tournament_players)

    round = Round(match_list, f"Round {i+1}")

    for match in round.matches:
        match_result = MatchResult(match, tournament_players)
        winner = match_result.select_winner()
        match_result.add_score()

    tournament.rounds.append(round)

tournament_result = TournamentResults(tournament)

# print(controller.previous_matches)
print(tournament.rounds)
print(tournament_result)
