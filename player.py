import curses


class InputHandler:
    def __init__(self, stdscr, key_count=4):
        self.stdscr = stdscr
        self.key_count = key_count
        self._build_key_map()

    def _build_key_map(self):
        self.KEY_MAP = {}
        if self.key_count == 4:
            keys = ['d', 'f', 'j', 'k']
        else:
            keys = ['s', 'd', 'f', 'j', 'k', 'l']
        
        for i, key in enumerate(keys):
            self.KEY_MAP[ord(key)] = i
            self.KEY_MAP[ord(key.upper())] = i

    def get_key(self):
        self.stdscr.nodelay(True)
        try:
            key = self.stdscr.getch()
            return key
        except:
            return -1

    def key_to_column(self, key):
        return self.KEY_MAP.get(key, -1)
