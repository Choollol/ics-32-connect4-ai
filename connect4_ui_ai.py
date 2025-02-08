# connect4_ui_ai.py
#
# ICS 32
# Project #2
#
# This module contains utility functions to implement the AI player
# for the console UI Connect Four game.
#

import connect4
import random
import multiprocessing
from collections import deque

DROP = 1
POP = 2

LOOKAHEAD_MOVE_THRESHOLDS = [(8, 5), (12, 4), (20, 3)]
DEFAULT_MAX_SCORE = -1000000000

LOOKAHEAD_EDGE_RADIUS = 2


def _find_bottom_empty_row_in_column(board: list[list[int]], column_number: int, row_count: int) -> int:
    for i in range(row_count - 1, -1, -1):
        if board[column_number][i] == connect4.EMPTY:
            return i

    return -1

def faster_drop(game_state: connect4.GameState, column_number: int, row_count: int) -> connect4.GameState:
    empty_row = _find_bottom_empty_row_in_column(
        game_state.board, column_number, row_count)

    if empty_row != -1:
        game_state.board[column_number][empty_row] = game_state.turn
        new_turn = _opposite_turn(game_state.turn)
        return connect4.GameState(game_state.board, turn=new_turn)
    else:
        raise connect4.InvalidMoveError()


def _opposite_turn(turn: int) -> int:
    if turn == connect4.RED:
        return connect4.YELLOW
    else:
        return connect4.RED


def _four_in_a_row(board: list[list[int]], col: int, row: int, coldelta: int, rowdelta: int, column_count: int, row_count: int) -> bool:
    start_cell = board[col][row]

    if start_cell == connect4.EMPTY:
        return False
    else:
        for i in range(1, 4):
            if not 1 <= col + coldelta * i < column_count \
                    or not 1 <= row + rowdelta * i < row_count \
                    or board[col + coldelta * i][row + rowdelta * i] != start_cell:
                return False
        return True


def _winning_sequence_begins_at(board: list[list[int]], col: int, row: int, column_count: int, row_count: int) -> bool:
    return _four_in_a_row(board, col, row, 0, 1, column_count, row_count) \
        or _four_in_a_row(board, col, row, 1, 1, column_count, row_count) \
        or _four_in_a_row(board, col, row, 1, 0, column_count, row_count) \
        or _four_in_a_row(board, col, row, 1, -1, column_count, row_count) \
        or _four_in_a_row(board, col, row, 0, -1, column_count, row_count) \
        or _four_in_a_row(board, col, row, -1, -1, column_count, row_count) \
        or _four_in_a_row(board, col, row, -1, 0, column_count, row_count) \
        or _four_in_a_row(board, col, row, -1, 1, column_count, row_count)


def faster_win_check(game_state: connect4.GameState, columnCount: int, rowCount: int):
    winner = connect4.EMPTY

    for col in range(columnCount):
        for row in range(rowCount):
            if game_state.board[col][row] != connect4.EMPTY and \
                    _winning_sequence_begins_at(game_state.board, col, row, columnCount, rowCount):
                if winner == connect4.EMPTY:
                    winner = game_state.board[col][row]
                elif winner != game_state.board[col][row]:
                    # This handles the rare case of popping a piece
                    # causing both players to have four in a row;
                    # in that case, the last player to make a move
                    # is the winner.
                    return _opposite_turn(game_state.turn)

    return winner


def is_move_valid(gameState: connect4.GameState, move: int, column: int) -> bool:
    """Column is 1-indexed"""
    if move == DROP:
        for i in range(connect4.rows(gameState) - 1, -1, -1):
            if gameState.board[column - 1][i] == connect4.EMPTY:
                return True
    elif move == POP:
        return gameState.board[column - 1][0] == gameState.turn

    return False


def get_single_score(winnerResult: int, ai_color, other_color) -> int:
    if winnerResult == other_color:
        return -1
    if winnerResult == ai_color:
        return 1
    return 0


def simulate_move(gameState: connect4.GameState, move: int, movesRemaining: int, column: int, lookaheadRange, ai_color, other_color) -> int:
    """Returns 'score' of chosen move"""

    column_count = connect4.columns(gameState)
    row_count = connect4.rows(gameState)

    total_score = 0

    queue: deque[tuple] = deque()

    queue.append((gameState, move, movesRemaining, column))

    while queue:
        front = queue.popleft()
        # if connect4.winner(front[0]) != connect4.EMPTY:
        if faster_win_check(front[0], column_count, row_count) != connect4.EMPTY:
            # total_score += get_win_score(front[0]) * front[2] ** front[2]
            total_score += get_single_score(connect4.winner(
                front[0]), ai_color, other_color) * front[2] ** 2
            continue
        if front[1] == DROP:
            if not is_move_valid(front[0], DROP, front[3]):
                continue
            #newGameState = connect4.drop(front[0], front[3] - 1)
            newGameState = faster_drop(front[0], front[3] - 1, row_count)
        if front[2] >= 1:
            for col in lookaheadRange:
                queue.append((newGameState, DROP, front[2] - 1, col))

    return total_score

    # Recursive
    """ if not is_move_valid(gameState, DROP, column):
        return 0

    if connect4.winner(gameState) != connect4.EMPTY or movesRemaining == 0:
        return get_win_score(gameState) * movesRemaining ** movesRemaining

    if move == DROP:
        newGameState = connect4.drop(gameState, column - 1)
        gameState = newGameState

    column = 1
    total_score = 0
    for col in range(1, connect4.columns(gameState) + 1):
        total_score += simulate_move(gameState, DROP, movesRemaining - 1, col)
    return total_score """


def simulate_move_helper(gameState: connect4.GameState, move: int, movesRemaining: int, column: int, lookaheadRange, scores, ai_color, other_color) -> None:
    scores[column] = simulate_move(
        gameState, move, movesRemaining, column, lookaheadRange, ai_color, other_color)


def multithreaded_move(gameState: connect4.GameState, lookaheadRange, lookahead_moves: int, lookaheadRangeLeft: int, lookaheadRangeRight: int, ai_color, other_color) -> tuple[int, int]:
    max_score = DEFAULT_MAX_SCORE

    # Start threads
    manager = multiprocessing.Manager()
    scores = manager.dict()
    processes: list[multiprocessing.Process] = []
    for col in lookaheadRange:
        if not is_move_valid(gameState, DROP, col):
            continue
        process = multiprocessing.Process(target=simulate_move_helper, args=(
            gameState, DROP, lookahead_moves, col, lookaheadRange, scores, ai_color, other_color))
        process.start()
        processes.append(process)

    # Wait for threads to finish
    for process in processes:
        process.join()

    # Find columns with max score
    possible_columns = [random.randint(
        lookaheadRangeLeft, lookaheadRangeRight)]
    found_nonzero_score = False
    for col, score in scores.items():
        # print(F"Column {col}'s score: {score}")
        if score != 0:
            found_nonzero_score = True
        if score > max_score:
            max_score = score
            possible_columns.clear()
            possible_columns.append(col)
        elif score == max_score:
            possible_columns.append(col)

    # Pick column
    possible_columns.sort()
    column = possible_columns[len(possible_columns) // 2]

    if not found_nonzero_score:
        column = random.randrange(lookaheadRangeLeft, lookaheadRangeRight + 1)

    return (DROP, column)


def singlethreaded_move(gameState: connect4.GameState, lookaheadRange, lookahead_moves: int, lookaheadRangeLeft: int, lookaheadRangeRight: int, ai_color, other_color) -> tuple[int, int]:
    max_score = DEFAULT_MAX_SCORE

    possible_columns = [random.randint(lookaheadRangeLeft + LOOKAHEAD_EDGE_RADIUS,
                                       lookaheadRangeRight - LOOKAHEAD_EDGE_RADIUS + 1)]
    found_nonzero_score = False
    for col in lookaheadRange:
        if not is_move_valid(gameState, DROP, col):
            continue
        score = simulate_move(
            gameState, DROP, lookahead_moves, col, lookaheadRange, ai_color, other_color)
        # print(f"Column {col}'s score: {score}")
        if score != 0:
            found_nonzero_score = True
        if score > max_score:
            max_score = score
            possible_columns.clear()
            possible_columns.append(col)
        elif score == max_score:
            possible_columns.append(col)

    column = possible_columns[len(possible_columns) // 2]

    if not found_nonzero_score:
        column = random.randrange(lookaheadRangeLeft + LOOKAHEAD_EDGE_RADIUS,
                                  lookaheadRangeRight - LOOKAHEAD_EDGE_RADIUS + 1)

    return (DROP, column)


def ai_move(gameState: connect4.GameState) -> tuple[int, int]:
    '''
    Asks the AI to choose a move, returning a tuple whose first element
    is DROP or POP and whose second element is a valid column number.
    Hint: helper functions would use useful here.
    '''

    """ move = random.randint(DROP, POP)
    column = random.randint(1, connect4.columns(gameState)) 
    return (move, column)
    """

    ai_color = gameState.turn
    other_color = _opposite_turn(ai_color)

    column_count = connect4.columns(gameState)

    # Get lookahead range
    lookaheadRangeLeft = column_count // 2 - LOOKAHEAD_EDGE_RADIUS
    lookaheadRangeRight = column_count // 2 + LOOKAHEAD_EDGE_RADIUS

    for col in range(1, column_count + 1):
        if gameState.board[col - 1][-1] != connect4.EMPTY:
            lookaheadRangeLeft = col - LOOKAHEAD_EDGE_RADIUS if col - \
                LOOKAHEAD_EDGE_RADIUS >= 1 else 1
            break

    for col in range(column_count, 0, -1):
        if gameState.board[col - 1][-1] != connect4.EMPTY:
            lookaheadRangeRight = col + LOOKAHEAD_EDGE_RADIUS if col + \
                LOOKAHEAD_EDGE_RADIUS <= column_count else column_count
            break

    lookaheadRange = range(lookaheadRangeLeft, lookaheadRangeRight + 1)

    # Get lookahead moves based on lookahead range
    for pair in LOOKAHEAD_MOVE_THRESHOLDS:
        if lookaheadRangeRight - lookaheadRangeLeft + 1 <= pair[0]:
            lookahead_moves = pair[1]
            break

    print(lookahead_moves)
    #lookahead_moves = 3
    return multithreaded_move(gameState, lookaheadRange, lookahead_moves, lookaheadRangeLeft, lookaheadRangeRight, ai_color, other_color)
    # return singlethreaded_move(gameState, lookaheadRange, lookahead_moves, lookaheadRangeLeft, lookaheadRangeRight, ai_color, other_color)
