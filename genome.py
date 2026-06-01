import random
from config import TRAIT_NAMES, MUTATION_STRENGTH


def clamp(value, low=0.0, high=1.0):
    return max(low, min(high, value))


class Genome:
    def __init__(self, traits=None):
        self.traits = traits if traits else {
            name: random.uniform(0.15, 0.85) for name in TRAIT_NAMES
        }

    def copy(self):
        return Genome(self.traits.copy())

    def crossover(self, other):
        child_traits = {}

        for name in TRAIT_NAMES:
            blend = random.uniform(0.35, 0.65)
            child_traits[name] = (
                self.traits[name] * blend
                + other.traits[name] * (1.0 - blend)
            )

        return Genome(child_traits)

    def mutate(self):
        new_traits = self.traits.copy()
        mutation_rate = clamp(0.03 + new_traits["mutation_rate"] * 0.22)

        for name in TRAIT_NAMES:
            if random.random() < mutation_rate:
                change = random.gauss(0, MUTATION_STRENGTH)
                new_traits[name] = clamp(new_traits[name] + change)

        return Genome(new_traits)

    def get_vector(self):
        return [self.traits[name] for name in TRAIT_NAMES]
