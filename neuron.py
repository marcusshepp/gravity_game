class Neuron(object):

    def __init__(self, set_of_input_weights, set_of_inputs, threshold):
        self.threshold = threshold
        self.set_of_input_weights = set_of_input_weights
        self.set_of_inputs = set_of_inputs
        self.num_of_inputs = len(self.set_of_inputs)

    def output(self):
        length = self.num_of_inputs
        activation = 0
        output = 0
        for i in range(length):
            activation += self.set_of_input_weights[i] * self.set_of_inputs[i]
        if activation > self.threshold:
            output = 1
        return output
