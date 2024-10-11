import json
import os
from models.tournament import Tournament
from controllers.base import Controller
from controllers.manage_data import (
    LoadData,
    CURRENT_TOURNAMENT_PATH,
)
from controllers.manage_players import ManagePlayers
from controllers.manage_tournaments import ReloadTounament, CreateTournament
from views.base import View

controller = Controller()

controller.display_main_menu()
