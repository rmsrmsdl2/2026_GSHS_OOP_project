import math

from config import TRAIT_NAMES


class Environment:
    def __init__(self):
        self.time = 0.0
        self.factors = {
            "light": 0.55,
            "humidity": 0.50,
            "wind": 0.35,
            "temperature": 0.52,
        }
        self.optimal_traits = {name: 0.5 for name in TRAIT_NAMES}

    def update(self, generation, speed=1.0):
        self.time += 0.010 * speed
        phase = generation * 0.37

        self.factors["light"] = self._wave(self.time * 0.70 + phase, 0.20, 0.90)
        self.factors["humidity"] = self._wave(self.time * 0.53 + phase * 1.7, 0.18, 0.86)
        self.factors["wind"] = self._wave(self.time * 0.91 + phase * 0.6, 0.12, 0.82)
        self.factors["temperature"] = self._wave(self.time * 0.41 + phase * 2.1, 0.25, 0.88)
        self._update_optimal_traits()

    def fitness(self, biomorph):
        distance = 0.0
        weights = {
            "trunk_length": 0.9,
            "branch_angle": 1.2,
            "curvature": 0.7,
            "branch_ratio": 0.8,
            "body_width": 0.9,
            "wing_span": 1.1,
            "antenna_angle": 0.7,
            "recursion_depth": 0.6,
            "mutation_rate": 0.4,
        }

        for name in TRAIT_NAMES:
            trait = biomorph.genome.traits[name]
            target = self.optimal_traits[name]
            distance += weights[name] * (trait - target) ** 2

        return math.exp(-distance * 2.4)

    def _update_optimal_traits(self):
        light = self.factors["light"]
        humidity = self.factors["humidity"]
        wind = self.factors["wind"]
        temperature = self.factors["temperature"]

        self.optimal_traits.update({
            "trunk_length": 0.25 + light * 0.45,
            "branch_angle": 0.20 + light * 0.50,
            "curvature": 0.20 + wind * 0.55,
            "branch_ratio": 0.25 + humidity * 0.50,
            "body_width": 0.28 + temperature * 0.42,
            "wing_span": 0.18 + wind * 0.56,
            "antenna_angle": 0.18 + humidity * 0.58,
            "recursion_depth": 0.22 + light * 0.45,
            "mutation_rate": 0.18 + abs(temperature - humidity) * 0.65,
        })

    def _wave(self, value, low, high):
        normalized = (math.sin(value) + 1.0) / 2.0
        return low + normalized * (high - low)
