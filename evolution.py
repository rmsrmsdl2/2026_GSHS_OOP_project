import random
from config import (
    ELITE_RATE,
    INITIAL_POPULATION,
    MAX_POPULATION,
    MIN_POPULATION,
    OFFSPRING_PER_PAIR,
    SURVIVAL_PRESSURE,
)
from biomorph import Biomorph
from fitness import FitnessCalculator


class EvolutionEngine:
    def __init__(self):
        self.fitness_calculator = FitnessCalculator()
        self.last_stats = {
            "best_fitness": 0.0,
            "average_fitness": 0.0,
            "average_error": 0.0,
            "survivors": 0,
            "births": 0,
        }

    def create_initial_population(self):
        return [Biomorph() for _ in range(INITIAL_POPULATION)]

    def evaluate(self, population, environment):
        total_fitness = 0.0
        total_error = 0.0

        for biomorph in population:
            total_fitness += self.fitness_calculator.calculate(biomorph, environment)
            total_error += biomorph.selection_error

        population.sort(key=lambda b: b.fitness, reverse=True)

        self.last_stats["best_fitness"] = population[0].fitness if population else 0.0
        self.last_stats["average_fitness"] = total_fitness / len(population)
        self.last_stats["average_error"] = total_error / len(population)

    def next_generation(self, population, environment):
        self.evaluate(population, environment)

        elite_count = max(2, int(len(population) * ELITE_RATE))
        elites = population[:elite_count]
        survivors = self._select_survivors(population)

        target_size = self._target_population_size(population)
        new_population = elites.copy()
        births = 0

        while len(new_population) < target_size:
            parent_a = self._roulette_select(survivors)
            parent_b = self._roulette_select(survivors)

            for _ in range(OFFSPRING_PER_PAIR):
                if len(new_population) >= target_size:
                    break
                child = parent_a.reproduce_with(parent_b)
                new_population.append(child)
                births += 1

        self.last_stats["survivors"] = len(survivors)
        self.last_stats["births"] = births
        return new_population[:MAX_POPULATION]

    def _select_survivors(self, population):
        survivors = []

        for biomorph in population:
            survival_chance = biomorph.fitness ** SURVIVAL_PRESSURE
            if random.random() < survival_chance:
                survivors.append(biomorph)

        minimum = max(6, int(len(population) * 0.25))
        if len(survivors) < minimum:
            survivors = population[:minimum]

        return survivors

    def _target_population_size(self, population):
        average_fitness = self.last_stats["average_fitness"]
        growth = int((average_fitness - 0.45) * 34)
        target = INITIAL_POPULATION + growth
        return max(MIN_POPULATION, min(MAX_POPULATION, target))

    def _roulette_select(self, survivors):
        total_fitness = sum(b.fitness for b in survivors)

        if total_fitness <= 0:
            return random.choice(survivors)

        pick = random.uniform(0, total_fitness)
        current = 0.0

        for biomorph in survivors:
            current += biomorph.fitness
            if current >= pick:
                return biomorph

        return survivors[-1]
