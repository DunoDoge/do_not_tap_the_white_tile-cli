import random


class Board:
    WIDTH = 4
    HEIGHT = 8

    def __init__(self):
        self.grid = [[0] * self.WIDTH for _ in range(self.HEIGHT)]
        self.score = 0
        self.game_over = False
        self._init_board()

    def _init_board(self):
        for row in range(self.HEIGHT):
            self._generate_row_at(row)

    def _generate_row_at(self, row):
        black_col = random.randint(0, self.WIDTH - 1)
        for col in range(self.WIDTH):
            self.grid[row][col] = 1 if col == black_col else 0

    def tap_column(self, col):
        if col < 0 or col >= self.WIDTH:
            return False

        bottom_row = self.HEIGHT - 1
        if self.grid[bottom_row][col] == 1:
            self.score += 1
            self._shift_down()
            self._generate_row_at(0)
            return True
        else:
            self.game_over = True
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
        lines.append(f"\nScore: {self.score}")
        
        return "\n".join(lines)
