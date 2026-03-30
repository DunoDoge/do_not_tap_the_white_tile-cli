import random
from game_mode import GameMode, ComboLevel, GameConfig


class Board:
    WIDTH = 4
    HEIGHT = 8
    MIN_WIDTH = 20
    MIN_HEIGHT = 15

    def __init__(self, game_mode=GameMode.INFINITE, window_height=24, window_width=40, sound_manager=None):
        self.window_height = window_height
        self.window_width = window_width
        self.column_width = 4
        self.visible_rows = 8
        self.grid = [[0] * self.WIDTH for _ in range(self.HEIGHT)]
        self.score = 0
        self.game_over = False
        self.game_mode = game_mode
        self.combo = 0
        self.max_combo = 0
        self.combo_level = ComboLevel.NORMAL
        self.time_remaining = GameConfig.TIMED_MODE_DURATION
        self.show_mistake = False
        self.sound_manager = sound_manager
        self.calculate_layout()
        self._init_board()

    def calculate_layout(self):
        self.column_width = max(2, (self.window_width - 5) // 4)
        self.visible_rows = 8
        self.row_height = max(1, (self.window_height - 13) // 8)

    def is_window_too_small(self):
        is_too_small = self.window_width < self.MIN_WIDTH or self.window_height < self.MIN_HEIGHT
        if is_too_small:
            message = f"窗口太小！最小尺寸: {self.MIN_WIDTH}x{self.MIN_HEIGHT}，当前: {self.window_width}x{self.window_height}"
        else:
            message = ""
        return (is_too_small, message)

    def update_window_size(self, height, width):
        self.window_height = height
        self.window_width = width
        self.calculate_layout()

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
            if self.sound_manager:
                self.sound_manager.play_piano_note()
            return True
        else:
            if self.game_mode == GameMode.INFINITE:
                self.game_over = True
            else:
                self.combo = 0
                self.combo_level = ComboLevel.NORMAL
                self.score = max(0, self.score - GameConfig.MISTAKE_PENALTY)
                self.show_mistake = True
            if self.sound_manager:
                self.sound_manager.play_error_sound()
            return False

    def _shift_down(self):
        for row in range(self.HEIGHT - 1, 0, -1):
            for col in range(self.WIDTH):
                self.grid[row][col] = self.grid[row - 1][col]

    def render(self):
        lines = []
        cw = self.column_width
        rh = self.row_height
        border = "+" + "+".join(["-" * cw] * self.WIDTH) + "+"
        black_block = "█" * cw
        empty_block = " " * cw
        keys = ["D", "F", "J", "K"]

        lines.append(border)

        for row in range(self.HEIGHT):
            for _ in range(rh):
                row_display = []
                for col in range(self.WIDTH):
                    if self.grid[row][col] == 1:
                        row_display.append(black_block)
                    else:
                        row_display.append(empty_block)
                lines.append("|" + "|".join(row_display) + "|")
            lines.append(border)

        key_cells = [key.center(cw) for key in keys]
        lines.append("|" + "|".join(key_cells) + "|")
        lines.append(border)

        if self.game_mode == GameMode.INFINITE:
            lines.append(f"Score: {self.score}")
        else:
            combo_level_name = self.combo_level.name.capitalize()
            status = f"Score: {self.score}  Combo: {self.combo} ({combo_level_name})  Time: {self.time_remaining}s"
            if self.show_mistake:
                status += "  Oops!"
            lines.append(status)

        return "\n".join(lines)
