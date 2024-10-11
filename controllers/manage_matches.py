"""Controllers to manage match related operations."""

import random
from models.matches import Match


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
                self.winner = self.match.players[0]
                break
            elif chosen_winner == "2":
                self.winner = self.match.players[1]
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
            if self.winner == "draw":
                if player.national_chess_id in (
                    self.match.players[0].national_chess_id,
                    self.match.players[1].national_chess_id,
                ):
                    player.score += 0.5
            elif self.winner.national_chess_id == player.national_chess_id:
                player.score += 1


class MatchDraw:

    def check_previous_matches(self, player_1, player_2, previous_matches):
        """Verify if match has already been played
        Return True if it has, false if not"""

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
