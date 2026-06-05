SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 760
FIELD_WIDTH = 930
FPS = 60

INITIAL_POPULATION = 90
MIN_POPULATION = 35
MAX_POPULATION = 150
GENERATION_INTERVAL = 135

MUTATION_STRENGTH = 0.09
ELITE_RATE = 0.10
SURVIVAL_PRESSURE = 0.72
OFFSPRING_PER_PAIR = 2
HISTORY_LIMIT = 120

TRAIT_NAMES = [
    "body_size",
    "branch_angle",
    "movement_speed",
    "energy_efficiency",
    "mutation_rate",
]

TRAIT_LABELS = {
    "body_size": "Body Size",
    "branch_angle": "Branch Angle",
    "movement_speed": "Move Speed",
    "energy_efficiency": "Energy Efficiency",
    "mutation_rate": "Mutation Rate",
}

TRAIT_WEIGHTS = {
    "body_size": 1.0,
    "branch_angle": 1.2,
    "movement_speed": 1.0,
    "energy_efficiency": 1.3,
    "mutation_rate": 0.6,
}

TRAIT_COLORS = {
    "body_size": (238, 104, 96),
    "branch_angle": (91, 174, 255),
    "movement_speed": (252, 201, 83),
    "energy_efficiency": (92, 216, 139),
    "mutation_rate": (200, 125, 255),
}
