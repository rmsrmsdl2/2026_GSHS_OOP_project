from config import SCREEN_WIDTH, SCREEN_HEIGHT, GENERATION_INTERVAL, TRAIT_NAMES
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

        self.average_trait_history = []
        self.population_history = []

    def update(self):
        if self.paused:
            return

        for biomorph in self.population:
            biomorph.update(SCREEN_WIDTH, SCREEN_HEIGHT)

        self.frame_count += 1

        if self.frame_count >= GENERATION_INTERVAL:
            self.next_generation()
            self.frame_count = 0

    def next_generation(self):
        self.environment.update(self.generation)
        self.population = self.engine.next_generation(self.population, self.environment)

        self.average_trait_history.append(self.get_average_traits())
        self.population_history.append(len(self.population))

        self.generation += 1

    def get_average_traits(self):
        averages = {}

        for name in TRAIT_NAMES:
            total = sum(b.genome.traits[name] for b in self.population)
            averages[name] = total / len(self.population)

        return averages

    def toggle_pause(self):
        self.paused = not self.paused