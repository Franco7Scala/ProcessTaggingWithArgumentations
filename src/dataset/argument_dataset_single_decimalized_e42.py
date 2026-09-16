from src.dataset.argument_dataset_single_decimalized_original import ArgumentDatasetSingleDecimalizedOriginal


class ArgumentDatasetSingleDecimalizedE42(ArgumentDatasetSingleDecimalizedOriginal):

    def check_admissibility(self, event, activity):
        mapping = {
            "e1": {"A", "B", "F", "Q"},
            "e2": {"A", "B", "D", "E"},
            "e3": {"A", "B", "C", "L"},
            "e4": {"A", "E", "F", "L"},
            "e5": {"C", "D", "F", "G"},
            "e6": {"D", "F", "I", "N"},
            "e7": {"B", "C", "E", "H"},
            "e8": {"D", "E", "I", "N"},
            "e9": {"C", "M", "P", "R"},
            "e10": {"I", "M", "Q", "R"},
            "e11": {"G", "M", "N", "O"},
            "e12": {"L", "O", "Q"},
            "e13": {"G", "O", "P", "Q"},
            "e14": {"H", "N", "O", "R"},
            "e15": {"H", "L", "M", "P"},
            "e16": {"H", "I", "P", "R"},
        }
        if event in mapping and (activity in mapping[event] or any(item in activity for item in mapping[event])):
            return True

        return False
