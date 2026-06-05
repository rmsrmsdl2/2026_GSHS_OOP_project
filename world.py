import random

from biomorph import Biomorph
from config import POPULATION_SIZE
from environment import Environment


class World:
    def __init__(self):
        self.generation = 1
        self.environment = Environment()
        self.population = [Biomorph() for _ in range(POPULATION_SIZE)]
        self.selected_index = 0
        self.message = "바이오모프를 클릭하면 그 개체를 부모로 다음 세대를 만듭니다."
        self.environment.update(self.generation)

    @property
    def selected(self):
        return self.population[self.selected_index]

    def update(self):
        self.environment.update(self.generation)

    def select(self, index):
        if not 0 <= index < len(self.population):
            return

        parent = self.population[index]
        self.population = self._children_from(parent)
        self.selected_index = 0
        self.generation += 1
        self.message = f"{self.generation}세대: #{parent.id} 개체를 부모로 선택했습니다."

    def randomize(self):
        self.population = [Biomorph() for _ in range(POPULATION_SIZE)]
        self.selected_index = 0
        self.generation = 1
        self.environment = Environment()
        self.environment.update(self.generation)
        self.message = "새로운 무작위 바이오모프 집단을 만들었습니다."

    def mutate_selected(self):
        parent = self.selected
        self.population = self._children_from(parent)
        self.selected_index = 0
        self.generation += 1
        self.message = f"{self.generation}세대: #{parent.id} 개체에서 변이시켰습니다."

    def _children_from(self, parent):
        children = [parent]

        while len(children) < POPULATION_SIZE:
            if len(children) > 2 and random.random() < 0.20:
                partner = random.choice(children)
                children.append(parent.crossover_child(partner))
            else:
                children.append(parent.breed_child())

        return children

    def fitness(self, biomorph):
        return self.environment.fitness(biomorph)
