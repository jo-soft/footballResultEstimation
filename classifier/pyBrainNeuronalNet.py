from pybrain.supervised import BackpropTrainer
from pybrain.tools.shortcuts import buildNetwork
from scipy.misc import comb


def calculate_hidden_layers(layer_number, in_dim, max_goals):
    # number of possible results with max ``max_goals`` goals per team
    num_of_categories = comb(max_goals, 2, exact=True)
    return int(2 * (in_dim + num_of_categories) / 3) + 1


class NeuronalNetworkClassifier(object):

    def __init__(self, training_data):
        """

        :param training_data:
        :param max_goals: max goals shoot
        """
        self.training_data = training_data
        layers_tuple = (self.training_data.indim,
                        calculate_hidden_layers(1, self.training_data.indim, training_data.max_goals),
                        2)
        self.net = buildNetwork(
            *layers_tuple
        )

    def train(self, epochs=None):
        trainer = BackpropTrainer(
            self.net,
            self.training_data
        )
        if epochs:
            trainer.trainEpochs(epochs)
        else:
            trainer.trainUntilConvergence()

    def activate(self, vector, raw=False):
        raw_result = self.net.activate(vector)
        if raw:
            return raw_result

        def get_goals(raw_num_goals):
            raw_num_goals = max(0, raw_num_goals)
            return int(
                round(raw_num_goals)
            )

        return tuple(get_goals(raw_num_goals) for raw_num_goals in raw_result)