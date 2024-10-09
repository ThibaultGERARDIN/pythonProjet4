"""Main view"""

from .player_menu import PlayerMenu
from .tournament_menu import TournamentMenu


class View:

    def __init__(self):
        self.main_menu = (
            "Menu principal\n"
            "1 - Menu joueurs\n2 - Menu tournois\n"
            "0 - Quitter le programme\n"
        )
        self.player_menu = PlayerMenu().player_main_menu
        self.tournament_menu = TournamentMenu().menu
        self.selected_menu = 0
        self.display = True

    def display_menu(self):
        while self.display:
            if self.selected_menu == 0:
                print(self.main_menu)
                self.navigate_menus()
            elif self.selected_menu == 1:
                print(self.player_menu)
                self.navigate_menus()
            elif self.selected_menu == 2:
                print(self.tournament_menu)
                self.navigate_menus()
            else:
                print(
                    "Ce menu n'existe pas ! Merci de choisir"
                    " parmis les numéros disponibles."
                )
                self.navigate_menus()

    def navigate_menus(self):
        self.selected_menu = int(input("Tapez le numéro du menu souhaité :"))
