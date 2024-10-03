"""Controllers to manage match related operations."""

import random


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
