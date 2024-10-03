"""Define the main controllers used in the program."""

from models.matches import Match
from models.rounds import Round
from controllers.manage_data import SaveTournament
from controllers.manage_matches import MatchResult


class Controller:

    def __init__(self, tournament):

        self.players = tournament.players
        self.previous_matches = []
        for round in tournament.rounds:
            for match in round.matches:
                self.previous_matches.append(match)
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
            print(
                f"{unfinished_round.round_name}"
                " terminé, passage au round suivant."
            )
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
            print(f"{round.round_name}" " terminé, passage au round suivant.")
            self.saver.save_state()
        print(f"Tournoi terminé ! {tournament.result()}")
        self.saver.end_save()
