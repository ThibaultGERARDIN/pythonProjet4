"""Define the main controller used in the program."""

import os
from views.base import View
from views.player_menu import PlayerMenu
from views.tournament_menu import TournamentMenu
from controllers.manage_players import ManagePlayers, PLAYER_DATA_PATH
from controllers.manage_tournaments import (
    CreateTournament,
    PlayTournament,
    ReloadTounament,
)
from controllers.manage_data import LoadData, SaveData, PAST_TOURNAMENT_PATH
from helpers.helpers import Helper


class Controller:
    """Main controller

    Initialize the views
    Navigate the menus and use relevant methods.
    """

    def __init__(self):
        """Initialize views and methods needed."""
        self.base_view = View()
        self.player_view = PlayerMenu()
        self.tournament_view = TournamentMenu()
        self.player_manager = ManagePlayers()
        self.helper = Helper()
        self.loader = LoadData()

    def display_main_menu(self):
        """Display the main menu and navigate it"""
        while True:
            self.base_view.display_main_menu()
            menu_choice = self.base_view.navigate_main_menu()
            if menu_choice == "1":
                self.display_player_menu()
            elif menu_choice == "2":
                self.display_tournament_menu()
            else:
                # remplacer break par quitter le programme
                break

    def display_player_menu(self):
        """Display the player menu and navigate it"""
        self.player_view.display_main_menu()
        menu_choice = self.player_view.navigate_main_menu()
        if menu_choice == "1":
            player_data = self.helper.load_file(PLAYER_DATA_PATH)
            if player_data:
                self.player_view.display_complete_list(player_data)
                self.exit_player_menu()
        elif menu_choice == "2":
            self.player_manager.new_player()
            self.exit_player_menu()
        elif menu_choice == "3":
            self.player_manager.search_player()
            self.exit_player_menu()
        elif menu_choice == "4":
            player_to_update = self.player_manager.select_player_to_update()
            if player_to_update:
                self.player_manager.update_player(player_to_update)
                self.exit_player_menu()
            else:
                self.player_view.player_not_in()
        else:
            self.display_main_menu()

    def exit_player_menu(self):
        """Return to main player menu or main menu."""
        exit_choice = self.player_view.exit_player_menu_prompt()
        if exit_choice == "1":
            self.display_player_menu()
        else:
            self.display_main_menu()

    def display_tournament_menu(self):
        """Display the tournament menu and navigate it"""
        self.tournament_view = TournamentMenu()
        tournoi_existant = self.tournament_view.tournoi_existant
        self.tournament_view.display_main_menu()
        menu_choice = self.tournament_view.navigate_main_menu()
        if menu_choice == "1":
            tournament_files_list = os.listdir(PAST_TOURNAMENT_PATH)
            chosen_file_index = self.tournament_view.display_past_list(
                tournament_files_list
            )
            if chosen_file_index:
                chosen_file_name = tournament_files_list[chosen_file_index - 1]
                file_path = PAST_TOURNAMENT_PATH + chosen_file_name
                tournament_to_display = self.helper.load_file(file_path)
                if tournament_to_display:
                    report_choice = self.tournament_view.choose_report_type()
                    if report_choice in ["1", "2", "3"]:
                        self.tournament_view.display_tournament_report(
                            tournament_to_display, report_choice
                        )
                    else:
                        self.tournament_view.display_main_menu()
                else:
                    self.tournament_view.display_main_menu()
        elif menu_choice == "2" and tournoi_existant:
            unfinished_tournament = self.loader.load_state()
            tournament = ReloadTounament(
                unfinished_tournament["tournament_players"],
                unfinished_tournament["tournament_infos"],
                unfinished_tournament["tournament_rounds"],
            ).recreate_tournament()
            PlayTournament(tournament).start_tournament()
        elif menu_choice == "2" and not tournoi_existant:
            tournament = CreateTournament()
        elif menu_choice == "3":
            confirm_erase = self.base_view.ask_y_n(
                "Confirmez-vous l'écrasement du tournoi en cours ?"
            )
            if confirm_erase == "y":
                unfinished_tournament = self.loader.load_state()
                tournament_to_erase = ReloadTounament(
                    unfinished_tournament["tournament_players"],
                    unfinished_tournament["tournament_infos"],
                    unfinished_tournament["tournament_rounds"],
                ).recreate_tournament()
                SaveData(tournament_to_erase).end_save()
                tournament = CreateTournament()
            else:
                self.tournament_view.display_main_menu()
        else:
            self.base_view.display_main_menu()
