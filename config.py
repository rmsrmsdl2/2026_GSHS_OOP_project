SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 760
FPS = 60

INITIAL_POPULATION = 80
MIN_POPULATION = 28
MAX_POPULATION = 140

GENERATION_INTERVAL = 150

MUTATION_STRENGTH = 0.10
ELITE_RATE = 0.12
SURVIVAL_PRESSURE = 0.58
OFFSPRING_PER_PAIR = 2

TRAIT_NAMES = [
    "body_size",
    "branch_angle",
    "movement_speed",
    "energy_efficiency",
    "mutation_rate",
]

TRAIT_WEIGHTS = {
    "body_size": 1.0,
    "branch_angle": 1.2,
    "movement_speed": 1.0,
    "energy_efficiency": 1.3,
    "mutation_rate": 0.6,
}

TRAIT_LABELS = {
    "body_size": "Body Size",
    "branch_angle": "Branch Angle",
    "movement_speed": "Move Speed",
    "energy_efficiency": "Energy Efficiency",
    "mutation_rate": "Mutation Rate",
}
