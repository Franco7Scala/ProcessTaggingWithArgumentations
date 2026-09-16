import csv

from src import utility
from src.dataset.argument_dataset_single_decimalized_original import ArgumentDatasetSingleDecimalizedOriginal
from src.dataset.argument_dataset_single_decimalized_e2 import ArgumentDatasetSingleDecimalizedE2
from src.dataset.argument_dataset_single_decimalized_e3 import ArgumentDatasetSingleDecimalizedE3
from src.dataset.argument_dataset_single_decimalized_e4 import ArgumentDatasetSingleDecimalizedE4
from src.dataset.argument_dataset_single_decimalized_e42 import ArgumentDatasetSingleDecimalizedE42


dataset_number = 2  # 2 3 4 42


paths = utility.get_paths(dataset_number)
path_csv_source_file = paths["statistics_file"]
path_csv_destination_file = paths["statistics_file_admissibility"]
dataset_name = f"e{dataset_number}"

if __name__ == "__main__":
    if dataset_name == "original":
        dataset = ArgumentDatasetSingleDecimalizedOriginal(paths["word2vec"], paths["raw_dataset"])

    elif dataset_name == "e2":
        dataset = ArgumentDatasetSingleDecimalizedE2(paths["word2vec"], paths["raw_dataset"])

    elif dataset_name == "e3":
        dataset = ArgumentDatasetSingleDecimalizedE3(paths["word2vec"], paths["raw_dataset"])

    elif dataset_name == "e4":
        dataset = ArgumentDatasetSingleDecimalizedE4(paths["word2vec"], paths["raw_dataset"])

    elif dataset_name == "e42":
        dataset = ArgumentDatasetSingleDecimalizedE42(paths["word2vec"], paths["raw_dataset"])

    with open(path_csv_source_file) as input_file:
        csv_reader = csv.reader(input_file, delimiter=";")
        with open(path_csv_destination_file, "w") as destination_file:
            first_line = True
            for row in csv_reader:
                if first_line:
                    first_line = False
                    new_line = ""
                    #new_line = "seq len; event; index event; related activity; (activities with related probabilities according to the nn);;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;"

                else:
                    new_line = "{}; {}; {}; {}; ".format(row[0], row[1], row[2], row[3])
                    for i in range(4, 38, 2):
                        activity = row[2].split("-")[-1]  #row[1].strip()
                        if dataset.check_admissibility(activity, row[i].strip()):
                            if "N/A" in row[i]:
                                pass
                                #new_line += "{}; {}; ".format(row[i], 100)

                            else:
                                new_line += "{}; {}; ".format(row[i], row[i + 1])

                new_line += "\n"
                destination_file.write(new_line)

    print("Done!")
