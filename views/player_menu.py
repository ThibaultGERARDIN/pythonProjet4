"""Player menu"""

import re
from models.players import DD_MM_YYYY, YYYY_MM_DD

INE_CHECK = re.compile(r"^([A-Z, a-z]{2})([0-9]{5}$)")


class PlayerMenu:
    """Player menu view"""

    def __init__(self):
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
            "4 - Valider les choix et créer le tournoi\n"
            "0 - Annuler et revenir au menu principal\n"
        )
        self.player_search_menu = (
            "Rechercher un joueur :\n"
            "1 - Par nom de famille\n"
            "2 - Par INE\n"
            "0 - Annuler et revenir au menu joueur\n"
        )
        self.player_display_menu = (
            "1 - Retour au menu joueur\n" "2 - Retour au menu principal\n"
        )

    def display_main_menu(self):
        print(self.player_main_menu)

    def navigate_main_menu(self):
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

    def exit_players_list_prompt(self):
        choice = input(self.player_display_menu)
        while not choice == "1" and not choice == "2":
            choice = input(
                "Choix invalide, merci de choisir parmis"
                " les numéros possibles :"
            )
        return choice

    def player_selection_prompt(self):
        choice = input(self.player_selection_menu)
        return choice

    def display_complete_list(self, players_list):
        i = 0
        for player in players_list:
            display_player = [
                f"Nom : {player["lastname"]}",
                f"Prénom : {player["firstname"]}",
                f"Date de naissance : {player["date_of_birth"]}",
                f"INE : {player["national_chess_id"]}",
            ]
            print(f"{i} :{display_player}\n")
            i += 1

    def display_choice_list(self, players_list):
        display_players_list = []
        for player in players_list:
            display_player = [
                f"Choix {players_list.index(player)}",
                f"NomPrenom : {player["name"]}",
                f"INE : {player["national_chess_id"]}",
            ]
            display_players_list.append(display_player)
        print(display_players_list)

    def player_choice_add_prompt(self):
        player_choice = input(
            "Sélectionnez le/les joueurs à ajouter"
            " au tournoi (tapez le/les numéros choisis"
            " séparés par , ou . ou espace)"
        )
        return player_choice

    def search_player_prompt(self):
        search_by = input(self.player_search_menu)
        return search_by

    def search_ine_prompt(self):
        player_ine = input(
            "Tapez le numéro INE du joueur recherché (ex: AB12345) :"
        )
        return player_ine

    def search_name_prompt(self):
        player_name = input("Tapez le nom de famille du joueur recherché :")
        return player_name

    def player_choice_update_prompt(self):
        player_choice = input("Sélectionnez le joueur à modifier :")
        return player_choice

    def update_player_prompt(self, player: dict):
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

    def create_player_prompt(self):
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
        print(f"Le joueur {player_name} est déjà inscrit.")

    def player_added(self, player_name):
        print(f"Le joueur {player_name} a été ajouté au tournoi.")

    def too_many_players(self, number_of_players, player_name=None):
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
        print(
            f"Vous devez selectionner {number_of_players} joueurs :\n"
            f" ({number_selected}/{number_of_players})"
            " sélectionnés."
        )

    def confirm_player_update(self, player_to_update, updated_player):
        confirm_update = self.ask_y_n(
            f"{player_to_update["lastname"]} => {updated_player["lastname"]}\n"
            f"{player_to_update["firstname"]}"
            f" => {updated_player["firstname"]}\n"
            f"{player_to_update["date_of_birth"]}"
            f" => {updated_player["date_of_birth"]}\n"
            f"{player_to_update["national_chess_id"]}"
            f" => {updated_player["national_chess_id"]}\n"
            "Confirmer les modifications ?"
        )
        return confirm_update

    def ask_y_n(self, message):
        answer = input(f"{message} (y/n) :")
        while not answer == "y" and not answer == "n":
            answer = input("Merci de répondre y ou n.")
        return answer
