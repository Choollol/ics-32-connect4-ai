# connect4_console_ai.py
#
# ICS 32 Winter 2022
# Project #2
#
# This executable module implements a console-only version of Connect Four.
# The second player is an AI player.

import connect4
import connect4_ui
import connect4_ui_ai


PLAYER_COLOR = connect4.RED


def run_console_ui() -> None:
    gameState = connect4_ui.make_new_game()

    print(connect4_ui.print_board(gameState), end="")

    game_ended = False

    while not game_ended:
        move_info = connect4_ui_ai.ai_move(gameState)

        try:
            gameState = connect4_ui.make_move(gameState, move_info)
        except connect4.GameOverError:
            game_ended = True

        if connect4.winner(gameState) != connect4.EMPTY:
            game_ended = True

        print(connect4_ui.print_board(gameState), end="")


if __name__ == '__main__':
    run_console_ui()
