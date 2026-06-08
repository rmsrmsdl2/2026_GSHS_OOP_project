SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 760
FPS = 60

PARENT_COUNT = 5
CHILDREN_PER_PARENT = 3
POPULATION_SIZE = PARENT_COUNT * CHILDREN_PER_PARENT
GRID_COLUMNS = 5
GRID_ROWS = 3

GENERATION_INTERVAL = 360
MUTATION_STRENGTH = 0.13
MIN_SEGMENT_LENGTH = 4.5

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

FACTOR_NAMES = ["light", "humidity", "wind", "temperature"]

FACTOR_LABELS = {
    "light": "빛",
    "humidity": "습도",
    "wind": "바람",
    "temperature": "온도",
}

TRAIT_ENVIRONMENT_NOTES = {
    "trunk_length": "빛이 강할수록 긴 중심 줄기가 유리합니다.",
    "branch_angle": "빛이 강할수록 넓은 가지 각도가 유리합니다.",
    "curvature": "바람이 강할수록 휘어진 구조가 유리합니다.",
    "branch_ratio": "습도가 높을수록 가지가 길게 이어지는 구조가 유리합니다.",
    "body_width": "온도가 높을수록 지나치게 넓은 몸통은 불리합니다.",
    "wing_span": "바람이 약할 때는 큰 날개가 유리하지만 강풍에서는 불리합니다.",
    "antenna_angle": "습도가 높을수록 넓은 더듬이 각도가 유리합니다.",
    "recursion_depth": "빛이 강할수록 복잡한 가지 구조가 유리합니다.",
    "mutation_rate": "환경 차이가 클수록 높은 돌연변이율이 유리합니다.",
}
