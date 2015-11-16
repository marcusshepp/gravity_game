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

def planet_to_bin_rep(planets):
    planet_one_x = bin(int(planets[0][0]))
    planet_one_y = bin(int(planets[0][1]))
    planet_one_m = bin(int(planets[0][4]))
    planet_two_x = bin(int(planets[1][0]))
    planet_two_y = bin(int(planets[1][1]))
    planet_two_m = bin(int(planets[1][4]))
    planet_three_x = bin(int(planets[2][0]))
    planet_three_y = bin(int(planets[2][1]))
    planet_three_m = bin(int(planets[2][4]))
    ml = []
    ml.append(planet_one_x[2:])
    ml.append(planet_one_y[2:])
    ml.append(planet_one_m[2:])
    ml.append(planet_two_x[2:])
    ml.append(planet_two_y[2:])
    ml.append(planet_two_m[2:])
    ml.append(planet_three_x[2:])
    ml.append(planet_three_y[2:])
    ml.append(planet_three_m[2:])
    for item in ml:
        if len(item) > 2 and len(item) < 8:
            diff = 8 - len(item)
            print diff
            item = list(item)
            print item
            for i in range(diff):
                item.insert(0, 0)
            item = [str(i) for i in item]
            print "".join(item)
            print item
    return ml

print planet_to_bin_rep(enemy_planets("maps/map1.md"))

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
