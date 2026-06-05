class FitnessCalculator:
    def calculate(self, biomorph, environment):
        fitness = environment.fitness(biomorph)
        biomorph.fitness = fitness
        return fitness
