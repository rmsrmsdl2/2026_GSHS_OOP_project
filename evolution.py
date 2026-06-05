from biomorph import Biomorph
from config import POPULATION_SIZE


class EvolutionEngine:
    def create_initial_population(self):
        return [Biomorph() for _ in range(POPULATION_SIZE)]

    def next_generation_from_parent(self, parent):
        children = [parent]

        while len(children) < POPULATION_SIZE:
            children.append(parent.breed_child())

        return children
