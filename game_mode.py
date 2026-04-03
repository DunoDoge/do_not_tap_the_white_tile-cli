from enum import Enum


class GameMode(Enum):
    INFINITE = 1
    TIMED = 2
    CHALLENGE = 3


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
    CHALLENGE_INITIAL_SPEED = 1.0
    CHALLENGE_SPEED_INCREMENT = 0.02
    CHALLENGE_MIN_SPEED = 0.1
    CHALLENGE_SPAWN_INTERVAL = 1.5


class GameSettings:
    KEY_MAPS = {
        4: ['D', 'F', 'J', 'K'],
        6: ['S', 'D', 'F', 'J', 'K', 'L'],
    }
    
    MIN_ROWS = 8
    MAX_ROWS = 12
    DEFAULT_KEY_COUNT = 4
    DEFAULT_ROW_COUNT = 8
    
    def __init__(self, key_count=None, row_count=None):
        self._key_count = key_count if key_count in self.KEY_MAPS else self.DEFAULT_KEY_COUNT
        self._row_count = row_count if row_count and self.MIN_ROWS <= row_count <= self.MAX_ROWS else self.DEFAULT_ROW_COUNT
    
    @property
    def key_count(self):
        return self._key_count
    
    @key_count.setter
    def key_count(self, value):
        if value in self.KEY_MAPS:
            self._key_count = value
    
    @property
    def row_count(self):
        return self._row_count
    
    @row_count.setter
    def row_count(self, value):
        if value and self.MIN_ROWS <= value <= self.MAX_ROWS:
            self._row_count = value
    
    def get_keys(self):
        return self.KEY_MAPS.get(self._key_count, self.KEY_MAPS[self.DEFAULT_KEY_COUNT])
    
    def get_key_ords(self):
        keys = self.get_keys()
        key_ords = {}
        for i, key in enumerate(keys):
            key_ords[ord(key.lower())] = i
            key_ords[ord(key.upper())] = i
        return key_ords
