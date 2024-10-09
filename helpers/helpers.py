"""Helper functions"""

import json


class Helper:

    @staticmethod
    def load_file(filepath):
        with open(filepath, "r") as file:
            loaded_file = json.load(file)
        return loaded_file

    @staticmethod
    def save_file(filepath, data):
        with open(filepath, "w") as file:
            json.dump(data, file, indent=4)
