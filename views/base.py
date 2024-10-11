"""Main view"""


class View:

    def __init__(self):
        self.main_menu = (
            "Menu principal\n"
            "1 - Menu joueurs\n"
            "2 - Menu tournois\n"
            "0 - Quitter le programme\n"
        )

    def display_main_menu(self):
        print(self.main_menu)

    def navigate_main_menu(self):
        selected_menu = input("Tapez le numéro du menu souhaité :")
        while (
            not selected_menu == "1"
            and not selected_menu == "2"
            and not selected_menu == "0"
        ):
            selected_menu = input(
                "Choix invalide, merci de choisir parmis"
                " les numéros possibles :"
            )
        return selected_menu

    def ask_y_n(self, message):
        answer = input(f"{message} (y/n) :")
        while not answer == "y" and not answer == "n":
            answer = input("Merci de répondre y ou n.")
        return answer
