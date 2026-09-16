import torch
import numpy

from torch.utils.data import Dataset, DataLoader
from gensim.models import Word2Vec

trace_size = 40     # dynamic in test
file_trace_size = 41
files_quantity = 10000
quantity_activity = 16
quantity_events = 22
embedding_size = 4
window_size = 5
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


class AbstractArgumentDataset(Dataset):

    def __init__(self, path_word2vec, path_raw_dataset, train=True, split_percentage=0.7, batch_size=32):
        self.batch_size = batch_size
        self.path_raw_dataset = path_raw_dataset
        words = self.build_words_vector()
        self.w2v = Word2Vec(words, min_count=1, vector_size = embedding_size)
        #self.w2v.save(path_word2vec)
        self.oracle_x, self.x, self.y = self._load_data(train, split_percentage)

    def __getitem__(self, index):
        return {"x": self.x[index], "y": self.y[index], "oracle_x": self.oracle_x[index]}

    def __len__(self):
        return len(self.x)

    def get_dataloader(self):
        return DataLoader(self, batch_size=self.batch_size)

    def _load_data(self, train, split_percentage):
        pass

    def check_admissibility(self, event, activity):
        pass

    def build_words_vector(self):
        input_name_file = "{}/trace{}-{}.txt"
        result = []
        for index_file in range(files_quantity):
            trace = open(input_name_file.format(self.path_raw_dataset, file_trace_size, index_file), "r")
            trace_lines = trace.readlines()

            for i in range(1, trace_size + 1):
                tokens_trace = trace_lines[i].split()
                raw_event = tokens_trace[0]
                raw_activity = tokens_trace[2]
                result.append([raw_event, raw_activity])

        return result

def convert_raw_event(raw_event):
    decimal_event = event_to_decimal(raw_event)
    return to_categorical(decimal_event, num_classes=quantity_events)

def convert_raw_activity(raw_activity):
    decimal_activity = activity_to_decimal(raw_activity)
    return to_categorical(decimal_activity, num_classes=quantity_activity)

def convert_raw_event_activity(raw_event, raw_activity):
    decimal_event = event_to_decimal(raw_event)
    decimal_activity = activity_to_decimal(raw_activity)
    event = to_categorical(decimal_event, num_classes=quantity_events)
    activity = to_categorical(decimal_activity, num_classes=quantity_activity)
    return numpy.stack((event, activity), axis=0)

def event_to_decimal(raw_event):
    return int(raw_event[1:]) - 1

def decimal_to_event(event):
    return "e{}".format(int(event + 1))

def activity_to_decimal(raw_activity):
    if raw_activity == "A":
        return 0
    elif raw_activity == "B":
        return 1
    elif raw_activity == "C":
        return 2
    elif raw_activity == "D":
        return 3
    elif raw_activity == "E":
        return 4
    elif raw_activity == "F":
        return 5
    elif raw_activity == "G":
        return 6
    elif raw_activity == "H":
        return 7
    elif raw_activity == "I":
        return 8
    elif raw_activity == "L":
        return 9
    elif raw_activity == "M":
        return 10
    elif raw_activity == "N":
        return 11
    elif raw_activity == "O":
        return 12
    elif raw_activity == "P":
        return 13
    elif raw_activity == "Q":
        return 14
    elif raw_activity == "R":
        return 15

    raise Exception("Unknown Activity!")

def decimal_to_activity(activity):
    if activity == 0:
        return "A"
    elif activity == 1:
        return "B"
    elif activity == 2:
        return "C"
    elif activity == 3:
        return "D"
    elif activity == 4:
        return "E"
    elif activity == 5:
        return "F"
    elif activity == 6:
        return "G"
    elif activity == 7:
        return "H"
    elif activity == 8:
        return "I"
    elif activity == 9:
        return "L"
    elif activity == 10:
        return "M"
    elif activity == 11:
        return "N"
    elif activity == 12:
        return "O"
    elif activity == 13:
        return "P"
    elif activity == 14:
        return "Q"
    elif activity == 15:
        return "R"

    raise Exception("Unknown Activity!")

def to_categorical(y, num_classes):
    return numpy.eye(num_classes, dtype='uint8')[y]
