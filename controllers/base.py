"""Liste préliminaire des controlleurs à implémenter."""

import random


class AddPlayer:
    pass


class CreateTounament:
    pass


class StartTournament:
    pass


class CreateMatch:
    pass


class CreateRound:
    pass


class MatchResult:

    def select_winner(self):
        winner = random.randint(1, 3)
        if winner == 1:
            pass
