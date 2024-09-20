"""Liste préliminaire des controlleurs à implémenter."""

import random
from models.players import Player
from models.matches import Match

# from models.tournament import Tournament
# from models.rounds import Round


class Controller:

    def __init__(self, players_list, previous_matches=None):
        if previous_matches is None:
            previous_matches = []

        self.players_list = players_list
        self.previous_matches = previous_matches

    def add_players(self):
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

    def draw_matches(self, tournament_players):
        tournament_players.sort(key=lambda player: player.score, reverse=True)
        number_of_matches = int(len(tournament_players) / 2)
        match_list = []

        player_draw_list = tournament_players.copy()

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


class CreateTounament:
    pass


class TournamentResults:
    """Give the result at the end of tournament"""

    def __init__(self, tournament):
        self.tournament = tournament
        self.ranking = sorted(
            self.tournament.players,
            key=lambda player: player.score,
            reverse=True,
        )
        self.winner = self.ranking[0]

    def __str__(self):
        """Used in print."""
        return (
            f"The winner is : {self.winner.name}\n"
            f"Classement final : {self.ranking}\n"
        )

    def __repr__(self):
        """Used in print."""
        return str(self)


class CreateMatch:
    pass


class CreateRound:
    pass


class MatchResult:

    def __init__(self, match, tournament_players):
        """Initialize the match result with a match and players"""
        self.match = match
        self.tournament_players = tournament_players
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

        for player in self.tournament_players:
            if self.winner == player.name:
                player.score += 1
            elif self.winner == "draw":
                if player.name in (
                    self.match.players[0].name,
                    self.match.players[1].name,
                ):
                    player.score += 0.5
