import curses
import time
from board import Board
from player import InputHandler


def main(stdscr):
    curses.curs_set(0)
    stdscr.clear()
    
    board = Board()
    handler = InputHandler(stdscr)
    
    while not board.game_over:
        stdscr.clear()
        stdscr.addstr(0, 0, board.render())
        stdscr.refresh()
        
        key = handler.get_key()
        if key == ord('q') or key == ord('Q'):
            break
        
        col = handler.key_to_column(key)
        if col != -1:
            board.tap_column(col)
        
        time.sleep(0.02)
    
    stdscr.clear()
    stdscr.addstr(0, 0, board.render())
    stdscr.addstr(board.HEIGHT * 2 + 4, 0, "Game Over!")
    stdscr.addstr(board.HEIGHT * 2 + 5, 0, f"Final Score: {board.score}")
    stdscr.addstr(board.HEIGHT * 2 + 6, 0, "Press any key to exit...")
    stdscr.nodelay(False)
    stdscr.getch()


if __name__ == "__main__":
    curses.wrapper(main)
