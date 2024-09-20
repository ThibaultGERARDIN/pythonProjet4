"""Define a player."""

from datetime import date


class Player:
    """Player."""

    def __init__(
        self, lastname, firstname, date_of_birth, national_chess_id, score=0
    ):
        self.name = lastname + firstname
        self.date_of_birth = date.fromisoformat(date_of_birth).strftime(
            "%d/%m/%Y"
        )
        self.national_chess_id = national_chess_id
        self.score = score
        self.lastname = lastname
        self.firstname = firstname

    def __str__(self):
        """Used in print."""
        return (
            f"Nom : {self.lastname} Prénom : {self.firstname}\n"
            f"Date de naissance : {self.date_of_birth}\n"
            f"N°INE : {self.national_chess_id}\nScore : {self.score}\n"
        )

    def __repr__(self):
        """Used in print."""
        return str(self)
