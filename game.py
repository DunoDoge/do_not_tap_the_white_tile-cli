import curses
import time
from board import Board
from player import InputHandler
from game_mode import GameMode, GameConfig
from sound_manager import SoundManager


ASCII_TITLE = [
    "    ____               _  __     ______             ",
    "   / __ \\ ____   ____ ( )/ /_   /_  __/____ _ ____  ",
    "  / / / // __ \\ / __ \\|// __/    / /  / __ `// __ \\ ",
    " / /_/ // /_/ // / / / / /_     / /  / /_/ // /_/ / ",
    "/_____/ \\____//_/ /_/  \\__/    /_/   \\__,_// .___/  ",
    "                                          /_/       ",
    "    __   __             _       __ __     _  __           ______ _  __    ",
    "   / /_ / /_   ___     | |     / // /_   (_)/ /_ ___     /_  __/(_)/ /___ ",
    "  / __// __ \\ / _ \\    | | /| / // __ \\ / // __// _ \\     / /  / // // _ \\",
    " / /_ / / / //  __/    | |/ |/ // / / // // /_ /  __/    / /  / // //  __/",
    " \\__//_/ /_/ \\___/     |__/|__//_/ /_//_/ \\__/ \\___/    /_/  /_//_/ \\___/ ",
]


def get_centered_x(width, line_length):
    return max(0, (width - line_length) // 2)


def get_centered_y(height, total_lines):
    return max(0, (height - total_lines) // 2)


def draw_centered_lines(stdscr, lines, start_y=None):
    height, width = stdscr.getmaxyx()
    total_lines = len(lines)
    if start_y is None:
        start_y = get_centered_y(height, total_lines)
    
    for i, line in enumerate(lines):
        y = start_y + i
        if y < height:
            x = get_centered_x(width, len(line))
            max_len = width - x - 1
            if y == height - 1:
                max_len = width - x - 1
            try:
                display_line = line[:max_len] if len(line) > max_len else line
                stdscr.addstr(y, x, display_line)
            except curses.error:
                pass


def show_rules(stdscr):
    stdscr.clear()
    height, width = stdscr.getmaxyx()
    
    rules_lines = [
        "========== 游戏规则 ==========",
        "",
        "【基本操作】",
        "  D - 点击第一列",
        "  F - 点击第二列",
        "  J - 点击第三列",
        "  K - 点击第四列",
        "",
        "【无限模式】",
        " 点击黑块得分",
        "点错白块游戏结束",
        "",
        "【限时模式】",
        "  60秒限时挑战",
        "连击可获得加分倍率",
        "失误扣分并中断连击",
        "",
        "========== 游戏规则 ==========",
        "按任意键返回...",
    ]
    
    draw_centered_lines(stdscr, rules_lines)
    stdscr.refresh()
    
    stdscr.nodelay(False)
    stdscr.getch()


def select_mode(stdscr):
    curses.curs_set(0)
    
    while True:
        stdscr.clear()
        height, width = stdscr.getmaxyx()
        
        menu_lines = [
            "",
            "[1] 无限模式",
            "[2] 限时模式",
            "[R] 规则说明",
            "[Q] 退出游戏",
        ]
        
        all_lines = ASCII_TITLE + menu_lines
        total_lines = len(all_lines)
        start_y = get_centered_y(height, total_lines)
        
        draw_centered_lines(stdscr, ASCII_TITLE, start_y)
        draw_centered_lines(stdscr, menu_lines, start_y + len(ASCII_TITLE))
        
        stdscr.refresh()
        
        key = stdscr.getch()
        if key == ord('1'):
            return GameMode.INFINITE
        elif key == ord('2'):
            return GameMode.TIMED
        elif key == ord('r') or key == ord('R'):
            show_rules(stdscr)
        elif key == ord('q') or key == ord('Q'):
            return None


def safe_addstr(stdscr, y, x, text):
    try:
        height, width = stdscr.getmaxyx()
        lines = text.split('\n')
        for i, line in enumerate(lines):
            row = y + i
            if row < height:
                max_len = width - x - 1
                if row == height - 1:
                    max_len = width - x - 1
                stdscr.addstr(row, x, line[:max_len] if len(line) > max_len else line)
    except curses.error:
        pass


def run_game(stdscr, game_mode):
    height, width = stdscr.getmaxyx()
    sound_manager = SoundManager()
    board = Board(game_mode, height, width, sound_manager)
    handler = InputHandler(stdscr)
    start_time = time.time()
    
    while not board.game_over:
        height, width = stdscr.getmaxyx()
        is_too_small, small_message = board.is_window_too_small()
        
        stdscr.clear()
        if is_too_small:
            safe_addstr(stdscr, 0, 0, small_message)
        else:
            safe_addstr(stdscr, 0, 0, board.render())
        stdscr.refresh()
        
        if is_too_small:
            key = stdscr.getch()
            if key == ord('q') or key == ord('Q'):
                break
            if key == curses.KEY_RESIZE:
                height, width = stdscr.getmaxyx()
                board.update_window_size(height, width)
            time.sleep(0.02)
            continue
        
        if game_mode == GameMode.TIMED:
            board.time_remaining = max(0, GameConfig.TIMED_MODE_DURATION - int(time.time() - start_time))
            if board.time_remaining <= 0:
                board.game_over = True
        
        key = handler.get_key()
        if key == ord('q') or key == ord('Q'):
            break
        
        if key == curses.KEY_RESIZE:
            height, width = stdscr.getmaxyx()
            board.update_window_size(height, width)
            continue
        
        col = handler.key_to_column(key)
        if col != -1:
            board.tap_column(col)
        
        time.sleep(0.02)
    
    stdscr.clear()
    stdscr.refresh()
    
    height, width = stdscr.getmaxyx()
    center_y = height // 2 - 2
    
    if game_mode == GameMode.INFINITE:
        safe_addstr(stdscr, center_y, 0, "Game Over!")
        safe_addstr(stdscr, center_y + 1, 0, f"Final Score: {board.score}")
        safe_addstr(stdscr, center_y + 3, 0, "按 R 重新开始，按 Q 退出")
    else:
        safe_addstr(stdscr, center_y, 0, "Time's Up!")
        safe_addstr(stdscr, center_y + 1, 0, f"Final Score: {board.score}")
        safe_addstr(stdscr, center_y + 2, 0, f"Max Combo: {board.max_combo}")
        safe_addstr(stdscr, center_y + 4, 0, "按 R 重新开始，按 Q 退出")
    
    stdscr.nodelay(False)
    while True:
        key = stdscr.getch()
        if key == ord('r') or key == ord('R'):
            return True
        elif key == ord('q') or key == ord('Q'):
            return False


def main(stdscr):
    curses.curs_set(0)
    stdscr.clear()
    
    while True:
        game_mode = select_mode(stdscr)
        if game_mode is None:
            break
        
        if not run_game(stdscr, game_mode):
            break


if __name__ == "__main__":
    curses.wrapper(main)
