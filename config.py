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
    "trunk_length",
    "branch_angle",
    "curvature",
    "branch_ratio",
    "body_width",
    "wing_span",
    "antenna_angle",
    "recursion_depth",
    "mutation_rate",
]

TRAIT_LABELS = {
    "trunk_length": "몸통 길이",
    "branch_angle": "가지 각도",
    "curvature": "휘어짐",
    "branch_ratio": "가지 비율",
    "body_width": "몸통 폭",
    "wing_span": "날개 폭",
    "antenna_angle": "더듬이 각도",
    "recursion_depth": "재귀 깊이",
    "mutation_rate": "돌연변이율",
}