# -*- coding: utf-8 -*-

import math
import random

from config import FACTOR_NAMES, TRAIT_NAMES


class Environment:
    def __init__(self):
        self.time = 0.0
        self.auto_mode = True
        self.selected_factor_index = 0
        self.factors = {
            "light": 0.55,
            "humidity": 0.50,
            "wind": 0.35,
            "temperature": 0.52,
        }
        self.optimal_traits = {name: 0.5 for name in TRAIT_NAMES}
        self.disaster_timer = 0
        self.disaster_name = ""
        self.event_log = ["자동 환경 변화가 시작되었습니다."]
        self._update_optimal_traits()

    @property
    def selected_factor(self):
        return FACTOR_NAMES[self.selected_factor_index]

    def update(self, generation, speed=1.0):
        self.time += 0.010 * speed

        if self.auto_mode:
            self._auto_update(generation)

        if self.disaster_timer > 0:
            self.disaster_timer -= 1
            if self.disaster_timer == 0:
                self.disaster_name = ""
                self._push_event("급격한 환경 변화가 종료되었습니다.")

        self._update_optimal_traits()

    def toggle_auto_mode(self):
        self.auto_mode = not self.auto_mode
        mode = "자동" if self.auto_mode else "수동"
        self._push_event(f"환경 조절 모드: {mode}")

    def select_factor(self, index):
        self.selected_factor_index = index % len(FACTOR_NAMES)

    def adjust_selected_factor(self, amount):
        self.auto_mode = False
        name = self.selected_factor
        self.factors[name] = self._clamp(self.factors[name] + amount)
        self._update_optimal_traits()

    def trigger_disaster(self):
        disasters = [
            ("가뭄", {"humidity": 0.08, "temperature": 0.86, "wind": 0.62}),
            ("폭풍", {"wind": 0.96, "light": 0.24, "humidity": 0.72}),
            ("한파", {"temperature": 0.12, "wind": 0.56, "light": 0.38}),
            ("폭염", {"temperature": 0.96, "humidity": 0.22, "light": 0.86}),
        ]
        self.disaster_name, changes = random.choice(disasters)
        for name, value in changes.items():
            self.factors[name] = value
        self.disaster_timer = 180
        self._push_event(f"급격한 환경 변화 발생: {self.disaster_name}")
        self._update_optimal_traits()

    def fitness(self, biomorph):
        traits = biomorph.genome.traits
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
            distance += weights[name] * (traits[name] - self.optimal_traits[name]) ** 2

        combo_penalty = self._combo_penalty(traits)
        disaster_penalty = self._disaster_penalty(traits)
        return math.exp(-(distance * 2.2 + combo_penalty + disaster_penalty))

    def _combo_penalty(self, traits):
        wind = self.factors["wind"]
        humidity = self.factors["humidity"]
        light = self.factors["light"]
        temperature = self.factors["temperature"]
        penalty = 0.0

        if wind > 0.65:
            penalty += max(0.0, traits["wing_span"] - 0.45) * (wind - 0.65) * 1.5
            penalty += max(0.0, 0.35 - traits["body_width"]) * (wind - 0.65) * 0.9

        if humidity > 0.60:
            mismatch = abs(traits["antenna_angle"] - traits["branch_ratio"])
            penalty += mismatch * (humidity - 0.60) * 0.8

        if light > 0.65:
            mismatch = abs(traits["branch_angle"] - traits["recursion_depth"])
            penalty += mismatch * (light - 0.65) * 0.7

        if temperature > 0.70:
            penalty += max(0.0, traits["body_width"] - 0.58) * (temperature - 0.70) * 1.1
            penalty += max(0.0, traits["recursion_depth"] - 0.70) * (temperature - 0.70) * 0.8

        return penalty

    def _disaster_penalty(self, traits):
        if not self.disaster_name:
            return 0.0

        if self.disaster_name == "폭풍":
            return max(0.0, traits["wing_span"] - 0.35) * 0.9
        if self.disaster_name == "가뭄":
            return max(0.0, 0.45 - traits["mutation_rate"]) * 0.7
        if self.disaster_name == "한파":
            return max(0.0, 0.45 - traits["body_width"]) * 0.8
        if self.disaster_name == "폭염":
            return max(0.0, traits["body_width"] - 0.55) * 0.8
        return 0.0

    def _auto_update(self, generation):
        phase = generation * 0.37
        self.factors["light"] = self._wave(self.time * 0.70 + phase, 0.20, 0.90)
        self.factors["humidity"] = self._wave(self.time * 0.53 + phase * 1.7, 0.18, 0.86)
        self.factors["wind"] = self._wave(self.time * 0.91 + phase * 0.6, 0.12, 0.82)
        self.factors["temperature"] = self._wave(self.time * 0.41 + phase * 2.1, 0.25, 0.88)

    def _update_optimal_traits(self):
        light = self.factors["light"]
        humidity = self.factors["humidity"]
        wind = self.factors["wind"]
        temperature = self.factors["temperature"]
        instability = abs(temperature - humidity) + abs(wind - light)

        self.optimal_traits.update({
            "trunk_length": 0.25 + light * 0.45,
            "branch_angle": 0.20 + light * 0.50,
            "curvature": 0.20 + wind * 0.55,
            "branch_ratio": 0.25 + humidity * 0.50,
            "body_width": 0.70 - temperature * 0.42,
            "wing_span": 0.72 - wind * 0.50,
            "antenna_angle": 0.18 + humidity * 0.58,
            "recursion_depth": 0.22 + light * 0.45,
            "mutation_rate": 0.16 + min(0.72, instability * 0.60),
        })

    def _push_event(self, text):
        self.event_log.append(text)
        self.event_log = self.event_log[-5:]

    def _wave(self, value, low, high):
        normalized = (math.sin(value) + 1.0) / 2.0
        return low + normalized * (high - low)

    def _clamp(self, value):
        return max(0.0, min(1.0, value))
