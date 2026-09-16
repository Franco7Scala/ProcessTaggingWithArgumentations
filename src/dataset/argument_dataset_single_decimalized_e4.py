from src.dataset.argument_dataset_single_decimalized_original import ArgumentDatasetSingleDecimalizedOriginal


class ArgumentDatasetSingleDecimalizedE4(ArgumentDatasetSingleDecimalizedOriginal):

    def check_admissibility(self, event, activity):
        mapping = {
            "e1": ["A", "B"],
            "e2": ["D", "N"],
            "e3": ["C", "A", "O"],
            "e4": ["L", "B", "R"],
            "e5": ["F", "G", "Q"],
            "e6": ["D", "N", "P"],
            "e7": ["H", "R", "P"],
            "e8": ["E", "C", "O"],
            "e9": ["M", "D", "N"],
            "e10": ["I", "Q", "L"],
            "e11": ["G", "O", "Q"],
            "e12": ["L", "O", "M"],
            "e13": ["P", "Q", "H"],
            "e14": ["H", "E", "I"],
            "e15": ["P", "F", "G"],
            "e16": ["I", "R", "F"],
            "e17": ["A", "G", "R"],
            "e18": ["B", "H", "E"],
            "e19": ["C", "I", "D"],
            "e20": ["E", "L", "C"],
            "e21": ["M", "N", "B"],
            "e22": ["F", "M", "A"]
        }
        if event in mapping and (activity in mapping[event] or any(item in activity for item in mapping[event])):
            return True

        return False
