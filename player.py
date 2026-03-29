import curses


class InputHandler:
    KEY_MAP = {
        ord('d'): 0, ord('D'): 0,
        ord('f'): 1, ord('F'): 1,
        ord('j'): 2, ord('J'): 2,
        ord('k'): 3, ord('K'): 3,
    }

    def __init__(self, stdscr):
        self.stdscr = stdscr

    def get_key(self):
        self.stdscr.nodelay(True)
        try:
            key = self.stdscr.getch()
            return key
        except:
            return -1

    def key_to_column(self, key):
        return self.KEY_MAP.get(key, -1)
