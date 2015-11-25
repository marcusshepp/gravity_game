import os, pickle

class NeuralNetwork(object):

    """
    Hold all layers together and propogate values through the net.
    """

    def __init__(self, data=None, pickled=False):
        """
        Hold data ie weights thresholds and input.
        also holds neurons for each layer
        """
        if pickled:
            with open("net_output/foo.pickle", "rb") as pickled_data:
                data = pickle.load(pickled_data)
                self.data = data
        else: self.data = data
        # create layers
        self.input_layer = data["num_input_nodes"]
        self.hidden_layer = data["num_hidden_nodes"]
        self.output_layer = data["num_output_nodes"]
        # inputs
        self.inputs = data["inputs"]
        # weights
        self.first_weights = data["first_weights"]
        self.second_weights = data["second_weights"]
        self.third_weights = data["third_weights"]
        # thresholds
        self.first_thresholds = data["first_thresholds"]
        self.second_thresholds = data["second_thresholds"]
        self.third_thresholds = data["third_thresholds"]

    def __neural_output(self, weights, inputs, threshold):
        """
        in: weights, inputs, threshold
        out: 1 or 0

        if the (sum of weights) x (sum of inputs)
        is greater than my threshold
        output 1
        else 0
        """
        length = len(inputs)
        activation = 0
        output = 0
        for i in range(length):
            activation += weights[i] * inputs[i]
        if activation > threshold:
            output = 1
        return output

    def __layer_out(self, weights, inputs, thresholds):
        """
        for all input & weights, compute each output from each neuron.
        """
        outs = []
        # number of thresholds = number of output bits
        for threshold in thresholds:
            outs.append(
                self.__neural_output(weights,
                                     inputs,
                                     threshold))
        return outs

    def one_out(self):
        """
        return bits for input layer.
        """
        return self.__layer_out(self.first_weights,
                              self.inputs,
                              self.first_thresholds)

    def hidden_layer_out(self):
        """
        return bits for hidden layer.
        """
        return self.__layer_out(self.second_weights,
                              self.one_out(),
                              self.second_thresholds)

    def output_layer_out(self):
        """
        return bits for ouput layer.
        """
        return self.__layer_out(self.third_weights,
                              self.hidden_layer_out(),
                              self.third_thresholds)

    def out(self):
        """
        for show
        """
        return self.output_layer_out()

    def pickle_data(self, name):
        name = name + ".pickle"
        path = os.path.join("net_output", name)
        with open(path, "wb") as net_output_pickle:
            pickle.dump(self.data, net_output_pickle)
