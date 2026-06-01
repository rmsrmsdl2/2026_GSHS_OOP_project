import math
import random
from config import TRAIT_NAMES, TRAIT_WEIGHTS


class Environment:
    STABLE = 1
    PERIODIC = 2
    SHOCK = 3

    def __init__(self):
        self.generation = 0
        self.mode = self.STABLE
        self.name = "Stable Selection"
        self.description = "A long-lasting pressure slowly favors one phenotype."
        self.optimal_traits = {name: 0.5 for name in TRAIT_NAMES}
        self.trait_weights = TRAIT_WEIGHTS.copy()
        self.factors = {
            "sunlight": 0.55,
            "food": 0.55,
            "wind": 0.35,
            "temperature": 0.50,
        }
        self.history = []
        self.event_log = []

    def update(self, generation):
        self.generation = generation

        if generation == 1 or generation % 12 == 0:
            self.mode = random.choice([self.STABLE, self.PERIODIC, self.SHOCK])
            self._record_mode_event()

        if self.mode == self.STABLE:
            self._stable_selection()
        elif self.mode == self.PERIODIC:
            self._periodic_selection()
        else:
            self._shock_selection()

        self.history.append({
            "generation": generation,
            "mode": self.mode,
            "name": self.name,
            "optimal_traits": self.optimal_traits.copy(),
            "trait_weights": self.trait_weights.copy(),
            "factors": self.factors.copy(),
        })

    def _record_mode_event(self):
        if self.mode == self.STABLE:
            self.name = "Stable Selection"
            self.description = "Constant pressure: one environment remains dominant."
        elif self.mode == self.PERIODIC:
            self.name = "Periodic Change"
            self.description = "Seasonal pressure: optimal traits oscillate by generation."
        else:
            self.name = "Sudden Climate Shift"
            self.description = "Shock pressure: wind, food, and temperature change sharply."

        self.event_log.append((self.generation, self.name))
        self.event_log = self.event_log[-6:]

    def _stable_selection(self):
        self.factors["sunlight"] = self._approach(self.factors["sunlight"], 0.78, 0.025)
        self.factors["food"] = self._approach(self.factors["food"], 0.48, 0.012)
        self.factors["wind"] = self._approach(self.factors["wind"], 0.38, 0.010)
        self.factors["temperature"] = self._approach(self.factors["temperature"], 0.55, 0.010)

        self.optimal_traits.update({
            "body_size": 0.42,
            "branch_angle": 0.72,
            "movement_speed": 0.48,
            "energy_efficiency": 0.68,
            "mutation_rate": 0.26,
        })
        self.trait_weights.update({
            "body_size": 0.95,
            "branch_angle": 1.85,
            "movement_speed": 0.85,
            "energy_efficiency": 1.35,
            "mutation_rate": 0.45,
        })

    def _periodic_selection(self):
        wave = (math.sin(self.generation * 0.55) + 1.0) / 2.0

        self.factors["sunlight"] = 0.25 + wave * 0.65
        self.factors["food"] = 0.85 - wave * 0.55
        self.factors["wind"] = 0.25 + (1.0 - wave) * 0.45
        self.factors["temperature"] = 0.35 + wave * 0.45

        self.optimal_traits.update({
            "body_size": 0.30 + self.factors["food"] * 0.45,
            "branch_angle": 0.25 + self.factors["sunlight"] * 0.65,
            "movement_speed": 0.30 + self.factors["wind"] * 0.50,
            "energy_efficiency": 0.45 + (1.0 - self.factors["food"]) * 0.40,
            "mutation_rate": 0.32 + abs(wave - 0.5) * 0.22,
        })
        self.trait_weights.update({
            "body_size": 1.10,
            "branch_angle": 1.50,
            "movement_speed": 1.35,
            "energy_efficiency": 1.20,
            "mutation_rate": 0.70,
        })

    def _shock_selection(self):
        if self.generation % 12 == 0:
            self.factors["sunlight"] = random.uniform(0.10, 0.92)
            self.factors["food"] = random.uniform(0.08, 0.42)
            self.factors["wind"] = random.uniform(0.70, 0.98)
            self.factors["temperature"] = random.choice([0.15, 0.88])
        else:
            self.factors["food"] = self._approach(self.factors["food"], 0.50, 0.020)
            self.factors["wind"] = self._approach(self.factors["wind"], 0.45, 0.025)

        self.optimal_traits.update({
            "body_size": 0.20 + self.factors["food"] * 0.35,
            "branch_angle": 0.20 + self.factors["sunlight"] * 0.50,
            "movement_speed": 0.62 + self.factors["wind"] * 0.25,
            "energy_efficiency": 0.72 + (1.0 - self.factors["food"]) * 0.20,
            "mutation_rate": 0.62,
        })
        self.trait_weights.update({
            "body_size": 1.80,
            "branch_angle": 0.90,
            "movement_speed": 1.60,
            "energy_efficiency": 1.95,
            "mutation_rate": 1.10,
        })

    def _approach(self, current, target, step):
        if current < target:
            return min(target, current + step)
        return max(target, current - step)

    def get_dominant_pressure(self):
        return max(self.trait_weights, key=self.trait_weights.get)
