import math
from config import TRAIT_NAMES, TRAIT_WEIGHTS


class FitnessCalculator:
    def calculate(self, biomorph, environment):
        distance = 0.0

        for name in TRAIT_NAMES:
            trait = biomorph.genome.traits[name]
            optimal = environment.optimal_traits[name]
            weight = TRAIT_WEIGHTS[name]
            distance += weight * ((trait - optimal) ** 2)

        fitness = math.exp(-distance)
        biomorph.fitness = fitness
        return fitness