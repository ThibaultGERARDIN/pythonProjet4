"""Tournament menu"""

import os
from controllers.manage_data import CURRENT_TOURNAMENT_PATH
from models.rounds import Round


class TournamentMenu:
    """Tournament menu view"""

    def __init__(self):
        if os.path.isdir(f"{CURRENT_TOURNAMENT_PATH}"):
            self.tournoi_existant = True
            self.tournament_main_menu = (
                "Menu tournois\n"
                "1 - Liste des tournois passés\n"
                "2 - Continuer le tournoi en cours\n"
                "3 - Créer un nouveau tournoi (annulera le tournoi en cours)\n"
                "0 - Retour\n"
            )
        else:
            self.tournoi_existant = False
            self.tournament_main_menu = (
                "Menu tournois\n"
                "1 - Liste des tournois passés\n"
                "2 - Créer un nouveau tournoi\n"
                "0 - Retour\n"
            )

    def display_main_menu(self):
        print(self.tournament_main_menu)

    def navigate_main_menu(self):
        selected_menu = input("Tapez le numéro du menu souhaité :")
        if self.tournoi_existant:
            while (
                not selected_menu == "1"
                and not selected_menu == "2"
                and not selected_menu == "3"
                and not selected_menu == "0"
            ):
                selected_menu = input(
                    "Choix invalide, merci de choisir parmis"
                    " les numéros possibles :"
                )
        else:
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

    def tournament_infos_prompt(self):
        tournament_infos = {}
        print(
            "Pour créer un nouveau tournoi"
            " merci de compléter les infos ci-dessous :\n"
        )
        tournament_infos["name"] = input("Nom du tournoi :")
        tournament_infos["location"] = input("Lieu :")
        tournament_infos["description"] = (
            input("Description (Par défaut = Tournoi d'échec) :")
            or "Tournoi d'échec"
        )
        tournament_infos["number_of_rounds"] = (
            input("Nombre de rounds (Par défaut = 4) :") or 4
        )
        return tournament_infos

    def round_end(self, round_name):
        return f"{round_name} terminé, passage au round suivant."

    def tournament_end(self, tounrament_result):
        print(f"Tournoi terminé ! {tounrament_result}")

    def display_round_matches(self, round=Round):
        print(f"Début du {round.round_name}\n" f"{round.matches}")

    def display_unfinished_round_matches(self, unfinished_round=Round):
        print(
            f"Reprise du {unfinished_round.round_name}\n"
            f"{unfinished_round.matches}"
        )

    def display_past_list(self, tournament_files_list):
        i = 0
        for file in tournament_files_list:
            i += 1
            print(f"{i} : {file}")
        chosen_file = input(
            "Choisissez un tournoi à afficher en détail"
            " (0 pour retour au menu):"
        )
        while chosen_file not in range(i):
            chosen_file = input(
                "Choix invalide, réessayez (0 pour retour au menu):"
            )
        if chosen_file == "0":
            self.display_main_menu()
        else:
            return chosen_file

    def choose_report_type(self):
        report_choice = input(
            "Choisissez les données à afficher pour le tournoi choisi :"
            "1 - Rapport complet"
            "2 - Résultat final"
            "3 - Liste des rounds"
            "0 - Retour au menu tournoi"
        )
        return report_choice
