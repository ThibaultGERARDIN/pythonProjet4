"""Controllers to manage tournament related operations."""

from models.tournament import Tournament
from models.matches import Match
from models.rounds import Round
from controllers.manage_players import AddPlayers


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

    def get_players(self):
        tournament_players = AddPlayers(self.players_list).tournament_players()
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
