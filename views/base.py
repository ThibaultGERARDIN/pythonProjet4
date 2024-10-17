"""Main menu view"""


class View:
    """Define main menu of program."""

    def __init__(self):
        self.main_menu = (
            "Gestionnaire de tournoi d'échecs\n"
            "Menu principal :\n"
            "1 - Menu joueurs\n"
            "2 - Menu tournois\n"
            "0 - Quitter le programme\n"
        )

    def display_main_menu(self):
        """Print the menu"""
        print(self.main_menu)

    def navigate_main_menu(self):
        """Prompt for main menu navigation. Validate and Return input."""
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
        """
        Method for yes/no question.

        Print the given message.
        Ask for y or n answer. (Check if correct)
        Return answer.
        """
        answer = input(f"{message} (y/n) :")
        while not answer == "y" and not answer == "n":
            answer = input("Merci de répondre y ou n.")
        return answer
