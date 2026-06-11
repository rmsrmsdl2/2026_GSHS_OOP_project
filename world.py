# -*- coding: utf-8 -*-

from biomorph import Biomorph
from config import (
    CHILDREN_PER_PARENT,
    GENERATION_INTERVAL,
    HISTORY_LIMIT,
    MAX_GENERATIONS,
    PARENT_COUNT,
    POPULATION_SIZE,
    PURE_MUTANT_COUNT,
    TRAIT_NAMES,
)
from environment import Environment


class World:
    def __init__(self):
        self.generation = 1
        self.frame_count = 0
        self.paused = False
        self.auto_generation = True
        self.started = False
        self.setup_mode = None
        self.finished = False
        self.environment = Environment()
        self.population = [Biomorph() for _ in range(POPULATION_SIZE)]
        self.selected_index = 0
        self.parent_ids = []
        self.message = "실험 방식을 선택하세요."
        self.history = []
        self.selection_history = []
        self.lineage = {}
        self.environment.update(self.generation)
        self._register_population(self.population, source="초기 개체")

    @property
    def selected(self):
        return self.population[self.selected_index]

    def update(self):
        if not self.started or self.paused or self.finished:
            return

        self.environment.update(self.generation)
        self.frame_count += 1

        if self.auto_generation and self.frame_count >= GENERATION_INTERVAL:
            self.next_generation()

    def select(self, index):
        if 0 <= index < len(self.population):
            self.selected_index = index
            biomorph = self.population[index]
            self.message = f"#{biomorph.id} 개체를 선택했습니다. 번식은 적합도 순위에 따라 진행됩니다."

    def next_generation(self):
        if not self.started or self.finished:
            return

        ranked = self.ranked_population()
        parents = [biomorph for biomorph, _score in ranked[:PARENT_COUNT]]
        self.parent_ids = [parent.id for parent in parents]
        self.record_selection(parents, ranked)

        children = []
        for parent in parents:
            for _ in range(CHILDREN_PER_PARENT):
                child = parent.breed_child()
                children.append(child)

        pure_mutants = [Biomorph() for _ in range(PURE_MUTANT_COUNT)]
        next_population = (children + pure_mutants)[:POPULATION_SIZE]

        self.generation += 1
        self.population = next_population
        self._register_population(children, source="선택 부모 자손")
        self._register_population(pure_mutants, source="쌩랜덤 돌연변이")
        self.selected_index = 0
        self.frame_count = 0
        self.environment.update(self.generation)
        self.record_history()

        if self.generation >= MAX_GENERATIONS:
            self.finished = True
            self.auto_generation = False
            self.message = "실험 종료: 최종 대표 개체의 부모 계보를 정리합니다."
        else:
            self.message = (
                f"{self.generation}세대: 선택 부모 {PARENT_COUNT}개체의 자손 "
                f"{PARENT_COUNT * CHILDREN_PER_PARENT}개체와 쌩랜덤 돌연변이 "
                f"{PURE_MUTANT_COUNT}개체가 생성되었습니다."
            )

    def ranked_population(self):
        return sorted(
            ((biomorph, self.fitness(biomorph)) for biomorph in self.population),
            key=lambda item: item[1],
            reverse=True,
        )

    def record_history(self):
        ranked = self.ranked_population()
        scores = [score for _biomorph, score in ranked]
        avg_fitness = sum(scores) / len(scores)
        best_fitness = scores[0]
        avg_error = sum(self.selection_error(biomorph) for biomorph in self.population) / len(self.population)
        avg_traits = {}

        for name in TRAIT_NAMES:
            avg_traits[name] = sum(biomorph.genome.traits[name] for biomorph in self.population) / len(self.population)

        self.history.append({
            "generation": self.generation,
            "avg_fitness": avg_fitness,
            "best_fitness": best_fitness,
            "avg_error": avg_error,
            "factors": self.environment.factors.copy(),
            "avg_traits": avg_traits,
        })
        self.history = self.history[-HISTORY_LIMIT:]

    def record_selection(self, parents, ranked):
        parent_scores = [self.fitness(parent) for parent in parents]
        avg_parent_traits = {}

        for name in TRAIT_NAMES:
            avg_parent_traits[name] = sum(parent.genome.traits[name] for parent in parents) / len(parents)

        self.selection_history.append({
            "generation": self.generation,
            "parent_ids": [parent.id for parent in parents],
            "avg_parent_fitness": sum(parent_scores) / len(parent_scores),
            "best_parent_fitness": parent_scores[0],
            "avg_parent_traits": avg_parent_traits,
            "representative_parent": ranked[0][0],
        })
        self.selection_history = self.selection_history[-HISTORY_LIMIT:]

    def selection_error(self, biomorph):
        error = 0.0
        for name in TRAIT_NAMES:
            trait = biomorph.genome.traits[name]
            target = self.environment.optimal_traits[name]
            error += (trait - target) ** 2
        return min(1.0, error / len(TRAIT_NAMES) * 5.0)

    def experiment_summary(self):
        ranked = self.ranked_population()
        representative, representative_score = ranked[0]
        first = self.history[0]
        last = self.history[-1]
        first_selection = self.selection_history[0] if self.selection_history else None
        last_selection = self.selection_history[-1] if self.selection_history else None
        trait_changes = []
        selected_trait_changes = []

        for name in TRAIT_NAMES:
            start = first["avg_traits"][name]
            end = last["avg_traits"][name]
            trait_changes.append((name, start, end, end - start))

            if first_selection and last_selection:
                selected_start = first_selection["avg_parent_traits"][name]
                selected_end = last_selection["avg_parent_traits"][name]
                selected_trait_changes.append((name, selected_start, selected_end, selected_end - selected_start))

        improved = sorted(trait_changes, key=lambda item: item[3], reverse=True)
        selected_improved = sorted(selected_trait_changes, key=lambda item: item[3], reverse=True)
        closest_traits = sorted(
            (
                (name, abs(representative.genome.traits[name] - self.environment.optimal_traits[name]))
                for name in TRAIT_NAMES
            ),
            key=lambda item: item[1],
        )

        return {
            "winner": representative,
            "winner_score": representative_score,
            "winner_error": self.selection_error(representative),
            "lineage": self.trace_lineage(representative.id),
            "last_selected_parent_ids": last_selection["parent_ids"] if last_selection else [],
            "initial_selected_fitness": first_selection["avg_parent_fitness"] if first_selection else first["avg_fitness"],
            "final_selected_fitness": last_selection["avg_parent_fitness"] if last_selection else last["avg_fitness"],
            "initial_avg_fitness": first["avg_fitness"],
            "final_avg_fitness": last["avg_fitness"],
            "initial_avg_error": first["avg_error"],
            "final_avg_error": last["avg_error"],
            "improved_traits": improved[:4],
            "selected_improved_traits": selected_improved[:4] if selected_improved else improved[:4],
            "closest_traits": closest_traits[:4],
        }

    def trace_lineage(self, biomorph_id):
        chain = []
        current_id = biomorph_id

        while current_id is not None and current_id in self.lineage:
            record = self.lineage[current_id]
            chain.append(record)
            current_id = record["parent_id"]

        return list(reversed(chain))

    def _register_population(self, biomorphs, source):
        for biomorph in biomorphs:
            self.lineage[biomorph.id] = {
                "id": biomorph.id,
                "parent_id": biomorph.parent_id,
                "generation": self.generation,
                "source": source,
                "fitness": self.fitness(biomorph),
                "traits": biomorph.genome.traits.copy(),
            }

    def randomize(self):
        self.population = [Biomorph() for _ in range(POPULATION_SIZE)]
        self.selected_index = 0
        self.generation = 1
        self.frame_count = 0
        self.parent_ids = []
        self.finished = False
        self.started = False
        self.setup_mode = None
        self.auto_generation = True
        self.environment = Environment()
        self.environment.update(self.generation)
        self.history = []
        self.selection_history = []
        self.lineage = {}
        self._register_population(self.population, source="초기 개체")
        self.message = "새 실험을 시작할 방식을 선택하세요."

    def choose_auto_start(self):
        self.setup_mode = "auto"
        self.started = True
        self.auto_generation = True
        self.environment.auto_mode = True
        self.history = []
        self.selection_history = []
        self.record_history()
        self.message = "자동 모드로 실험을 시작했습니다."

    def choose_manual_setup(self):
        self.setup_mode = "manual"
        self.started = False
        self.auto_generation = False
        self.environment.auto_mode = False
        self.message = "수동 모드: 초기 환경 변수를 조절한 뒤 실험을 시작하세요."

    def start_manual_experiment(self):
        self.setup_mode = "manual"
        self.started = True
        self.auto_generation = False
        self.environment.auto_mode = False
        self.history = []
        self.selection_history = []
        self.record_history()
        self.message = "수동 설정 환경으로 실험을 시작했습니다. N으로 세대를 진행하세요."

    def toggle_pause(self):
        if not self.started or self.finished:
            return
        self.paused = not self.paused
        self.message = "시뮬레이션을 일시정지했습니다." if self.paused else "시뮬레이션을 다시 진행합니다."

    def toggle_auto_generation(self):
        if not self.started or self.finished:
            return
        self.auto_generation = not self.auto_generation
        mode = "자동" if self.auto_generation else "수동"
        self.message = f"세대 교체 모드: {mode}"

    def trigger_disaster(self):
        if not self.started or self.finished:
            return
        self.environment.trigger_disaster()
        self.message = f"급격한 환경 변화 발생: {self.environment.disaster_name}"

    def fitness(self, biomorph):
        return self.environment.fitness(biomorph)
