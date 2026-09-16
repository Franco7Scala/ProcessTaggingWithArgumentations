import torch
import numpy

from torch import nn
from src import dataset
from src.dataset.dataset import decimal_to_event


device = "cpu"


class Model(nn.Module):

    def __init__(self, input_size, out_features, w2v):
        super(Model, self).__init__()
        self.out_features = out_features
        self.num_layers = 32
        self.input_size = input_size
        self.hidden_size = 32
        self.out_features = out_features
        self.embedding_size = dataset.dataset.embedding_size
        self.w2v = w2v

        self.fc_0 = nn.Linear((dataset.dataset.window_size * dataset.dataset.embedding_size), 128)
        self.fc_0_0 = nn.Linear(128, 256)
        self.fc_1 = nn.Linear(256, 128)
        self.fc_2 = nn.Linear(128, 32)
        self.fc_3 = nn.Linear(32, out_features)

    def forward(self, x):
        x = torch.narrow(x, 2, x.shape[2] - dataset.dataset.window_size, dataset.dataset.window_size)
        input = numpy.zeros((x.shape[0], x.shape[1], int(x.shape[2] * dataset.dataset.embedding_size)))
        for i in range(x.shape[0]):
            current_sample = numpy.zeros((x.shape[2], dataset.dataset.embedding_size))
            for j in range(x.shape[2]):
                try:
                    current_sample[j] = self.w2v.wv[decimal_to_event(x[i][0][j].item())]

                except:
                    print(decimal_to_event(x[i][0][j].item()))

            input[i][0] = current_sample.reshape(-1)

        input = torch.from_numpy(input).type(torch.float32).to(device)
        output = self.fc_0(input)
        output = self.fc_0_0(torch.relu(output))
        output = self.fc_1(torch.relu(output))
        output = self.fc_2(torch.relu(output))
        output = self.fc_3(torch.relu(output))
        output = nn.functional.softmax(output, dim=2)
        return output
