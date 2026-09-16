import torch

from src import dataset
from src.dataset.argument_dataset_single_decimalized_original import ArgumentDatasetSingleDecimalizedOriginal, decimal_to_activity, decimal_to_event, window_size
from src.main_production import call_oracle
from src.utility import print_progress_bar

n_dataset = 2

path_neural_network = f"/Users/francesco/Desktop/Argumentation/models/neural_network_ep50_typesingle_cpu_dataset_e{n_dataset}.nn"
path_word2vec = f"/Users/francesco/Desktop/Argumentation/models/word2vec_e{n_dataset}.model"
path_activities = f"/Users/francesco/Desktop/Argumentation/buildjar/support/activitiesForLog_{n_dataset}.txt"
path_events = f"/Users/francesco/Desktop/Argumentation/buildjar/support/eventsForLog_{n_dataset}.txt"
path_raw_dataset = f"/Users/francesco/Desktop/Argumentation/Datasets/e{n_dataset}"

path_processes = "/Users/francesco/Desktop/Argumentation/buildjar/support/processForLog.txt"
path_jar_tool = "/Users/francesco/Desktop/Argumentation/Argumentation.jar"
path_canen_tool = "/Users/francesco/Desktop/Argumentation/Canen"
path_support_folder = "/Users/francesco/Desktop/Argumentation/Tmp"
path_statistics_file = f"/Users/francesco/Desktop/Argumentation/results_hard_admissibility_dataset_{n_dataset}.csv"


def sequence_to_list(tensor):
    result = []
    for i in tensor.reshape(-1):
        result.append(decimal_to_event(i))

    return result


def elaborate_sequence_line(target_to_print, sequence_listed):
    result = ""
    current_sequence = ",".join(sequence_listed)
    # appending starting informations i/o
    result += sequence_listed[dataset.trace_size - 1] + "; "
    result += current_sequence.replace(",", "-") + "; "
    result += target_to_print[0] + "; "

    try:
        # appending after filtering probabilities
        oracle_result = call_oracle(current_sequence)
        filtered_activity = list(dict.fromkeys([x for x in oracle_result]))

        for a in range(len(filtered_activity)):
            result += "{}; ".format(filtered_activity[a])

    except:
        result += "N/A\n"

    return result


if __name__ == "__main__":
    split_percentage = 0.0
    # building model
    first = True
    max_length = 6
    for current_trace_size in range(window_size, max_length):
        print("Working on trace size {} on {}".format(current_trace_size, max_length - 1))
        dataset.trace_size = current_trace_size
        # building dataset
        argument_test_set = ArgumentDatasetSingleDecimalizedOriginal(path_word2vec, path_raw_dataset, train=False, split_percentage=split_percentage, batch_size=1)
        val_loader = argument_test_set.get_dataloader()
        # writing result file
        with open(path_statistics_file, "a") as statistics_file:
            index = 0
            if first:
                statistics_file.write("seq_len; event; current sequence; ground truth; (admissible activities);;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;\n")
                first = False

            for datapoint in val_loader:
                print_progress_bar(index, len(val_loader), prefix="Building file:\t\t")
                input = datapoint['x'].squeeze(2)
                target = torch.reshape(datapoint['y'], (datapoint['y'].shape[1], datapoint['y'].shape[2]))
                target_argmaxed = torch.argmax(target, dim=1)
                target_to_print = []
                for i in target_argmaxed:
                    target_to_print.append(decimal_to_activity(i))

                sequence_statistics = elaborate_sequence_line(target_to_print, sequence_to_list(input))
                statistics_file.write("{}; {}\n".format(dataset.trace_size, sequence_statistics))
                index += 1

            print_progress_bar(len(val_loader), len(val_loader), prefix="Building file:\t\t")
