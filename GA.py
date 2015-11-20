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


class GeneticTrainer(object):
    """
    trains an ann to play a simple game.
    """

    def __init__(self, pop_size=0):
        if pop_size != 0:
            self.pop_size = pop_size
        else: self.pop_size = 5
        self.population = [] # weights and thresh's for ann
        self.pop_index = 0
        self.last_population = dict()
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

    def nn_data(self, chrome, path):
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
        data["inputs"] = data_helpers.get_data(path)
        data["first_weights"] = decoded_chrome[0]
        data["second_weights"] = decoded_chrome[1]
        data["third_weights"] = decoded_chrome[2]
        data["first_thresholds"] = decoded_chrome[3]
        data["second_thresholds"] = decoded_chrome[4]
        data["third_thresholds"] = decoded_chrome[5]
        return data

    def decode_output(self, out):
        """
        in: binary string
        out: x, y corrdinates
        """
        return [int("".join([str(i) for i in out[:10]]), 2), int("".join([str(i) for i in out[10:]]), 2)]

    def create_trys(self, current_board):
        """
        in: current_board
        out: net generated guesses
        """
        if self.begin:
            """
            if its the first time accessing a population of guesses
            call the initial function to create said population.
            """
            self.init_population()
            population = self.population
            self.begin = False
        else:
            population = self.population
        self.last_population["trys"] = []
        for chrome in population:
            """
            create a net based on the current chromosome
            appends to the trys list in self
            """
            data_for_network = self.nn_data(chrome, current_board)
            ann = net.NeuralNetwork(data_for_network)
            x, y = self.decode_output(ann.out())
            self.last_population["trys"].append((x, y))
        return self.last_population["trys"]

    def evaluate(self):
        """

        """
        desired_destination = (0, 0)
        fits = []
        for decision in self.last_population["deaths"]:
            d = data_helpers.distance(decision, desired_destination)
            fitness = 1000 - abs(int(d))
            fits.append(fitness)
        self.fits = fits
        self.create_new_population()

    def create_new_population(self):
        """
        for p in pop do
            select partner
            cross over
            mutate
            append
        pop = pop_container
        """
        temp = []
        for chromosome in self.population:
            partner = self.select_partner()
            child = self.mutate(self.crossover(chromosome, partner))
            temp.append(child)
        self.population = temp

    def select_partner(self):
        fits = self.fits
        totals = []
        running_total = 0
        for f in fits:
            running_total += f
            totals.append(running_total)
        rnd = r.random() * running_total
        for i, t in enumerate(totals):
            if rnd < t:
                return self.population[i]

    def crossover(self, chromosome, partner):
        """
        in: parents [2]
        out: children [1]
        rate: 0.5
        """
        yes = r.randrange(0, 1)
        if yes:
            c = chromosome[:400] + partner[400:len(partner)]
            return c
        elif not yes:
            c = r.choice([chromosome, partner])
            return c

    def mutate(self, chromosome):
        position = r.randrange(0, len(chromosome))
        newvalue = r.randrange(-255, 255)
        chromosome[position] = newvalue
        return chromosome
