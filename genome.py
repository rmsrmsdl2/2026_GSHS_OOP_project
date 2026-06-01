import random
from config import TRAIT_NAMES, MUTATION_STRENGTH


class Genome:
    def __init__(self, traits=None):
        self.traits = traits if traits else {
            name: random.uniform(0.0, 1.0) for name in TRAIT_NAMES
        }

    def copy(self):
        return Genome(self.traits.copy())

    def mutate(self):
        new_traits = self.traits.copy()
        mutation_rate = new_traits["mutation_rate"]

        for name in TRAIT_NAMES:
            if random.random() < mutation_rate:
                change = random.uniform(-MUTATION_STRENGTH, MUTATION_STRENGTH)
                new_traits[name] = min(1.0, max(0.0, new_traits[name] + change))

        return Genome(new_traits)

    def get_vector(self):
        return [self.traits[name] for name in TRAIT_NAMES]