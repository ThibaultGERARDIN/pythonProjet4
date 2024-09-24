"""Define the main controllers used in the program."""

import random
from models.players import Player
from models.matches import Match
from models.rounds import Round


class Controller:

    def __init__(self, tournament):

        self.players = tournament.players
        self.previous_matches = tournament.previous_matches

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
        for i in range(tournament.number_of_rounds):

            tournament.current_round = i + 1
            match_list = self.draw_matches()

            round = Round(match_list, f"Round {i+1}")

            for match in round.matches:
                match_result = MatchResult(match, tournament)
                match_result.select_winner()
                match_result.add_score()

            tournament.rounds.append(round)


class CreateTounament:

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

    def select_winner(self):
        """Randomly select winner of the match"""
        chosen_winner = random.randint(1, 3)
        if chosen_winner == 1:
            self.winner = self.match.players[0].name
        elif chosen_winner == 2:
            self.winner = self.match.players[1].name
        else:
            self.winner = "draw"

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
