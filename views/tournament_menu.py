"""View for tournament related prints and inputs."""

import os
from tabulate import tabulate
from controllers.manage_data import CURRENT_TOURNAMENT_PATH
from models.rounds import Round


class TournamentMenu:
    """
    Define the tournament menu view and all methods linked.

    All prints and inputs concerning tournaments.
    """

    def __init__(self):
        """Initialize different menu if current tournament exists or not"""
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
        """Print main tournament menu"""
        print(self.tournament_main_menu)

    def navigate_main_menu(self):
        """Prompt to navigate menu, validate and return input."""
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

    def display_tournament_result(self, winner_name, ranking):
        """Print tournament result from winner name and tournament ranking"""
        rank_index = list(range(1, len(ranking) + 1))
        display_list = []
        for player in ranking:
            display_player = {}
            display_player["Nom"] = player.lastname
            display_player["Prénom"] = player.firstname
            display_player["Date de naissance"] = player.date_of_birth
            display_player["INE"] = player.national_chess_id
            display_player["Score final"] = player.score
            display_list.append(display_player)

        print(f"Tournoi terminé ! Le gagnant est : {winner_name}")
        print(
            tabulate(
                display_list,
                headers="keys",
                showindex=rank_index,
                tablefmt="mixed_grid",
            )
        )

    def tournament_infos_prompt(self):
        """
        Prompt to input tournament base information.

        Return dict with name, location, description, number_of_rounds.
        """
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
        number_of_rounds = input("Nombre de rounds (Par défaut = 4) :") or 4
        while True:
            try:
                int(number_of_rounds)
                break
            except ValueError:
                number_of_rounds = (
                    input("Merci de taper un chiffre (Par défaut = 4) :") or 4
                )
        tournament_infos["number_of_rounds"] = int(number_of_rounds)
        return tournament_infos

    def round_end(self, round_name):
        """Return "round_name ended" for ask y/n argument"""
        return f"{round_name} terminé, passage au round suivant."

    def display_round_matches(self, round=Round):
        """Print list of starting round matches"""
        print(f"Début du {round.round_name}\n" f"{round.matches}")

    def display_unfinished_round_matches(self, unfinished_round=Round):
        """Print list of re-starting round matches"""
        print(
            f"Reprise du {unfinished_round.round_name}\n"
            f"{unfinished_round.matches}"
        )

    def display_past_list(self, tournament_files_list):
        """
        Print list of past tournament files

        Prompt for file selection.
        Validate input and return int(input)
        """
        if len(tournament_files_list) == 0:
            print("Pas d'ancien tournoi trouvé, retour au menu.")
            return None
        else:
            i = 0
            for file in tournament_files_list:
                i += 1
                print(f"{i} : {file}")
            chosen_file = input(
                "Choisissez un tournoi à afficher en détail"
                " (0 pour retour au menu):"
            )
            while True:
                try:
                    int(chosen_file)
                    while int(chosen_file) not in range(
                        len(tournament_files_list) + 1
                    ):
                        chosen_file = input(
                            "Choix invalide. (0 pour retour au menu):"
                        )
                    if chosen_file == "0":
                        self.display_main_menu()
                        break
                    else:
                        return int(chosen_file)
                except (TypeError, ValueError):
                    chosen_file = input(
                        "Choix invalide. (0 pour retour au menu):"
                    )

    def choose_report_type(self):
        """
        Prompt to choose report type from list of choices.

        Validate input and return it.
        """
        report_choice = input(
            "Choisissez les données à afficher pour le tournoi choisi :\n"
            "1 - Rapport complet\n"
            "2 - Résultat final\n"
            "3 - Liste des rounds\n"
            "0 - Retour au menu tournoi\n"
        )
        while (
            not report_choice == "1"
            and not report_choice == "2"
            and not report_choice == "3"
            and not report_choice == "0"
        ):
            report_choice = input(
                "Choix invalide, merci de choisir parmis"
                " les numéros possibles :"
            )
        return report_choice

    def display_tournament_report(self, tournament_to_display, report_choice):
        """Transform and display tournament data according to report choice."""
        tournament_infos = tournament_to_display["static_infos"]
        tournament_infos["end_date"] = tournament_to_display[
            "static_infos"
        ].get("end_date", "Annulé")
        if "tournament_result" in tournament_to_display:
            tournament_result = tournament_to_display["tournament_result"]
        else:
            tournament_result = None
            tournament_players = tournament_to_display["tournament_players"]
        tournament_rounds = tournament_to_display["tournament_rounds"]
        if report_choice == "1":
            print(
                f"Nom du tournoi : {tournament_infos["name"]}\n"
                f"Lieu : {tournament_infos["location"]}\n"
                f"Date de début : {tournament_infos["start_date"]}\n"
                f"Date de fin : {tournament_infos["end_date"]}\n"
                f"Description : {tournament_infos["description"]}\n"
                f"Nombre de rounds : {tournament_infos["number_of_rounds"]}\n"
            )
            if tournament_result:
                tournament_winner = tournament_result.pop(0)
                print(tournament_winner)
                rank_index = list(range(1, len(tournament_result) + 1))
                print(
                    tabulate(
                        tournament_result,
                        headers="keys",
                        showindex=rank_index,
                        tablefmt="mixed_grid",
                    )
                )
            else:
                print("Tournoi annulé avant la fin, liste des joueurs :")
                print(
                    tabulate(
                        tournament_players,
                        headers="keys",
                        tablefmt="mixed_grid",
                    )
                )
            print("Liste des rounds du tournoi :\n")
            for round in tournament_rounds:
                round_name = round["round_name"]
                start_time = round["start_time"]
                i = 0
                match_list = []
                for match in round["matches"]:
                    i += 1
                    match_in = f"Match {i}: {match[0]} vs {match[1]}"
                    match_list.append(match_in)
                round_result = round["result"]
                end_time = round["end_time"]
                print(
                    f"{round_name} :\n"
                    f"Début : {start_time}\n"
                    f"Matchs : {match_list}\n"
                    f"Résultats : {round_result}\n"
                    f"Fin : {end_time}\n"
                )
        elif report_choice == "2" and tournament_result:
            tournament_winner = tournament_result.pop(0)
            print(tournament_winner)
            rank_index = list(range(1, len(tournament_result) + 1))
            print(
                tabulate(
                    tournament_result,
                    headers="keys",
                    showindex=rank_index,
                    tablefmt="mixed_grid",
                )
            )
        elif report_choice == "2" and tournament_players:
            print("Tournoi annulé avant la fin, liste des joueurs :")
            print(
                tabulate(
                    tournament_players,
                    headers="keys",
                    tablefmt="mixed_grid",
                )
            )
        else:
            print("Liste des rounds du tournoi :\n")
            for round in tournament_rounds:
                round_name = round["round_name"]
                start_time = round["start_time"]
                i = 0
                match_list = []
                for match in round["matches"]:
                    i += 1
                    match_in = f"Match {i}: {match[0]} vs {match[1]}"
                    match_list.append(match_in)
                round_result = round["result"]
                end_time = round["end_time"]
                print(
                    f"{round_name} :\n"
                    f"Début : {start_time}\n"
                    f"Matchs : {match_list}\n"
                    f"Résultats : {round_result}\n"
                    f"Fin : {end_time}\n"
                )
