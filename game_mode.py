from enum import Enum


class GameMode(Enum):
    INFINITE = 1
    TIMED = 2


class ComboLevel(Enum):
    NORMAL = 1
    GOOD = 2
    GREAT = 3
    EXCELLENT = 4


class GameConfig:
    TIMED_MODE_DURATION = 60
    COMBO_THRESHOLDS = {10: ComboLevel.GOOD, 20: ComboLevel.GREAT, 50: ComboLevel.EXCELLENT}
    COMBO_MULTIPLIERS = {ComboLevel.NORMAL: 1, ComboLevel.GOOD: 1.5, ComboLevel.GREAT: 2, ComboLevel.EXCELLENT: 2.5}
    MISTAKE_PENALTY = 10
