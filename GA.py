"""
# Genetic Algorithm
#
for each chrome do

    decode chrome

    create new nn

    run nn

    decode output

    compare output to desired output

    assign fitness

    select part

    cross

    mutate

create new pop
#
"""
import random as r

import net
import data_helpers
import biological_model

class GeneticTrainer:
    """
    trains an ann to play a simple game.
    """

    def __init__(self, pop_size=0):
        if pop_size != 0:
            self.pop_size = pop_size
        else: self.pop_size = 15
        self.population = list() # weights and thresh's for ann
        self.decoded_population = list() # (x, y) pair corrdinates for game
        self.current_index = -1
        self.current_board = str()
        self.last_generation = dict()
        self.begin = True

    def init_population(self):
        for _ in range(self.pop_size):
            chrome = []
            # size of chrome
            # total number of weights and thresholds
            for i in range(869):
                chrome.append(r.randrange(-255, 255))
            self.population.append(chrome)

    def decode(self, chrome):
        """
        Weights from input to layer one: 621
        Weights from layer one to layer two: 45
        Weights from layer two to layer three: 100
        total weights: 766
        94 thresholds are needed.
        total:  869

        (621, 45, 100, 9, 5, 20)
        """
        synapsus0 = chrome[:621]
        synapsus1 = chrome[621:621+45]
        synapsus2 = chrome[621+45:621+45+100]
        thresholds0 = chrome[621+45+100:621+45+100+9]
        thresholds1 = chrome[621+45+100+9:621+45+100+9+5]
        thresholds2 = chrome[621+45+100+9+5:621+45+100+9+5+20]
        return synapsus0, synapsus1, synapsus2, thresholds0, thresholds1, thresholds2

    def nn_data(self, chrome):
        """
        put the data into a dict in order to easily create a nn object.
        in: chromosome, path to current_board
        out: data that my ann can be created with
        """
        decoded_chrome = self.decode(chrome)
        data = dict()
        data["num_input_nodes"] = 9
        data["num_hidden_nodes"] = 5
        data["num_output_nodes"] = 20
        data["inputs"] = data_helpers.get_data(self.current_board)
        data["first_weights"] = decoded_chrome[0]
        data["second_weights"] = decoded_chrome[1]
        data["third_weights"] = decoded_chrome[2]
        data["first_thresholds"] = decoded_chrome[3]
        data["second_thresholds"] = decoded_chrome[4]
        data["third_thresholds"] = decoded_chrome[5]
        return data

    def decode_network_output(self, out):
        """
        in: binary string, ie output for the 20 output nodes from ANN.
        out: x, y corrdinates
        """
        return [int("".join([str(i) for i in out[:10]]), 2),
                int("".join([str(i) for i in out[10:]]), 2)]
    
    def advance(self):
        """
        Advances the current index.
        """
        if self.current_index < (len(self.decoded_population) - 1):
            self.current_index += 1
    
    def next_move(self):
        """
        Gives the current move.
        """
        return self.decoded_population[self.current_index]
    
    def set_board(self, path_to_board):
        """
        Gives the object the path to the current board data being played.
        """
        self.current_board = path_to_board
        
    def generate_moves(self):
        """
        Given the current board creates a decoded population
        of moves to be used tested in the game.
        """
        if self.begin:
            self.init_population()
            self.begin = False
        self.decoded_population = list()
        for chromosome in self.population:
            # print(chromosome)
            network_info = self.nn_data(chromosome)
            # print(network_info)
            artificial_neural_network = net.NeuralNetwork(network_info)
            x, y = self.decode_network_output(artificial_neural_network.out())
            self.decoded_population.append((x, y))
        print(self.decoded_population)
    
    
    
