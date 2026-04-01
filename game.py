import curses
import time
from board import Board
from player import InputHandler
from game_mode import GameMode, GameConfig
from sound_manager import SoundManager
from score_manager import ScoreManager


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


def show_pause_menu(stdscr):
    stdscr.clear()
    height, width = stdscr.getmaxyx()
    
    pause_lines = [
        "========== 游戏暂停 ==========",
        "",
        "按 [空格] 继续游戏",
        "按 [R] 重新开始",
        "按 [Esc] 返回主菜单",
        "",
        "========== 游戏暂停 ==========",
    ]
    
    draw_centered_lines(stdscr, pause_lines)
    stdscr.refresh()
    
    stdscr.nodelay(False)
    while True:
        key = stdscr.getch()
        if key == ord(' '):
            return 'resume'
        elif key == ord('r') or key == ord('R'):
            return 'restart'
        elif key == 27:
            return 'menu'


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
        "  Esc - 暂停游戏",
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
        "【挑战模式】",
        "  黑键从顶端下落",
        "点击底部黑键得分",
        "黑键逃脱游戏结束",
        "",
        "========== 游戏规则 ==========",
        "按任意键返回...",
    ]
    
    draw_centered_lines(stdscr, rules_lines)
    stdscr.refresh()
    
    stdscr.nodelay(False)
    stdscr.getch()


def show_leaderboard(stdscr):
    score_manager = ScoreManager()
    
    while True:
        stdscr.clear()
        height, width = stdscr.getmaxyx()
        
        menu_lines = [
            "========== 排行榜 ==========",
            "",
            "[1] 无限模式排行榜",
            "[2] 限时模式排行榜",
            "[3] 挑战模式排行榜",
            "[其他键] 返回",
        ]
        
        draw_centered_lines(stdscr, menu_lines)
        stdscr.refresh()
        
        stdscr.nodelay(False)
        key = stdscr.getch()
        
        if key == ord('1'):
            _display_leaderboard(stdscr, score_manager, "infinite")
        elif key == ord('2'):
            _display_leaderboard(stdscr, score_manager, "timed")
        elif key == ord('3'):
            _display_leaderboard(stdscr, score_manager, "challenge")
        else:
            return


def _display_leaderboard(stdscr, score_manager, mode):
    stdscr.clear()
    height, width = stdscr.getmaxyx()
    
    top_scores = score_manager.get_top_scores(mode, limit=10)
    
    if mode == "infinite":
        title = "无限模式排行榜"
        header = "排名  分数    日期"
    elif mode == "challenge":
        title = "挑战模式排行榜"
        header = "排名  分数    日期"
    else:
        title = "限时模式排行榜"
        header = "排名  分数    连击    日期"
    
    lines = [
        f"========== {title} ==========",
        "",
        header,
    ]
    
    if not top_scores:
        lines.append("")
        lines.append("暂无记录")
    else:
        for i, record in enumerate(top_scores, 1):
            if mode == "infinite" or mode == "challenge":
                line = f" {i:<4} {record.score:<6} {record.timestamp}"
            else:
                line = f" {i:<4} {record.score:<6} {record.max_combo:<6} {record.timestamp}"
            lines.append(line)
    
    lines.append("")
    lines.append(f"========== {title} ==========")
    lines.append("按任意键返回...")
    
    draw_centered_lines(stdscr, lines)
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
            "[3] 挑战模式",
            "[R] 规则说明",
            "[L] 排行榜",
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
        elif key == ord('3'):
            return GameMode.CHALLENGE
        elif key == ord('r') or key == ord('R'):
            show_rules(stdscr)
        elif key == ord('l') or key == ord('L'):
            show_leaderboard(stdscr)
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
    score_manager = ScoreManager()
    board = Board(game_mode, height, width, sound_manager)
    handler = InputHandler(stdscr)
    start_time = time.time()
    total_pause_time = 0
    pause_start_time = None
    
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
            board.time_remaining = max(0, GameConfig.TIMED_MODE_DURATION - int(time.time() - start_time - total_pause_time))
            if board.time_remaining <= 0:
                board.game_over = True
        
        if game_mode == GameMode.CHALLENGE:
            current_time = time.time()
            board.update_falling_tiles(current_time)
        
        key = handler.get_key()
        if key == ord('q') or key == ord('Q'):
            break
        
        if key == 27:
            pause_start_time = time.time()
            action = show_pause_menu(stdscr)
            pause_end_time = time.time()
            total_pause_time += (pause_end_time - pause_start_time)
            
            if action == 'resume':
                board.last_fall_time = time.time()
                continue
            elif action == 'restart':
                return True
            elif action == 'menu':
                return False
        
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
        score_manager.add_score(board.score, "infinite")
    elif game_mode == GameMode.TIMED:
        safe_addstr(stdscr, center_y, 0, "Time's Up!")
        safe_addstr(stdscr, center_y + 1, 0, f"Final Score: {board.score}")
        safe_addstr(stdscr, center_y + 2, 0, f"Max Combo: {board.max_combo}")
        safe_addstr(stdscr, center_y + 4, 0, "按 R 重新开始，按 Q 退出")
        score_manager.add_score(board.score, "timed", board.max_combo)
    elif game_mode == GameMode.CHALLENGE:
        safe_addstr(stdscr, center_y, 0, "Game Over!")
        safe_addstr(stdscr, center_y + 1, 0, f"Final Score: {board.score}")
        safe_addstr(stdscr, center_y + 2, 0, f"Speed Level: {board.get_speed_level()}")
        safe_addstr(stdscr, center_y + 4, 0, "按 R 重新开始，按 Q 退出")
        score_manager.add_score(board.score, "challenge")
    
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
        
        while True:
            should_restart = run_game(stdscr, game_mode)
            if not should_restart:
                break


if __name__ == "__main__":
    curses.wrapper(main)
