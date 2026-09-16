import numpy
import torch
import warnings

from subprocess import Popen, PIPE, STDOUT
from gensim.models import Word2Vec
from src import dataset, utility
from src.dataset.dataset import event_to_decimal, decimal_to_activity
from src.model.neural_network import Model


paths = utility.get_paths(2)


warnings.filterwarnings("ignore")


def read_sequence():
    sequence_to_tensor = []
    sequence_to_list = []
    print("ATTENTION: put at least 5 events!")
    while True:
        current_event = input("Insert the event name or END (or e) to complete:\n")
        if current_event.casefold() == "END".casefold() or current_event.casefold() == "e".casefold():
            if len(sequence_to_tensor) < dataset.window_size:
                print("ATTENTION: put at least 5 events!")

            else:
                print("Given sequence: {}".format(sequence_to_list))
                break

        else:
            sequence_to_tensor.append(event_to_decimal(current_event))
            sequence_to_list.append(current_event)

    plain_x = numpy.zeros((int(len(sequence_to_tensor) - dataset.window_size + 1), dataset.window_size))
    listed_x = []
    k = 0
    for i in range(len(sequence_to_tensor) - dataset.window_size + 1):
        current_x = numpy.zeros(dataset.window_size)
        current_s = []
        for j in range(dataset.window_size):
            current_x[j] = sequence_to_tensor[i + j]
            current_s.append(sequence_to_list[i + j])

        plain_x[k] = current_x.reshape(-1)
        k += 1
        listed_x.append(current_s)

    return torch.Tensor(plain_x).reshape(k, 1, dataset.window_size), listed_x


def call_oracle(sequence):
    process = Popen(["java", "-jar", paths["jar_tool"], paths["activities"], paths["events"], paths["processes"], paths["canen_tool"], paths["support_folder"], sequence], stdout=PIPE, stderr=STDOUT)
    predictions = []

    for line in process.stdout:
        predictions.append(line.decode("utf-8").split("-")[2])

    return predictions


def conditioning(x):
    return x / numpy.sum(x)


def get_sorted_ownership(tensored_data):
    activity = []
    probability = []
    for _, x in enumerate(tensored_data.detach().numpy()):
        sorted = (-x).argsort()[:tensored_data.shape[1]]
        current_activity = []
        current_probability = []
        for i in range(len(sorted)):
            current_activity.append(decimal_to_activity(sorted[i]))
            current_probability.append(x[sorted[i]])

        activity.append(current_activity)
        probability.append(current_probability)

    return activity, probability


if __name__ == "__main__":
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = Model(1, 1, None)
    model = torch.load(paths["neural_network"]).to(device)
    model.w2v = Word2Vec.load(paths["word2vec"])
    model.eval()
    sequence_tensored, sequence_listed = read_sequence()
    model_result = model(sequence_tensored)

    for j in range(len(sequence_listed)):
        sorted_activity, sorted_probability = get_sorted_ownership(model_result[j])
        for i in range(len(sorted_activity)):
            current_sequence = ",".join(sequence_listed[j])
            try:
                oracle_result = call_oracle(current_sequence)
                filtered_activity = [x for x in sorted_activity[i] if x in oracle_result]
                filtered_probability = conditioning(numpy.array(sorted_probability[i])[[x for x in range(len(sorted_activity[i])) if sorted_activity[i][x] in oracle_result]])
                activities_with_probability = ""
                for a in range(len(filtered_activity)):
                    activities_with_probability += "{}({:.2f}%), ".format(filtered_activity[a], filtered_probability[a] * 100)

                activities_with_probability = activities_with_probability[:len(activities_with_probability) - 2]
                print("The event {} in position {} of the sequence can hurt the following activities (with related probability): {}".format(sequence_listed[j][dataset.window_size - 1], dataset.window_size + j, activities_with_probability))
                # print for detailed statistics
                original_activities_with_probability = ""
                for a in range(len(sorted_activity[i])):
                    original_activities_with_probability += "{}({:.2f}%), ".format(sorted_activity[i][a], sorted_probability[i][a] * 100)

                original_activities_with_probability = original_activities_with_probability[:len(original_activities_with_probability) - 2]
                print("\tAre removed {} selections".format(len(sorted_activity[i]) - len(filtered_activity)))
                print("\tThe event {} in position {} of the sequence according to the nn can hurt the following activities (with related probability): {}".format(sequence_listed[j][dataset.window_size - 1], dataset.window_size + j, original_activities_with_probability))

            except:
                print("The event {} in position {} of the sequence can't hurt activities".format(sequence_listed[j][dataset.window_size - 1], i))
