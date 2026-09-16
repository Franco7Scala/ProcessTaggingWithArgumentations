import numpy
import torch
import time

from src import dataset, utility
from src.dataset.argument_dataset_single_decimalized_original import ArgumentDatasetSingleDecimalizedOriginal, decimal_to_activity, decimal_to_event, window_size
from src.main_production import call_oracle, conditioning, get_sorted_ownership
from src.model.neural_network import Model
from src.utility import print_progress_bar
from gensim.models import Word2Vec


paths = utility.get_paths(2)


def sequence_to_list(tensor):
    result = []
    for i in tensor.reshape(-1):
        result.append(decimal_to_event(i))

    return result


def elaborate_sequence_line(target_to_print, model_result, sequence_listed, oracle_input):
    result = ""
    sorted_activity, sorted_probability = get_sorted_ownership(model_result)
    #for i in range(len(sorted_activity)):

    current_sequence = ",".join(sequence_listed)
    # appending starting informations i/o
    result += sequence_listed[dataset.dataset.window_size - 1] + "; " #sequence_listed[dataset.dataset.trace_size - 1] + "; "
    result += oracle_input.replace(",", "-") + "; "
    result += target_to_print[0] + "; "
    # appending nn probabilities
    original_activities_with_probability = ""
    for a in range(len(sorted_activity[0])):
        original_activities_with_probability += "{}; {:.2f}; ".format(sorted_activity[0][a], sorted_probability[0][a] * 100)

    result += original_activities_with_probability

    try:
        # appending after filtering probabilities
        time_start = get_millis()
        oracle_result = call_oracle(oracle_input)
        time_oracle = get_millis() - time_start

        filtered_activity = [x for x in sorted_activity[0] if x in oracle_result]
        filtered_probability = conditioning(numpy.array(sorted_probability[0])[[x for x in range(len(sorted_activity[0])) if sorted_activity[0][x] in oracle_result]])
        activities_with_probability = ""
        for a in range(len(filtered_activity)):
            activities_with_probability += "{}; {:.2f}; ".format(filtered_activity[a], filtered_probability[a] * 100)

        result += activities_with_probability[:len(activities_with_probability) - 2] + "\n"


    except Exception as e:
        time_oracle = get_millis() - time_start
        result += "N/A\n"

    return result, time_oracle


def get_millis():
    return time.time_ns() / 1000000


if __name__ == "__main__":
    split_percentage = 0.60
    # building model
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = Model(1, 1, None)
    model = torch.load(paths["neural_network"]).to(device)
    model.w2v = Word2Vec.load(paths["word2vec"])
    model.eval()
    first = True
    max_length = dataset.dataset.trace_size + 1
    for current_trace_size in range(window_size, max_length):
        print("Working on trace size {} on {}".format(current_trace_size, max_length - 1))
        dataset.dataset.trace_size = current_trace_size
        # building dataset
        argument_test_set = ArgumentDatasetSingleDecimalizedOriginal(paths["word2vec"], paths["raw_dataset"], train=False, split_percentage=split_percentage, batch_size=1)
        val_loader = argument_test_set.get_dataloader()
        # writing result file
        with open(paths["statistics_file"], "a") as statistics_file:
            with open(paths["times_file"], "a") as times_file:
                index = 0
                if first:
                    statistics_file.write("seq_len; event; current sequence; related activity; (activities with related probabilities according to the nn);;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;; (activities with related probabilities conditioned);\n")
                    times_file.write("seq_len; nn; admissibility; tool\n")
                    first = False

                for datapoint in val_loader:
                    times = ""
                    print_progress_bar(index, len(val_loader), prefix="Building file:\t\t")
                    input = datapoint['x'].squeeze(2)
                    oracle_input = datapoint['oracle_x'][0]
                    target = torch.reshape(datapoint['y'], (datapoint['y'].shape[1], datapoint['y'].shape[2]))
                    target_argmaxed = torch.argmax(target, dim=1)
                    target_to_print = []
                    for i in target_argmaxed:
                        target_to_print.append(decimal_to_activity(i))

                    time_start = get_millis()
                    prediction = model(input)
                    time_nn = get_millis() - time_start

                    prediction = prediction.squeeze(1)

                    sequence_statistics, time_oracle = elaborate_sequence_line(target_to_print, prediction, sequence_to_list(input), oracle_input)
                    stringed_event = decimal_to_event(input[0][0][dataset.dataset.window_size - 1].item())
                    time_start = get_millis()
                    stringed_activity = decimal_to_activity(torch.argmax(prediction).item())
                    argument_test_set.check_admissibility(stringed_event, stringed_activity)
                    time_admissibility = get_millis() - time_start

                    statistics_file.write("{}; {}".format(oracle_input.count(",") + 1, sequence_statistics))
                    times_file.write("{};{};{};{}\n".format(oracle_input.count(",") + 1, time_nn, time_admissibility, time_oracle))
                    index += 1

            print_progress_bar(len(val_loader), len(val_loader), prefix="Building file:\t\t")

        break
