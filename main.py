import random
from operator import attrgetter
import matplotlib.pyplot as plt
import copy

populationSize = 50
geneCount = 50
generations = 50


class Individual:
    def __init__(self):
        self.gene = []
        self.fitness = 0.0

    def __repr__(self):
        return "<Gene = " + str(self.gene) + ">" + " <Fitness = " + str(self.fitness) + ">\n"


def mutation(child):
    mutation_rate = random.uniform(1 / populationSize, 1 / geneCount)
    for i in range(0, len(child.gene)):
        mutation_probability = random.uniform(0.0, 1.0)
        if mutation_probability < (100 * mutation_rate):
            alteration = random.uniform(0, mutation_probability)

            if random.randint(1, 2) % 2:
                if child.gene[i] + alteration < 1.0:
                    child.gene[i] = child.gene[i] + alteration
                else:
                    child.gene[i] = 1.0
            else:
                if child.gene[i] + alteration > 0.0:
                    child.gene[i] = child.gene[i] - alteration
                else:
                    child.gene[i] = 1.0


def evaluate(array):
    fitness = 0.0
    loop = 0
    for agents in array:
        for _ in agents.gene:
            fitness = fitness + agents.gene[loop]
            loop = loop + 1
        agents.fitness = fitness
        fitness = 0.0
        loop = 0


def get_fittest(array):
    temp = copy.deepcopy(array)
    temp.sort(key=attrgetter('fitness'), reverse=True)
    fittest = temp[0]
    return fittest


def get_mean_average(array):
    total = 0.0
    evaluate(array)
    for offspring in array:
        total = total + offspring.fitness
    return total / len(array)


class Population:
    def __init__(self):
        self.agents = []
        self.offspring = []

    def add_individuals(self, population_size, gene_count):
        for _ in range(0, population_size):
            gene = []
            for _ in range(0, gene_count):
                gene.append(random.uniform(0.0, 1.0))
            individual = Individual()
            individual.gene = gene[:]
            self.agents.append(individual)

    def select_parents(self):
        self.offspring = []
        for i in range(0, populationSize):
            p1 = random.randint(0, populationSize - 1)
            p2 = random.randint(0, populationSize - 1)

            if self.agents[p1].fitness >= self.agents[p2].fitness:
                self.offspring.append(self.agents[p1])
            else:
                self.offspring.append(self.agents[p2])

    def crossover_mutation(self):
        new_population = []
        end = int(populationSize / 2)
        for _ in range(0, end):
            a = random.randint(0, populationSize - 1)
            b = random.randint(0, populationSize - 1)

            individual_one = self.offspring[a]
            individual_two = self.offspring[b]

            cross_point = random.randint(int(geneCount * 0.5), int(geneCount * 0.9))

            child1 = Individual()
            child2 = Individual()
            child1.gene = individual_one.gene[:cross_point]
            child1.gene.extend(individual_two.gene[cross_point:])
            child2.gene = individual_two.gene[:cross_point]
            child2.gene.extend(individual_one.gene[cross_point:])

            mutation(child1)
            mutation(child2)

            new_population.append(child1)
            new_population.append(child2)

        self.offspring = new_population


def main():
    fittest = []
    mean_average = []
    population = Population()
    population.add_individuals(populationSize, geneCount)
    evaluate(population.agents)

    for _ in range(0, generations):
        population.select_parents()
        population.crossover_mutation()
        evaluate(population.offspring)
        fittest_individual = get_fittest(population.offspring)
        mean_fitness = get_mean_average(population.offspring)
        fittest.append(fittest_individual.fitness)
        mean_average.append(mean_fitness)
        population.agents = copy.deepcopy(population.offspring)

    print("Fittest", fittest[-1])
    print("Mean Average", mean_average[-1])
    plt.plot(fittest)
    plt.plot(mean_average)
    plt.ylabel('Fittest (Blue) & Mean Average Fitness (Orange)')
    plt.xlabel('Generations')
    plt.show()


main()
