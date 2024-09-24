"""Main view"""


class Menu:

    def __init__(self):
        self.main_menu = (
            "Menu principal\n" "1 - Menu joueurs\n2 - Menu tournois"
        )
        self.player_menu = (
            "Menu joueurs\n"
            "1 - Ajouter un joueur\n2 - Afficher la liste\n0 - Retour"
        )
        self.tournament_menu = (
            "Menu tournois\n"
            "1 - Liste des tournois\n2 - Créer nouveau tournoi\n"
            "3 - Continuer tournoi\n4 - Commencer tournoi\n0 - Retour"
        )
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
                self.display = False

    def navigate_menus(self):
        self.selected_menu = int(input("Tapez le numéro du menu souhaité :"))
