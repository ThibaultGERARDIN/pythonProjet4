"""Controllers to manage tournament related operations."""

import json
from models.tournament import Tournament
from models.matches import Match
from models.rounds import Round
from controllers.manage_players import ManagePlayers
from controllers.manage_data import SaveData
from controllers.manage_matches import MatchResult, MatchDraw
from views.player_menu import PlayerMenu
from views.tournament_menu import TournamentMenu
from views.base import View


class ReloadTounament:
    """Reacreate tournament from current tournament data."""

    def __init__(
        self,
        players_list,
        tournament_infos,
        tournament_rounds,
    ):
        """Initialize from data loaded from the saved files."""
        self.players_list = players_list
        self.infos = tournament_infos
        self.rounds = tournament_rounds
        self.manage_players = ManagePlayers()

    def get_players(self):
        """Create tournament players list."""
        tournament_players = self.manage_players.tournament_players(
            self.players_list
        )
        return tournament_players

    def recreate_match(self, list_of_matches):
        """Recreate matches from rounds data."""
        tournament_players = self.get_players()
        match_list = []
        for match in list_of_matches:
            player_1_INE = match[0][1]
            player_2_INE = match[1][1]
            player_1_score = match[0][2]
            player_2_score = match[1][2]
            for player in tournament_players:
                if player_1_INE == player.national_chess_id:
                    player_1 = player
                elif player_2_INE == player.national_chess_id:
                    player_2 = player
            player_1.score = player_1_score
            player_2.score = player_2_score
            match_in = Match(player_1, player_2)
            match_list.append(match_in)
        return match_list

    def recreate_tournament(self):
        """Recreate Tournament object from all the given data."""
        tournament_players = self.get_players()
        name = self.infos["name"]
        description = self.infos["description"]
        start_date = self.infos["start_date"]
        location = self.infos["location"]
        number_of_rounds = self.infos["number_of_rounds"]
        current_round = self.infos["current_round"]
        tournament = Tournament(
            name,
            location,
            tournament_players,
            description,
            number_of_rounds,
            current_round,
        )
        tournament.start_date = start_date
        for round in self.rounds:
            match_list = self.recreate_match(round["matches"])
            round_number = round["round_number"]
            round_start_time = round["start_time"]
            round_result = round["result"]
            round_end_time = round["end_time"]
            round_in = Round(match_list, round_number)
            round_in.start_time = round_start_time
            round_in.result = round_result
            round_in.end_time = round_end_time
            tournament.rounds.append(round_in)
        return tournament


class CreateTournament:
    """Create new tournament from input data."""

    def __init__(self):
        """Initialize the views and the data inputs."""
        self.base_view = View()
        self.player_menu = PlayerMenu()
        self.tournament_menu = TournamentMenu()
        self.manage_players = ManagePlayers()
        self.tournament_infos = self.tournament_menu.tournament_infos_prompt()
        self.tournament_players = self.select_players()

    def select_players(self):
        """
        Open player selection menu to prompt inputs.

        Select players from list or create new ones
        Check / update list of selected players
        Validate list of players to create Tournament.
        """
        tournament_players = []
        number_of_players = self.tournament_infos["number_of_rounds"] * 2
        while True:
            source_choice = self.player_menu.player_selection_prompt()
            if source_choice == "1":
                self.add_players_from_list(
                    tournament_players, number_of_players
                )
            elif source_choice == "2":
                new_player = self.manage_players.new_player()
                while not new_player:
                    new_player = self.manage_players.new_player()
                if len(tournament_players) < number_of_players:
                    tournament_players.append(new_player)
                    self.player_menu.player_added(new_player.name)
                else:
                    self.player_menu.too_many_players(
                        number_of_players, new_player.name
                    )
            elif source_choice == "3":
                self.player_menu.number_selected(
                    len(tournament_players), number_of_players
                )
                self.player_menu.display_choice_list(tournament_players)
            elif source_choice == "4":
                self.player_menu.display_choice_list(tournament_players)
                player_choice = self.player_menu.player_choice_remove_prompt(
                    tournament_players
                )
                if player_choice:
                    removed_player = tournament_players.pop(player_choice)
                    self.player_menu.display_removed_player(removed_player)
            elif source_choice == "5":
                self.validate_and_launch(tournament_players, number_of_players)
            else:
                break

    def add_players_from_list(self, tournament_players, number_of_players):
        """
        Select players to add to tournament from list

        Can select one or multiple players at once.
        """
        if len(tournament_players) < number_of_players:
            with open("./data/players.json", "r") as file:
                try:
                    players_list = json.load(file)
                except ValueError:
                    print("Erreur : liste de joueurs inexistante.")
                    pass
            self.player_menu.display_choice_list(players_list)
            selected_indexes = self.player_menu.player_choice_add_prompt()
            for index in selected_indexes:
                if index <= len(players_list):
                    player = players_list[index]
                    if player in tournament_players:
                        self.player_menu.player_already_in(player["name"])
                    else:
                        if len(tournament_players) < number_of_players:
                            tournament_players.append(player)
                            self.player_menu.player_added(player["name"])
                        else:
                            self.player_menu.too_many_players(
                                number_of_players, player["name"]
                            )
                else:
                    print(f"Choix {index} invalide.")
        else:
            self.player_menu.too_many_players(number_of_players)

    def validate_and_launch(self, tournament_players, number_of_players):
        """If list is full ask to validate and launch tournament."""
        self.player_menu.display_choice_list(tournament_players)
        if len(tournament_players) == number_of_players:
            validate = self.base_view.ask_y_n(
                "Validez-vous la liste ci-dessus pour"
                " la création du tournoi ?"
            )
            if validate == "y":
                self.tournament_players = (
                    self.manage_players.tournament_players(tournament_players)
                )
                tournament = Tournament(
                    self.tournament_infos["name"],
                    self.tournament_infos["location"],
                    self.tournament_players,
                    self.tournament_infos["description"],
                    self.tournament_infos["number_of_rounds"],
                )
                ask_start = self.base_view.ask_y_n(
                    "Tournoi créé ! Voulez-vous le lancer ?"
                )
                if ask_start == "y":
                    PlayTournament(tournament).start_tournament()
                else:
                    SaveData(tournament).save_state()
            else:
                print("Retour au choix des participants")
                self.player_menu.player_selection_prompt()
        else:
            self.player_menu.number_selected(
                len(tournament_players), number_of_players
            )


class PlayTournament:
    """Play a tournament."""

    def __init__(self, tournament):
        """
        Initialize with tournament object.

        Initialize the views needed.
        Create previous matches list from rounds.
        Initialize saver method.
        """
        self.view = TournamentMenu()
        self.base_view = View()
        self.tournament = tournament
        self.players = tournament.players
        self.previous_matches = []
        for round in tournament.rounds:
            for match in round.matches:
                self.previous_matches.append(match)
        self.saver = SaveData(tournament)
        self.match_draws = MatchDraw()

    def start_tournament(self):
        """Start (or restart) the tournament"""
        tournament = self.tournament
        self.saver.save_state()
        if (
            0 < tournament.current_round <= len(tournament.rounds)
            and tournament.rounds[tournament.current_round - 1].end_time
            == "Round en cours"
        ):
            unfinished_round = tournament.rounds[tournament.current_round - 1]
            self.view.display_unfinished_round_matches(unfinished_round)
            for i in range(len(unfinished_round.result), 4):
                match_result = MatchResult(
                    unfinished_round.matches[i], tournament
                )
                match_result.select_winner()
                match_result.add_score()
                unfinished_round.record_result(i, match_result.winner)
                self.saver.save_state()
            unfinished_round.finish_round()
            self.view.round_end(unfinished_round.round_name)
            self.saver.save_state()
        for i in range(tournament.current_round, tournament.number_of_rounds):
            tournament.current_round += 1
            self.saver.current_round = tournament.current_round
            match_list = self.match_draws.draw_matches(
                self.players, self.previous_matches
            )
            round = Round(match_list, i + 1)
            tournament.rounds.append(round)
            self.view.display_round_matches(round)
            match_index = 0
            for match in round.matches:
                match_index += 1
                match_result = MatchResult(match, tournament)
                match_result.select_winner()
                match_result.add_score()
                round.record_result(match_index, match_result.winner)
                self.saver.save_state()
            round.finish_round()
            self.saver.save_state()
            if tournament.current_round < tournament.number_of_rounds:
                next_round = self.base_view.ask_y_n(
                    f"{self.view.round_end(round.round_name)}"
                )
                if next_round == "n":
                    break
        if (tournament.current_round < tournament.number_of_rounds) or (
            tournament.rounds[tournament.current_round - 1].end_time
            == "Round en cours"
        ):
            self.saver.save_state()
            self.base_view.display_main_menu()
        else:
            tournament.finish_tournament()
            self.saver.end_save(tournament)
