"""Controllers to manage match related operations."""

from views.player_menu import PlayerMenu
from models.matches import Match


class MatchResult:
    """Determine match winner and add score to player(s)."""

    def __init__(self, match, tournament):
        """Initialize with a match and tournament."""
        self.match = match
        self.players = tournament.players
        self.winner = None
        self.view = PlayerMenu()

    def select_winner(self):
        """Choose winner of the match from input."""
        self.winner = self.view.select_winner_prompt(self.match)
        return self.winner

    def add_score(self):
        """Add score to the winner(s) of the match."""
        if self.winner is None:
            raise ValueError("Le gagnant n'a pas été sélectionné !")

        for player in self.players:
            if self.winner == "draw":
                if player.national_chess_id in (
                    self.match.players[0].national_chess_id,
                    self.match.players[1].national_chess_id,
                ):
                    player.score += 0.5
            elif self.winner.national_chess_id == player.national_chess_id:
                player.score += 1


class MatchDraw:
    """Draw matches to create list for a new round."""

    def check_previous_matches(self, player_1, player_2, previous_matches):
        """
        Verify if match has already been played

        Compare players national chess ID to determine
        previous pairings vs current pairing
        Return True if it has, false if not
        """

        for match in previous_matches:
            if (
                match.players[0].national_chess_id
                == player_1.national_chess_id
                and match.players[1].national_chess_id
                == player_2.national_chess_id
            ) or (
                match.players[0].national_chess_id
                == player_2.national_chess_id
                and match.players[1].national_chess_id
                == player_1.national_chess_id
            ):
                return True
        return False

    def draw_matches(self, players_list, previous_matches):
        """
        Create new match list for a round

        Check previous matches
        Sort players by score
        Pair players in new match
        Return list of matches
        """
        players_list.sort(key=lambda player: player.score, reverse=True)
        number_of_matches = int(len(players_list) / 2)
        match_list = []
        player_draw_list = players_list.copy()
        for i in range(number_of_matches):
            player_1 = player_draw_list.pop(0)
            player_2 = player_draw_list.pop(0)
            match_already_played = self.check_previous_matches(
                player_1, player_2, previous_matches
            )
            attempts = 0
            while match_already_played and attempts < len(player_draw_list):
                player_draw_list.append(player_2)
                player_2 = player_draw_list.pop(0)
                match_already_played = self.check_previous_matches(
                    player_1, player_2, previous_matches
                )
                attempts += 1
                if attempts >= len(player_draw_list):
                    print("Aucun match non répété n'a pu être trouvé.")
            player_draw_list.sort(
                key=lambda player: player.score, reverse=True
            )
            match_list.append(Match(player_1, player_2))
        previous_matches.extend(match_list)
        return match_list
