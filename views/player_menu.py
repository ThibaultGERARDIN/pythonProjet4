"""View for player related prints and inputs."""

import re
from tabulate import tabulate
from models.players import DD_MM_YYYY, YYYY_MM_DD

INE_CHECK = re.compile(r"^([A-Z, a-z]{2})([0-9]{5}$)")


class PlayerMenu:
    """
    Define the player menu view and all methods linked.

    All prints and inputs concerning players.
    """

    def __init__(self):
        """Initialize the different player menus."""
        self.player_main_menu = (
            "Menu joueurs\n"
            "1 - Afficher la liste des joueurs\n"
            "2 - Ajouter un joueur\n"
            "3 - Chercher un joueur\n"
            "4 - Modifier un joueur\n"
            "0 - Retour\n"
        )
        self.player_selection_menu = (
            "Choix des participants au tournoi :\n"
            "1 - Depuis la liste de joueurs\n"
            "2 - Créer un nouveau joueur\n"
            "3 - Afficher la liste des joueurs sélectionnés\n"
            "4 - Modifier la liste des joueurs sélectionnés\n"
            "5 - Valider les choix et créer le tournoi\n"
            "0 - Annuler et revenir au menu principal\n"
        )
        self.player_search_menu = (
            "Rechercher un joueur :\n"
            "1 - Par nom de famille\n"
            "2 - Par INE\n"
            "0 - Annuler et revenir au menu joueur\n"
        )
        self.exit_menu = (
            "1 - Retour au menu joueur\n" "2 - Retour au menu principal\n"
        )

    def display_main_menu(self):
        """Print main player menu."""
        print(self.player_main_menu)

    def navigate_main_menu(self):
        """Prompt for main menu navigation. Validate and Return input."""
        selected_menu = input("Tapez le numéro du menu souhaité :")
        while (
            not selected_menu == "1"
            and not selected_menu == "2"
            and not selected_menu == "3"
            and not selected_menu == "4"
            and not selected_menu == "0"
        ):
            selected_menu = input(
                "Choix invalide, merci de choisir parmis"
                " les numéros possibles :"
            )
        return selected_menu

    def exit_player_menu_prompt(self):
        """Prompt for display menu navigation. Validate and Return input."""
        choice = input(self.exit_menu)
        while not choice == "1" and not choice == "2":
            choice = input(
                "Choix invalide, merci de choisir parmis"
                " les numéros possibles :"
            )
        return choice

    def player_selection_prompt(self):
        """Prompt for selection menu navigation. Validate and Return input."""
        choice = input(self.player_selection_menu)
        while (
            not choice == "1"
            and not choice == "2"
            and not choice == "3"
            and not choice == "4"
            and not choice == "5"
            and not choice == "0"
        ):
            choice = input(
                "Choix invalide, merci de choisir parmis"
                " les numéros possibles :"
            )
        return choice

    def select_winner_prompt(self, match):
        """Prompt for winner menu navigation. Validate and Return winner."""
        chosen_winner = input(
            f"Merci d'indiquer le gagnant du match {match} :\n"
            f"1 - {match.players[0].name}\n"
            f"2 - {match.players[1].name}\n"
            f"3 - Match nul\n"
        )
        while (
            not chosen_winner == "1"
            and not chosen_winner == "2"
            and not chosen_winner == "3"
        ):
            chosen_winner = input("Choix invalide, merci de choisir 1, 2 ou 3")
        if chosen_winner == "1":
            winner = match.players[0]
        elif chosen_winner == "2":
            winner = match.players[1]
        else:
            winner = "draw"
        return winner

    def display_complete_list(self, players_list):
        """
        Display full list of player information in a table.

        Lastname, Firstname, Birthday and INE. With index.
        """
        display_list = []
        for player in players_list:
            display_player = {
                "Nom": player["lastname"],
                "Prénom": player["firstname"],
                "Date de naissance": player["date_of_birth"],
                "INE": player["national_chess_id"],
            }
            display_list.append(display_player)
        print(
            tabulate(
                display_list,
                headers="keys",
                showindex="always",
                tablefmt="mixed_grid",
            )
        )

    def display_choice_list(self, players_list):
        """
        Display reduced list of player information in a table.

        FullName, and INE. With index.
        """
        display_players_list = []
        for player in players_list:
            display_player = {
                "NomComplet": player["name"],
                "INE": player["national_chess_id"],
            }
            display_players_list.append(display_player)
        print(
            tabulate(
                display_players_list,
                headers="keys",
                showindex="always",
                tablefmt="mixed_grid",
            )
        )

    def player_choice_add_prompt(self):
        """
        Prompt to select players in list.

        Validate and transform input
        Return a list of int indexes.
        """
        player_choice = input(
            "Sélectionnez le/les joueurs à ajouter"
            " au tournoi (tapez le/les numéros choisis"
            " séparés par , ou . ou espace)"
        )
        int_choice = re.sub(r"[a-zA-Z]+", "", player_choice)
        cleaned_list = re.split(r",|\.| ", int_choice)
        selected_indexes = []
        try:
            cleaned_list.remove("")
        except ValueError:
            pass
        for choice in cleaned_list:
            try:
                int(choice)
                selected_indexes.append(int(choice))
            except (TypeError, ValueError):
                pass
        return selected_indexes

    def player_choice_remove_prompt(self, player_list):
        """
        Prompt to remove player from list.

        Validate input and Return int(input) or None.
        """
        player_choice = input(
            "Sélectionnez le joueur à retirer du tournoi"
            " (Entrée pour retour au menu):"
        )
        while True:
            if not player_choice:
                print("Aucun joueur selectionné.")
                return None
            else:
                try:
                    int(player_choice)
                    if int(player_choice) in range(len(player_list)):
                        return int(player_choice)
                    else:
                        player_choice = input(
                            f"Choix {player_choice} invalide."
                            " Merci de choisir un numéro dans la liste"
                            " (Entrée pour retour au menu):"
                        )
                except (TypeError, ValueError):
                    player_choice = input(
                        f"Choix {player_choice} invalide."
                        " Merci de choisir un numéro dans la liste"
                        " (Entrée pour retour au menu):"
                    )

    def display_removed_player(self, player):
        """Print name of given removed player."""
        print(f"Le joueur {player["name"]} a bien été retiré du tournoi.")

    def search_player_prompt(self):
        """
        Display and Prompt for player search menu.

        Validate and return input.
        """
        search_by = input(self.player_search_menu)
        while (
            not search_by == "1"
            and not search_by == "2"
            and not search_by == "0"
        ):
            search_by = input("Choix invalide, veuillez réessayer.")
        return search_by

    def search_ine_prompt(self):
        """
        Prompt for INE search

        Validate input to match INE
        Return input.upper()
        """
        player_ine = input(
            "Tapez le numéro INE du joueur recherché (ex: AB12345) :"
        )
        while not INE_CHECK.match(player_ine):
            player_ine = input(
                "INE incorrect, doit correspondre à"
                " 2 lettres suivies de 5 chiffres (ex:AB12345) :"
            )
        return player_ine.upper()

    def search_name_prompt(self):
        """Prompt for name search. Return input"""
        player_name = input("Tapez le nom de famille du joueur recherché :")
        return player_name

    def player_choice_update_prompt(self, search_list):
        """
        Prompt to select player to update from list.

        Validate input and return int(input)
        """
        player_choice = input("Sélectionnez le joueur à modifier :")
        while True:
            try:
                int(player_choice)
                if int(player_choice) in range(len(search_list)):
                    return int(player_choice)
                else:
                    player_choice = input(
                        f"Choix {player_choice} invalide."
                        " Merci de choisir un numéro dans la liste"
                        " (Entrée pour retour au menu):"
                    )
            except (TypeError, ValueError):
                player_choice = input(
                    f"Choix {player_choice} invalide."
                    " Merci de choisir un numéro dans la liste"
                    " (Entrée pour retour au menu):"
                )

    def update_player_prompt(self, player: dict):
        """
        Prompt to update player info from player dict.

        Return updated player dict.
        """
        updated_player_data = {}
        print(
            "Vous pouvez modifier les données ci-après"
            ' (tapez "ENTREE" pour garder la valeur.)'
        )
        updated_player_data["lastname"] = (
            input(f"Modifier nom : {player["lastname"]} ?")
            or player["lastname"]
        )
        updated_player_data["firstname"] = (
            input(f"Modifier prénom : {player["firstname"]} ?")
            or player["firstname"]
        )
        updated_player_data["date_of_birth"] = (
            input(f"Modifier date de naissance : {player["date_of_birth"]} ?")
            or player["date_of_birth"]
        )
        while not DD_MM_YYYY.match(
            updated_player_data["date_of_birth"]
        ) and not YYYY_MM_DD.match(updated_player_data["date_of_birth"]):
            updated_player_data["date_of_birth"] = input(
                "Date non reconnue, merci de donner une date"
                " au format DD(-/)MM(-/)YYYY ou YYYY(-/)MM(-/)DD :"
            )
        updated_player_data["national_chess_id"] = (
            input(f"Modifier INE : {player["national_chess_id"]} ?")
            or player["national_chess_id"]
        )
        while not INE_CHECK.match(updated_player_data["national_chess_id"]):
            updated_player_data["national_chess_id"] = input(
                "INE incorrect, doit correspondre à"
                " 2 lettres suivies de 5 chiffres (ex:AB12345) :"
            )
        return updated_player_data

    def confirm_player_update(self, player_to_update, updated_player):
        """
        Prompt to validate updated player data.

        Print old_data => new_data.
        Ask y/n and return answer.
        """
        confirm_update = self.ask_y_n(
            f"Nom : {player_to_update["lastname"]}"
            f" => {updated_player["lastname"]}\n"
            f"Prénom : {player_to_update["firstname"]}"
            f" => {updated_player["firstname"]}\n"
            f"Date de naissance : {player_to_update["date_of_birth"]}"
            f" => {updated_player["date_of_birth"]}\n"
            f"INE : {player_to_update["national_chess_id"]}"
            f" => {updated_player["national_chess_id"]}\n"
            "Confirmer les modifications ?"
        )
        return confirm_update

    def create_player_prompt(self):
        """
        Prompt to create new player.

        Input successive data and return player dict.
        """
        new_player_data = {}
        print(
            "Compléter les données demandées ci-dessous"
            " pour ajouter un joueur à la base de données :"
        )
        new_player_data["lastname"] = input("Nom :")
        new_player_data["firstname"] = input("Prénom :")
        new_player_data["date_of_birth"] = input("Date de naissance :")
        while not DD_MM_YYYY.match(
            new_player_data["date_of_birth"]
        ) and not YYYY_MM_DD.match(new_player_data["date_of_birth"]):
            new_player_data["date_of_birth"] = input(
                "Date non reconnue, merci de donner une date"
                " au format DD(-/)MM(-/)YYYY ou YYYY(-/)MM(-/)DD :"
            )
        new_player_data["national_chess_id"] = input(
            "Identifiant National d'Echec :"
        )
        while not INE_CHECK.match(new_player_data["national_chess_id"]):
            new_player_data["national_chess_id"] = input(
                "INE incorrect, doit correspondre à"
                " 2 lettres suivies de 5 chiffres (ex:AB12345) :"
            )
        return new_player_data

    def player_already_in(self, player_name):
        """Print player already in tournament."""
        print(f"Le joueur {player_name} est déjà inscrit.")

    def player_added(self, player_name):
        """Print player successfully added to tournament."""
        print(f"Le joueur {player_name} a été ajouté au tournoi.")

    def added_in_database(self, player_name):
        """Print player successfully added to database."""
        print(f"Le joueur {player_name} a été ajouté à la base de données.")

    def already_in_database(self, player_national_chess_id):
        """Print player already in database with player INE."""
        print(
            f"Un joueur avec l'INE {player_national_chess_id}"
            " est déjà dans la liste, veuillez réessayer."
        )

    def player_not_in(self):
        """Print player doesn't exist"""
        print("Aucun joueur trouvé, veuillez le rajouter.")

    def too_many_players(self, number_of_players, player_name=None):
        """
        Print too many players (number of players). Plus player name if given
        """
        if player_name:
            print(
                f"Le joueur {player_name}"
                " n'a pu être ajouté, nombre"
                " maximum atteint"
                f" ({number_of_players} joueurs)."
            )
        else:
            print(
                "Nombre maximum de joueurs atteint"
                f" ({number_of_players} joueurs)"
            )

    def number_selected(self, number_selected, number_of_players):
        """Print (number_selected / number_of_players)"""
        print(
            f"Vous devez selectionner {number_of_players} joueurs :\n"
            f" ({number_selected}/{number_of_players})"
            " sélectionnés."
        )

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
