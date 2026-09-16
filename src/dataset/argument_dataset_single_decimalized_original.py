from torch.autograd import Variable
from src.dataset.dataset import *


class ArgumentDatasetSingleDecimalizedOriginal(AbstractArgumentDataset):

    def __init__(self, path_word2vec, path_raw_dataset, train=True, split_percentage=0.7, batch_size=32):
        super(ArgumentDatasetSingleDecimalizedOriginal, self).__init__(path_word2vec, path_raw_dataset, train, split_percentage, batch_size)

    def _load_data(self, train, split_percentage):
        input_name_file = "{}/trace{}-{}.txt"

        if train:
            start = 0
            end = files_quantity * split_percentage
            print(end)
            label = "Loading training set:\t"

        else:
            start = files_quantity - 50 # * split_percentage FIXME
            end = files_quantity
            label = "Loading test set:\t"

        #x = numpy.zeros((int(end - start), 1, trace_size))
        #y = numpy.zeros((int(end - start), 1, quantity_activity))
        oracle_x = []
        x = numpy.zeros((int(end - start) * int(trace_size / window_size), 1, window_size))
        y = numpy.zeros((int(end - start) * int(trace_size / window_size), 1, quantity_activity))

        current_sample = 0
        #print(label)
        # print_progress_bar(current_sample, int(end - start) * int(trace_size/window_size), prefix=label)

        for index_file in range(int(start), int(end)):
            trace = open(input_name_file.format(self.path_raw_dataset, file_trace_size, index_file), "r")
            trace_lines = trace.readlines()

            collected = 0
            #current_x = numpy.zeros(trace_size)
            current_oracle_x = ""
            current_x = numpy.zeros(window_size)
            for i in range(1, trace_size + 1):
                tokens_trace = trace_lines[i].split()
                raw_event = tokens_trace[0]
                raw_activity = tokens_trace[2]

                current_oracle_x += f"{'' if len(current_oracle_x) == 0 else ','}{raw_event}"
                current_x[collected] = event_to_decimal(raw_event)
                collected += 1

                if collected == window_size:
                    oracle_x.append(current_oracle_x)
                    x[current_sample] = current_x.reshape(-1)
                    y[current_sample] = convert_raw_activity(raw_activity)
                    collected = 0
                    current_sample += 1

            # x[current_sample] = current_x.reshape(-1)
            # y[current_sample] = convert_raw_activity(raw_activity)
            # collected = 0
            # current_sample += 1
            # print_progress_bar(current_sample, int(end - start) * int(trace_size/window_size), prefix=label)

        return oracle_x, Variable(torch.Tensor(x)).to(device), Variable(torch.Tensor(y)).to(device)

    def check_admissibility(self, event, activity):
        e1 = ["A", "B", "I"]
        e2 = ["A", "B", "I", "N"]
        e3 = ["C"]
        e4 = ["A", "B", "E", "L", "N"]
        e5 = ["B", "F", "G", "L"]
        e6 = ["D"]
        e7 = ["E", "H", "L"]
        e8 = ["F", "G", "H", "M"]
        e9 = ["F", "G", "M"]
        e10 = ["F", "H", "M", "Q"]
        e11 = ["O", "Q"]
        e12 = ["O"]
        e13 = ["O", "Q"]
        e14 = ["O", "Q"]
        e15 = ["O", "P", "Q"]
        e16 = ["R"]
        if event == "e1" and (activity in e1 or any(item in activity for item in e1)) or \
                event == "e2" and (activity in e2 or any(item in activity for item in e2)) or \
                event == "e3" and (activity in e3 or any(item in activity for item in e3)) or \
                event == "e4" and (activity in e4 or any(item in activity for item in e4)) or \
                event == "e5" and (activity in e5 or any(item in activity for item in e5)) or \
                event == "e6" and (activity in e6 or any(item in activity for item in e6)) or \
                event == "e7" and (activity in e7 or any(item in activity for item in e7)) or \
                event == "e8" and (activity in e8 or any(item in activity for item in e8)) or \
                event == "e9" and (activity in e9 or any(item in activity for item in e9)) or \
                event == "e10" and (activity in e10 or any(item in activity for item in e10)) or \
                event == "e11" and (activity in e11 or any(item in activity for item in e11)) or \
                event == "e12" and (activity in e12 or any(item in activity for item in e12)) or \
                event == "e13" and (activity in e13 or any(item in activity for item in e13)) or \
                event == "e14" and (activity in e14 or any(item in activity for item in e14)) or \
                event == "e15" and (activity in e15 or any(item in activity for item in e15)) or \
                event == "e16" and (activity in e16 or any(item in activity for item in e16)):
            return True

        return False
