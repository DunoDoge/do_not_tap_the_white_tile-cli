import curses
import time
from board import Board
from player import InputHandler
from game_mode import GameMode, GameConfig


def select_mode(stdscr):
    stdscr.clear()
    
    menu_lines = [
        "================================",
        "       别踩白块",
        "================================",
        "",
        "请选择游戏模式：",
        "",
        "[1] 无限模式",
        "    规则：点击黑块得分，失误即结束",
        "",
        "[2] 限时模式",
        "    规则：60秒限时，连击加分，失误扣10分",
        "",
        "按 1 或 2 选择模式...",
        "按 Q 退出游戏",
        "================================",
    ]
    
    for i, line in enumerate(menu_lines):
        try:
            height, width = stdscr.getmaxyx()
            if i < height:
                max_len = width - 1
                stdscr.addstr(i, 0, line[:max_len] if len(line) > max_len else line)
        except curses.error:
            pass
    
    stdscr.refresh()
    
    while True:
        key = stdscr.getch()
        if key == ord('1'):
            return GameMode.INFINITE
        elif key == ord('2'):
            return GameMode.TIMED
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
    board = Board(game_mode)
    handler = InputHandler(stdscr)
    start_time = time.time()
    
    while not board.game_over:
        stdscr.clear()
        safe_addstr(stdscr, 0, 0, board.render())
        stdscr.refresh()
        
        if game_mode == GameMode.TIMED:
            board.time_remaining = max(0, GameConfig.TIMED_MODE_DURATION - int(time.time() - start_time))
            if board.time_remaining <= 0:
                board.game_over = True
        
        key = handler.get_key()
        if key == ord('q') or key == ord('Q'):
            break
        
        col = handler.key_to_column(key)
        if col != -1:
            board.tap_column(col)
        
        time.sleep(0.02)
    
    stdscr.clear()
    safe_addstr(stdscr, 0, 0, board.render())
    
    info_row = board.HEIGHT * 2 + 4
    if game_mode == GameMode.INFINITE:
        safe_addstr(stdscr, info_row, 0, "Game Over!")
        safe_addstr(stdscr, info_row + 1, 0, f"Final Score: {board.score}")
        safe_addstr(stdscr, info_row + 3, 0, "按 R 重新开始，按 Q 退出")
    else:
        safe_addstr(stdscr, info_row, 0, "Time's Up!")
        safe_addstr(stdscr, info_row + 1, 0, f"Final Score: {board.score}")
        safe_addstr(stdscr, info_row + 2, 0, f"Max Combo: {board.max_combo}")
        safe_addstr(stdscr, info_row + 4, 0, "按 R 重新开始，按 Q 退出")
    
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
