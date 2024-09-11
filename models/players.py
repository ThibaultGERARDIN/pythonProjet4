class Player:
    """Définit un joueur."""

    def __init__(
        self, lastname, firstname, date_of_birth, national_chess_id, score=0
    ):
        self.lastname = lastname
        self.firstname = firstname
        self.date_of_birth = date_of_birth
        self.national_chess_id = national_chess_id
        self.score = score
