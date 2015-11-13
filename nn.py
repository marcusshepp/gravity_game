import re

from neuron import Neuron

[[200,100,50,50,1],[400,100,50,50,1],[600,100,50,50,1]]


def has(line):
    i = "self.planets"
    return i in line

with open("maps/map1.md", "r") as inputd:
    x = [line for line in inputd]
    x = [i for i in x if has(str(i))]
    data = []
    for i in x:
        data.append(re.findall("[-+]?\d+[\.]?\d*", ''.join(i)))
    print data
    p0 = data[0][:5]
    print p0
    p1 = data[0][5:10]
    print p1
    p2 = data[0][10:15]
    print p2
    




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
