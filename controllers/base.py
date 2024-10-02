"""Define the main controllers used in the program."""

import random
from models.players import Player
from models.matches import Match
from models.rounds import Round
from models.tournament import Tournament
from controllers.crud import SaveTournament


class Controller:

    def __init__(self, tournament):

        self.players = tournament.players
        self.previous_matches = tournament.previous_matches
        self.saver = SaveTournament(tournament)

    def check_previous_matches(self, player_1, player_2):
        """Verify if match has already been played
        Return True if it has, false if not"""

        for match in self.previous_matches:
            if (
                match.players[0].name == player_1.name
                and match.players[1].name == player_2.name
            ) or (
                match.players[0].name == player_2.name
                and match.players[1].name == player_1.name
            ):
                return True

        return False

    def draw_matches(self):
        self.players.sort(key=lambda player: player.score, reverse=True)
        number_of_matches = int(len(self.players) / 2)
        match_list = []

        player_draw_list = self.players.copy()

        for i in range(number_of_matches):
            player_1 = player_draw_list.pop(0)
            player_2 = player_draw_list.pop(0)
            match_already_played = self.check_previous_matches(
                player_1, player_2
            )
            attempts = 0
            while match_already_played and attempts < len(player_draw_list):
                player_draw_list.append(player_2)
                player_2 = player_draw_list.pop(0)
                match_already_played = self.check_previous_matches(
                    player_1, player_2
                )
                attempts += 1
                if attempts >= len(player_draw_list):
                    # S'il n'est pas possible de trouver un match non répété
                    print("Aucun match non répété n'a pu être trouvé.")
            player_draw_list.sort(
                key=lambda player: player.score, reverse=True
            )
            match_list.append(Match(player_1, player_2))
        self.previous_matches.extend(match_list)
        return match_list

    def start_tournament(self, tournament):
        """Start (or restart) the tournament"""
        if (
            0 < tournament.current_round <= len(tournament.rounds)
            and tournament.rounds[tournament.current_round - 1].end_time
            == "Round en cours"
        ):
            unfinished_round = tournament.rounds[tournament.current_round - 1]
            for i in range(len(unfinished_round.result), 4):
                match_result = MatchResult(
                    unfinished_round.matches[i], tournament
                )
                match_result.select_winner()
                match_result.add_score()
                unfinished_round.record_result(i, match_result.winner)
                self.saver.save_state()
            unfinished_round.finish_round()
            self.saver.save_state()

        for i in range(tournament.current_round, tournament.number_of_rounds):
            tournament.current_round += 1
            self.saver.current_round = tournament.current_round
            match_list = self.draw_matches()
            round = Round(match_list, i + 1)
            tournament.rounds.append(round)
            match_index = 0
            for match in round.matches:
                match_index += 1
                match_result = MatchResult(match, tournament)
                match_result.select_winner()
                match_result.add_score()
                round.record_result(match_index, match_result.winner)
                self.saver.save_state()
            round.finish_round()
            self.saver.save_state()
        print(f"Tournoi terminé ! {tournament.result()}")
        self.saver.end_save()


class ReloadTounament:
    """Reacreate tournament from current tournament infos."""

    def __init__(
        self,
        players_list,
        tournament_infos,
        tournament_rounds,
        tournament_previous_matches,
    ):
        self.players_list = players_list
        self.infos = tournament_infos
        self.rounds = tournament_rounds
        self.previous_matches = tournament_previous_matches

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
        tournament.previous_matches = self.recreate_match(
            self.previous_matches
        )
        return tournament


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
                player["score"],
            )
            tournament_players.append(player_in)
        return tournament_players


class MatchResult:

    def __init__(self, match, tournament):
        """Initialize the match result with a match and players"""
        self.match = match
        self.players = tournament.players
        self.winner = None

    def test_select_winner(self):
        """Randomly select winner of the match (for testing purposes)"""
        chosen_winner = random.randint(1, 3)
        if chosen_winner == 1:
            self.winner = self.match.players[0].name
        elif chosen_winner == 2:
            self.winner = self.match.players[1].name
        else:
            self.winner = "draw"

        return self.winner

    def select_winner(self):
        """Choose winner of the match"""
        while True:
            chosen_winner = input(
                f"Merci d'indiquer le gagnant du match {self.match} :\n"
                f"1 - {self.match.players[0].name}\n"
                f"2 - {self.match.players[1].name}\n"
                f"3 - Match nul\n"
            )

            if chosen_winner == "1":
                self.winner = self.match.players[0].name
                break
            elif chosen_winner == "2":
                self.winner = self.match.players[1].name
                break
            elif chosen_winner == "3":
                self.winner = "draw"
                break
            else:
                print("Choix invalide : merci de répondre par 1, 2 ou 3")
        return self.winner

    def add_score(self):
        """Add score to the winner and players involved in the match"""
        if self.winner is None:
            raise ValueError("Winner must be selected before adding scores.")

        for player in self.players:
            if self.winner == player.name:
                player.score += 1
            elif self.winner == "draw":
                if player.name in (
                    self.match.players[0].name,
                    self.match.players[1].name,
                ):
                    player.score += 0.5
