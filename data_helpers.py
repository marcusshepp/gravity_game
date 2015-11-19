import re

def nn_info(inp,inl,hid,out):
    """
    given hidden input and out
    gives number of weights0 + weights1 + weights2 + thresholds needed
    """
    w0 = inp * inl
    w1 = inl * hid
    w2 = hid * out
    p = lambda x, y, z: "Weights from {0} to {1}: {2}\n".format(x, y, z)
    print( p("input", "layer one", str(w0)))
    print( p("layer one", "layer two", str(w1)))
    print( p("layer two", "layer three", str(w2)))
    print( "total weights: {0}\n".format(w0+w1+w2))
    print( "{0} thresholds are needed. \n".format(inp+hid+out))
    print( "total: ",w0 + w1 + w2 + inp + inl + hid + out, "\n")
    return w0, w1, w2, inl,hid,out

def to_bin(data, length):
    """
    in: string, length of desired result
    out: binary representation
    """
    return bin(int(data))[2:].zfill(length)

def planet_to_bin_rep(planets):
    """
    in: data from game map
    out: data for enemy planets
    """
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
    """
    further filtering the enemy planet data.
    """
    value = ""
    for i in l:
        for d in i:
            value += d
    return [int(i) for i in value]

def get_data(path):
    """
    opens file and runs algo on data.
    returns x, y coor in bin for ann.
    """
    def has(line):
        i = "self.planets"
        return i in line
    with open(path, "r") as inputd:
        x = [line for line in inputd]
        x = [i for i in x if has(str(i))]
        data = []
        for i in x:
            data.append(re.findall("[-]?\d[\.]?\d*", ''.join(i)))
        p0 = data[0][:5]
        p1 = data[0][5:10]
        p2 = data[0][10:15]
        return full_input(planet_to_bin_rep([p0, p1, p2]))
