"""
# Genetic Algorithm
#
### in: none
### out: weights, thresholds
#
#
"""
import random as r

from net import NeuralNetwork
from data_helpers import get_data


def init_population(pop_size):
    population = []
    for _ in range(pop_size):
        chrome = []
        # size of chrome
        # total number of weights and thresholds
        for i in range(869):
            chrome.append(r.randrange(-255, 255))
        population.append(chrome)
    return population

def decode(chrome):
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

def nn_data(chrome, path):
    """
    put the data into a dict to easily create a nn object.
    in: chromosome, path to current_board
    out: data that my ann can be created with
    """
    decoded_chrome = decode(chrome)
    data = dict()
    data["num_input_nodes"] = 9
    data["num_hidden_nodes"] = 5
    data["num_output_nodes"] = 20
    data["inputs"] = get_data(path)
    data["first_weights"] = decoded_chrome[0]
    data["second_weights"] = decoded_chrome[1]
    data["third_weights"] = decoded_chrome[2]
    data["first_thresholds"] = decoded_chrome[3]
    data["second_thresholds"] = decoded_chrome[4]
    data["third_thresholds"] = decoded_chrome[5]
    return data

def decode_output(out):
    """
    in: binary string
    out: x, y corrdinates
    """
    return [int("".join([str(i) for i in out[:10]]), 2), int("".join([str(i) for i in out[10:]]), 2)]

def fitness(chrome):
    """
    find the distance between the dying point and the destination planet.
    """
    pass

def evolve(gens, current_board):
    """
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
    """
    pop_size = 1
    pop = init_population(pop_size)
    for _ in range(gens):
        temp_pop = []
        for chrome in pop:
            data_for_network = nn_data(chrome, current_board)
            ann = NeuralNetwork(data_for_network)
            x, y = decode_output(ann.out())
            return x, y


if __name__ == '__main__':
    print(evolve(1, "maps/map1.md"))
