import random
from config import TRAIT_NAMES


class Environment:
    def __init__(self):
        self.generation = 0
        self.mode = 1
        self.name = "Stable Selection"
        self.optimal_traits = {name: 0.5 for name in TRAIT_NAMES}
        self.history = []

    def update(self, generation):
        self.generation = generation

        if generation % 8 == 0:
            self.mode = random.choice([1, 2, 3])

            if self.mode == 1:
                self.name = "Stable Selection"
                self._stable_change()
            elif self.mode == 2:
                self.name = "Periodic Change"
                self._periodic_change()
            else:
                self.name = "Sudden Climate Shift"
                self._sudden_change()

        self.history.append(self.optimal_traits.copy())

    def _stable_change(self):
        selected = random.choice(TRAIT_NAMES)
        self.optimal_traits[selected] = random.uniform(0.35, 0.75)

    def _periodic_change(self):
        self.optimal_traits["branch_angle"] = 0.2 if self.optimal_traits["branch_angle"] > 0.5 else 0.8
        self.optimal_traits["movement_speed"] = 0.75 if self.optimal_traits["movement_speed"] < 0.5 else 0.25

    def _sudden_change(self):
        self.optimal_traits = {
            name: random.uniform(0.05, 0.95) for name in TRAIT_NAMES
        }