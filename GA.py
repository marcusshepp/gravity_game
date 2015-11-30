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
import datetime

import net
import data_helpers
import biological_model as bm

class GeneticTrainer:
    """
    trains an ann to play a simple game.
    """

    def __init__(self, pop_size=15, generation_flag=100):
        self.population = list() # weights and thresh's for ann
        self.decoded_population = list() # (x, y) pair corrdinates for game
        self.fitness_scores = list()
        self.current_board = str()
        self.last_generation = dict()
        self.generations = 0 # number of times a new populous has been created
        self.current_index = -1
        self.begin = True
        self.generation_flag = generation_flag
        self.pop_size = pop_size

    def init_population(self):
        for _ in range(self.pop_size):
            chrome = []
            # size of chrome
            # total number of weights and thresholds
            for i in range(869):
                chrome.append(r.randrange(-255, 255))
            self.population.append(chrome)

    @property
    def size_of_population(self):
        return self.pop_size

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
        return [int("".join([str(i) for i in out[:10]]), 2), int("".join([str(i) for i in out[10:]]), 2)]

    def advance(self):
        """
        Advances the current index.
        """
        if self.current_index < (len(self.decoded_population) - 1):
            self.current_index += 1

    def clear(self):
        self.current_index = -1

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
        self.clear()

    def set_deaths(self, deaths):
        """
        Entry point to submit the results from the last population
        of moves.
        """
        self.last_generation["deaths"] = list()
        for death in deaths:
            self.last_generation["deaths"].append(death)

    def generate_fitness_scores(self):
        """
        Create Fitness Scores for the current population of
        Artificial Neural Network data.
        Takes the death point and finds the distance between that point
        and desired_destination.
        Then takes 1000 - absolute value of that distance.
        """
        desired_destination = (700,300) # map 1
        self.fitness_scores = list()
        for resulting_destination in self.last_generation["deaths"]:
            print("resulting_destination: ", resulting_destination)
            dist = data_helpers.distance(resulting_destination, desired_destination)
            print("distance: ", dist)
            fitness = 1000-abs(int(dist))
            print("fitness: ", fitness)
            self.fitness_scores.append(fitness)

    def create_new_population(self):
        """
        Uses the Biological Model to mimic genetic chromosome
        mutation and crossover.
        """
        self.check_for_generation_cap()
        pop_container = list()
        for chromosome in self.population:
            partner = bm.select_partner(
                self.fitness_scores, self.population)
            child = bm.mutate(bm.crossover(chromosome, partner))
            pop_container.append(child)
        if self.population == pop_container:
            print("newly created populous is the same as the old populous")
        self.population = pop_container
        print("generations: ", self.generations)
        self.generations += 1

    def evaluate(self):
        self.generate_fitness_scores()
        self.create_new_population()

    def check_for_generation_cap(self):
        if self.generations % self.generation_flag == 0:
            print(self.fitness_scores)
            best_chromosome = max(self.fitness_scores)
            index = [i for i, v in enumerate(self.fitness_scores) if v == best_chromosome][0]
            data = self.nn_data(self.population[index])
            ann = net.NeuralNetwork(data)
            today = str(datetime.datetime.now())
            ann.pickle_data(today)
            print("Generation cap met\nPickled Network object to file.")

    def reset(self, deaths, path_to_board):
        self.set_deaths(deaths)
        self.evaluate()
        self.set_board(path_to_board)
        self.generate_moves()
