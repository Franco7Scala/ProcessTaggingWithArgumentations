from src.dataset.argument_dataset_single_decimalized_original import ArgumentDatasetSingleDecimalizedOriginal


class ArgumentDatasetSingleDecimalizedE2(ArgumentDatasetSingleDecimalizedOriginal):

    def check_admissibility(self, event, activity):
        mapping = {
            "e1": ["A", "B"],
            "e2": ["D", "N"],
            "e3": ["C"],
            "e4": ["L"],
            "e5": ["F", "G"],
            "e6": ["D", "N"],
            "e7": ["H", "R"],
            "e8": ["E"],
            "e9": ["M"],
            "e10": ["I", "Q"],
            "e11": ["G", "O"],
            "e12": ["L", "O"],
            "e13": ["P", "Q"],
            "e14": ["H"],
            "e15": ["P"],
            "e16": ["I", "R"],
            "e17": ["A"],
            "e18": ["B"],
            "e19": ["C"],
            "e20": ["E"],
            "e21": ["M"],
            "e22": ["F"]
        }
        if event in mapping and (activity in mapping[event] or any(item in activity for item in mapping[event])):
            return True

        return False
