import json
from models.players import Player
from models.matches import Match
from models.rounds import Round


players_data = open("./data/players.json")
players_list = json.load(players_data)

tournament_players = []

for player in players_list:
    player_in = Player(
        player["lastname"],
        player["firstname"],
        player["date_of_birth"],
        player["national_chess_id"],
        player["score"],
    )
    tournament_players.append(player_in)

number_of_matches = int(len(tournament_players) / 2)

match_list = []

player_draw_list = tournament_players.copy()

for i in range(number_of_matches):
    player_1 = player_draw_list.pop(0)
    player_2 = player_draw_list.pop(0)
    match_list.append(Match(player_1, player_2))

print(match_list[0].players[0])


round_1 = Round(match_list, "Round 1")

print(round_1.matches[0])
