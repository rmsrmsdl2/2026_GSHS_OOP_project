from config import GENERATION_INTERVAL, SCREEN_HEIGHT, SCREEN_WIDTH, TRAIT_NAMES
from environment import Environment
from evolution import EvolutionEngine


class World:
    def __init__(self):
        self.environment = Environment()
        self.engine = EvolutionEngine()
        self.population = self.engine.create_initial_population()

        self.generation = 1
        self.frame_count = 0
        self.paused = False
        self.speed_multiplier = 1

        self.average_trait_history = []
        self.population_history = []
        self.fitness_history = []
        self.error_history = []

        self.environment.update(self.generation)
        self.engine.evaluate(self.population, self.environment)
        self._record_generation()

    def update(self):
        if self.paused:
            return

        for _ in range(self.speed_multiplier):
            for biomorph in self.population:
                biomorph.update(SCREEN_WIDTH, SCREEN_HEIGHT)

            self.frame_count += 1

            if self.frame_count >= GENERATION_INTERVAL:
                self.next_generation()
                self.frame_count = 0

    def next_generation(self):
        self.generation += 1
        self.environment.update(self.generation)
        self.population = self.engine.next_generation(self.population, self.environment)
        self._record_generation()

    def _record_generation(self):
        self.average_trait_history.append(self.get_average_traits())
        self.population_history.append(len(self.population))
        self.fitness_history.append(self.engine.last_stats["average_fitness"])
        self.error_history.append(self.engine.last_stats["average_error"])

        self.average_trait_history = self.average_trait_history[-80:]
        self.population_history = self.population_history[-80:]
        self.fitness_history = self.fitness_history[-80:]
        self.error_history = self.error_history[-80:]

    def get_average_traits(self):
        averages = {}

        for name in TRAIT_NAMES:
            total = sum(b.genome.traits[name] for b in self.population)
            averages[name] = total / len(self.population)

        return averages

    def get_best_biomorph(self):
        return max(self.population, key=lambda biomorph: biomorph.fitness)

    def toggle_pause(self):
        self.paused = not self.paused

    def cycle_speed(self):
        if self.speed_multiplier == 1:
            self.speed_multiplier = 2
        elif self.speed_multiplier == 2:
            self.speed_multiplier = 4
        else:
            self.speed_multiplier = 1
