from biomorph import Biomorph
from config import CHILDREN_PER_PARENT, GENERATION_INTERVAL, PARENT_COUNT, POPULATION_SIZE
from environment import Environment


class World:
    def __init__(self):
        self.generation = 1
        self.frame_count = 0
        self.paused = False
        self.auto_generation = True
        self.environment = Environment()
        self.population = [Biomorph() for _ in range(POPULATION_SIZE)]
        self.selected_index = 0
        self.parent_ids = []
        self.message = "상위 5개체가 자동으로 부모가 되어 다음 세대를 만듭니다."
        self.environment.update(self.generation)

    @property
    def selected(self):
        return self.population[self.selected_index]

    def update(self):
        if self.paused:
            return

        self.environment.update(self.generation)
        self.frame_count += 1

        if self.auto_generation and self.frame_count >= GENERATION_INTERVAL:
            self.next_generation()

    def select(self, index):
        if 0 <= index < len(self.population):
            self.selected_index = index
            biomorph = self.population[index]
            self.message = f"#{biomorph.id} 개체 정보를 표시합니다. 번식은 적합도 기준으로 자동 진행됩니다."

    def next_generation(self):
        ranked = self.ranked_population()
        parents = [biomorph for biomorph, _score in ranked[:PARENT_COUNT]]
        self.parent_ids = [parent.id for parent in parents]

        children = []
        for parent in parents:
            for _ in range(CHILDREN_PER_PARENT):
                children.append(parent.breed_child())

        self.population = children
        self.selected_index = 0
        self.generation += 1
        self.frame_count = 0
        self.environment.update(self.generation)
        self.message = f"{self.generation}세대: 적합도 상위 5개체가 각각 자손 3개를 만들었습니다."

    def ranked_population(self):
        return sorted(
            ((biomorph, self.fitness(biomorph)) for biomorph in self.population),
            key=lambda item: item[1],
            reverse=True,
        )

    def randomize(self):
        self.population = [Biomorph() for _ in range(POPULATION_SIZE)]
        self.selected_index = 0
        self.generation = 1
        self.frame_count = 0
        self.parent_ids = []
        self.environment = Environment()
        self.environment.update(self.generation)
        self.message = "새로운 무작위 바이오모프 집단을 만들었습니다."

    def toggle_pause(self):
        self.paused = not self.paused

    def toggle_auto_generation(self):
        self.auto_generation = not self.auto_generation
        mode = "자동" if self.auto_generation else "수동"
        self.message = f"세대 교체 모드: {mode}"

    def trigger_disaster(self):
        self.environment.trigger_disaster()
        self.message = f"자연재해 발생: {self.environment.disaster_name}"

    def fitness(self, biomorph):
        return self.environment.fitness(biomorph)
