# -*- coding: utf-8 -*-

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 760
FPS = 60

PARENT_COUNT = 5
CHILDREN_PER_PARENT = 3
PURE_MUTANT_COUNT = 5
POPULATION_SIZE = PARENT_COUNT * CHILDREN_PER_PARENT + PURE_MUTANT_COUNT
GRID_COLUMNS = 5
GRID_ROWS = 4

GENERATION_INTERVAL = 360
MUTATION_STRENGTH = 0.13
MIN_SEGMENT_LENGTH = 4.5
HISTORY_LIMIT = 80
MAX_GENERATIONS = 50

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
    "recursion_depth": "분기 깊이",
    "mutation_rate": "돌연변이율",
}

FACTOR_NAMES = ["light", "humidity", "wind", "temperature"]

FACTOR_LABELS = {
    "light": "빛",
    "humidity": "습도",
    "wind": "바람",
    "temperature": "온도",
}

TRAIT_ENVIRONMENT_NOTES = {
    "trunk_length": "빛이 강할수록 중심 줄기가 긴 개체가 유리합니다.",
    "branch_angle": "빛 조건에 따라 유리한 가지 각도가 달라집니다.",
    "curvature": "바람이 강할수록 휘어지는 구조가 유리합니다.",
    "branch_ratio": "습도가 높을수록 가지가 길게 뻗는 구조가 유리합니다.",
    "body_width": "온도가 높으면 지나치게 두꺼운 몸통은 불리합니다.",
    "wing_span": "강한 바람에서는 넓은 날개가 불리합니다.",
    "antenna_angle": "습도 변화는 감각 기관의 각도 선택압에 영향을 줍니다.",
    "recursion_depth": "빛이 충분하면 복잡한 분기 구조가 유리합니다.",
    "mutation_rate": "환경이 불안정할수록 변이가 있는 집단이 유리합니다.",
}

TRAIT_COLORS = {
    "trunk_length": (116, 196, 255),
    "branch_angle": (255, 203, 92),
    "curvature": (153, 205, 183),
    "branch_ratio": (176, 151, 255),
    "body_width": (241, 128, 118),
    "wing_span": (113, 166, 255),
    "antenna_angle": (247, 164, 96),
    "recursion_depth": (126, 220, 144),
    "mutation_rate": (213, 137, 255),
}
