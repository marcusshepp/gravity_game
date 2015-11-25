import net
import GA

ga = GA.GeneticTrainer(pop_size=2)
ga.set_board("maps/map1.md")
ga.init_population()
data = ga.nn_data(ga.population[0])
ann = net.NeuralNetwork(pickled=True)
print (ann.out())
