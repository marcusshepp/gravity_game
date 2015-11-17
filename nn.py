import re

from neuron import Neuron

def enemy_planets(file_path):
    _planets = []
    string_to_catch = "self.planets"
    with open(file_path, "r") as inputd:
        x = [line for line in inputd]
        x = [i for i in filter(lambda i: string_to_catch in i, x)]
        data = []
        for i in x:
            data.append(re.findall("[-+]?\d+[\.]?\d*", ''.join(i)))
        p0, p1, p2 = data[0][:5], data[0][5:10], data[0][10:15]
        _planets = [p0, p1, p2]
        inputd.close()
    return _planets

# print enemy_planets("maps/map1.md")

def to_bin(data, length):
    return bin(int(data))[2:].zfill(length)

def planet_to_bin_rep(planets):
    print planets
    planet_one = [to_bin(planets[0][0], 10),
                  to_bin(planets[0][1], 10),
                  to_bin(planets[0][4], 3)]
    planet_two = [to_bin(planets[1][0], 10),
                  to_bin(planets[1][1], 10),
                  to_bin(planets[1][4], 3)]
    planet_three = [to_bin(planets[2][0], 10),
                    to_bin(planets[2][1], 10),
                    to_bin(planets[2][4], 3)]
    return planet_one, planet_two, planet_three

def full_input(l):
    value = ""
    for i in l:
        for d in i:
            value += d
    return [i for i in value]

print len(full_input(planet_to_bin_rep(planets)))

def estimate_launch():
    pass

# def input(weights, thresholds, inputs):
#     n0 = Neuron([weights[0], weights[3]], inputs, thresholds[0])
#     n1 = Neuron([weights[1], weights[2]], inputs, thresholds[1])
#
# def hidden(weights, thresholds, inputs):
#     n2 = Neuron([weights[4], weights[7]], [n0.output(), n1.output()], thresholds[2])
#     n3 = Neuron([weights[5], weights[8]], [n0.output(), n1.output()], thresholds[3])
#     n4 = Neuron([weights[6], weights[9]], [n0.output(), n1.output()], thresholds[4])
#
# def out(weights, thresholds, inputs):
#     n5 = Neuron(
#         [weights[10], weights[11], weights[12]],
#         [n2.output(), n3.output(), n4.output()], thresholds[5])
#     return n5.output()
