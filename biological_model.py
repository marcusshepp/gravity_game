import random as r

def select_partner(fits, pop):
    """
    Mimics weighted selection with replacement.
    """
    totals = []
    running_total = 0
    for f in fits:
        running_total += f
        totals.append(running_total)
    rnd = r.random() * running_total
    for i, t in enumerate(totals):
        if rnd < t:
            return pop[i]

def crossover(chromosome, partner):
    """
    in: parents [2]
    out: children [1]
    rate: 0.5
    Crosses two chromosomes at their mid point.
    """
    # yes = r.randrange(0, 1)
    # if yes:
    c = chromosome[:400] + partner[400:len(partner)]
    return c
    # elif not yes:
    #     c = r.choice([chromosome, partner])
    #     return c

def mutate(chromosome):
    """
    mutates a random allel with rate of 1.
    """
    position = r.randrange(0, len(chromosome))
    newvalue = r.randrange(-255, 255)
    chromosome[position] = newvalue
    return chromosome
