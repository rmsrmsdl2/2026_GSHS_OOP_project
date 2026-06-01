import random
from config import INITIAL_POPULATION, MAX_POPULATION
from biomorph import Biomorph
from fitness import FitnessCalculator


class EvolutionEngine:
    def __init__(self):
        self.fitness_calculator = FitnessCalculator()

    def create_initial_population(self):
        return [Biomorph() for _ in range(INITIAL_POPULATION)]

    def next_generation(self, population, environment):
        for biomorph in population:
            self.fitness_calculator.calculate(biomorph, environment)

        population.sort(key=lambda b: b.fitness, reverse=True)

        survivor_count = max(10, len(population) // 2)
        survivors = population[:survivor_count]

        new_population = survivors.copy()

        while len(new_population) < INITIAL_POPULATION:
            parent = self._select_parent(survivors)
            child = parent.reproduce()
            new_population.append(child)

        return new_population[:MAX_POPULATION]

    def _select_parent(self, survivors):
        total_fitness = sum(b.fitness for b in survivors)

        if total_fitness == 0:
            return random.choice(survivors)

        pick = random.uniform(0, total_fitness)
        current = 0

        for biomorph in survivors:
            current += biomorph.fitness
            if current >= pick:
                return biomorph

        return survivors[-1]