"""Define a player."""

from datetime import date, datetime
import re

DD_MM_YYYY = re.compile(
    r"^(3[01]|[12][0-9]|0?[1-9])(\/|-)(1[0-2]|0?[1-9])\2([0-9]{2})?[0-9]{2}$"
)
YYYY_MM_DD = re.compile(
    r"^([0-9]{2})?[0-9]{2}(\/|-)(1[0-2]|0?[1-9])\2(3[01]|[12][0-9]|0?[1-9])$"
)


class Player:
    """Player."""

    def __init__(
        self, lastname, firstname, date_of_birth, national_chess_id, score=0
    ):
        self.name = lastname + firstname
        if DD_MM_YYYY.match(date_of_birth):
            birthday = re.sub("/", "-", date_of_birth)
            self.date_of_birth = (
                datetime.strptime(birthday, "%d-%m-%Y")
                .date()
                .strftime("%d-%m-%Y")
            )
        elif YYYY_MM_DD.match(date_of_birth):
            birthday = re.sub("/", "-", date_of_birth)
            self.date_of_birth = date.fromisoformat(birthday).strftime(
                "%d-%m-%Y"
            )
        else:
            print(f"{date_of_birth} : Incorrect date format")
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
