"""Tournament menu"""

import os
from controllers.manage_data import CURRENT_TOURNAMENT_PATH


class TournamentMenu:
    """Tournament menu view"""

    def __init__(self):
        if os.path.isdir(f"{CURRENT_TOURNAMENT_PATH}"):
            self.menu = (
                "Menu tournois\n"
                "1 - Liste des tournois passés\n"
                "2 - Continuer le tournoi en cours\n"
                "3 - Annuler le tournoi en cours\n0 - Retour"
            )
        else:
            self.menu = (
                "Menu tournois\n"
                "1 - Liste des tournois passés\n"
                "2 - Créer un nouveau tournoi\n"
                "0 - Retour"
            )
