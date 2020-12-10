import copy
import random
import math
from operator import attrgetter

import matplotlib.pyplot as plt

populationSize = 20
geneCount = 10
generations = 200
mutationStep = random.uniform(0.0, 0.01)  # Mutation step needs to be small to reach a near perfect child


class Individual:
    def __init__(self):
        self.gene = []
        self.fitness = 0.0


def mutation(child):
    mutation_rate = random.uniform(1 / populationSize, 1 / geneCount)

    for i in range(0, len(child.gene)):
        mutation_probability = random.uniform(0.0, 1.0)
        if mutation_probability < (100 * mutation_rate):
            alteration = random.uniform(0, mutationStep)
            if random.randint(1, 2) % 2:
                if child.gene[i] + alteration < 5.12:  # Ensure a gene cannot be more than 5.12
                    child.gene[i] = child.gene[i] + alteration
                else:
                    child.gene[i] = 5.12
            else:
                if child.gene[i] + alteration > -5.12:  # Ensure a gene cannot be less than 5.12
                    child.gene[i] = child.gene[i] - alteration
                else:
                    child.gene[i] = -5.12


def evaluate(array):
    fitness = 10 * geneCount
    loop = 0
    for agents in array:
        for _ in agents.gene:
            # Minimisation function
            fitness = fitness + (agents.gene[loop] * agents.gene[loop] - 10 * math.cos(2 * math.pi * agents.gene[loop]))
            loop = loop + 1
        agents.fitness = fitness
        fitness = 0.0
        loop = 0


def get_fittest(array):
    temp = copy.deepcopy(array)
    temp.sort(key=attrgetter('fitness'), reverse=False)
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
                gene.append(random.uniform(-5.12, 5.12))
            individual = Individual()
            individual.gene = gene[:]
            self.agents.append(individual)

    # Tournament Selection
    def select_parents(self):
        self.offspring = []
        for i in range(0, populationSize):
            p1 = random.randint(0, populationSize - 1)  # -1 because array starts at 0
            p2 = random.randint(0, populationSize - 1)

            if self.agents[p1].fitness <= self.agents[p2].fitness:  # We want the smaller fitness
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


def PerformTournamentSelection():
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
    plt.legend(['Fittest', 'Average'])
    plt.ylabel('Fittest & Mean Average Fitness')
    plt.xlabel('Generations')
    plt.show()
