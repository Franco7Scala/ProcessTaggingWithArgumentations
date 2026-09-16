from src.dataset.argument_dataset_single_decimalized_original import ArgumentDatasetSingleDecimalizedOriginal


class ArgumentDatasetSingleDecimalizedE3(ArgumentDatasetSingleDecimalizedOriginal):

    def check_admissibility(self, event, activity):
        mapping = {
            "e1": ["A", "B"],
            "e2": ["D", "N"],
            "e3": ["C", "A", "O"],
            "e4": ["L", "B"],
            "e5": ["F", "G"],
            "e6": ["D", "N"],
            "e7": ["H", "R", "P"],
            "e8": ["E", "C"],
            "e9": ["M", "D"],
            "e10": ["I", "Q"],
            "e11": ["G", "O", "Q"],
            "e12": ["L", "O"],
            "e13": ["P", "Q"],
            "e14": ["H", "E"],
            "e15": ["P", "F"],
            "e16": ["I", "R"],
            "e17": ["A", "G", "R"],
            "e18": ["B", "H"],
            "e19": ["C", "I"],
            "e20": ["E", "L"],
            "e21": ["M", "N"],
            "e22": ["F", "M"]
        }
        if event in mapping and (activity in mapping[event] or any(item in activity for item in mapping[event])):
            return True

        return False
