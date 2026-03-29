import random
from game_mode import GameMode, ComboLevel, GameConfig


class Board:
    WIDTH = 4
    HEIGHT = 8

    def __init__(self, game_mode=GameMode.INFINITE):
        self.grid = [[0] * self.WIDTH for _ in range(self.HEIGHT)]
        self.score = 0
        self.game_over = False
        self.game_mode = game_mode
        self.combo = 0
        self.max_combo = 0
        self.combo_level = ComboLevel.NORMAL
        self.time_remaining = GameConfig.TIMED_MODE_DURATION
        self.show_mistake = False
        self._init_board()

    def _init_board(self):
        for row in range(self.HEIGHT):
            self._generate_row_at(row)

    def _generate_row_at(self, row):
        black_col = random.randint(0, self.WIDTH - 1)
        for col in range(self.WIDTH):
            self.grid[row][col] = 1 if col == black_col else 0

    def get_combo_level(self, combo_count):
        if combo_count >= 50:
            return ComboLevel.EXCELLENT
        elif combo_count >= 20:
            return ComboLevel.GREAT
        elif combo_count >= 10:
            return ComboLevel.GOOD
        else:
            return ComboLevel.NORMAL

    def get_score_multiplier(self):
        return GameConfig.COMBO_MULTIPLIERS[self.combo_level]

    def tap_column(self, col):
        if col < 0 or col >= self.WIDTH:
            return False

        bottom_row = self.HEIGHT - 1
        if self.grid[bottom_row][col] == 1:
            if self.game_mode == GameMode.INFINITE:
                self.score += 1
            else:
                self.combo += 1
                if self.combo > self.max_combo:
                    self.max_combo = self.combo
                self.combo_level = self.get_combo_level(self.combo)
                multiplier = self.get_score_multiplier()
                self.score += int(1 * multiplier)
            self.show_mistake = False
            self._shift_down()
            self._generate_row_at(0)
            return True
        else:
            if self.game_mode == GameMode.INFINITE:
                self.game_over = True
            else:
                self.combo = 0
                self.combo_level = ComboLevel.NORMAL
                self.score = max(0, self.score - GameConfig.MISTAKE_PENALTY)
                self.show_mistake = True
            return False

    def _shift_down(self):
        for row in range(self.HEIGHT - 1, 0, -1):
            for col in range(self.WIDTH):
                self.grid[row][col] = self.grid[row - 1][col]

    def render(self):
        lines = []
        lines.append("+" + "+".join(["----"] * self.WIDTH) + "+")
        
        for row in range(self.HEIGHT):
            row_display = []
            for col in range(self.WIDTH):
                if self.grid[row][col] == 1:
                    row_display.append("████")
                else:
                    row_display.append("    ")
            lines.append("|" + "|".join(row_display) + "|")
            lines.append("+" + "+".join(["----"] * self.WIDTH) + "+")
        
        lines.append("|" + "|".join([" D  ", " F  ", " J  ", " K  "]) + "|")
        lines.append("+" + "+".join(["----"] * self.WIDTH) + "+")
        
        if self.game_mode == GameMode.INFINITE:
            lines.append(f"\nScore: {self.score}")
        else:
            combo_level_name = self.combo_level.name.capitalize()
            status = f"\nScore: {self.score}  Combo: {self.combo} ({combo_level_name})  Time: {self.time_remaining}s"
            if self.show_mistake:
                status += "  Oops!"
            lines.append(status)
        
        return "\n".join(lines)
