import sys

sys.path.append("../project2")

import connect4_console
import connect4_ui
import connect4

def new_suite(suite_name: str):
    print(f"\t>>> testing: {suite_name} <<<")

def main():
    new_suite("get_board_dimension()")
    assert connect4_ui.get_board_dimension("4", connect4.MIN_COLUMNS, connect4.MAX_COLUMNS) == 4
    assert connect4_ui.get_board_dimension("20", connect4.MIN_COLUMNS, connect4.MAX_COLUMNS) == 20
    assert connect4_ui.get_board_dimension("3", connect4.MIN_COLUMNS, connect4.MAX_COLUMNS) == -1
    assert connect4_ui.get_board_dimension("21", connect4.MIN_COLUMNS, connect4.MAX_COLUMNS) == -1
    
    new_suite("print_board()")
    print(connect4_ui.print_board(connect4.new_game(4, 4)))
    print(connect4_ui.print_board(connect4.new_game(14, 4)))

if __name__ == "__main__":
    main()