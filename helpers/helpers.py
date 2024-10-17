"""Helper functions"""

import json


class Helper:
    """Define static functions used in other parts of the program."""

    @staticmethod
    def load_file(filepath):
        """Load the given file."""
        with open(filepath, "r") as file:
            loaded_file = json.load(file)
        if loaded_file:
            return loaded_file
        else:
            print("Pas de fichier trouvé.")
            return None

    @staticmethod
    def save_file(filepath, data):
        """Save the given data in the given file."""
        with open(filepath, "w") as file:
            json.dump(data, file, indent=4)
