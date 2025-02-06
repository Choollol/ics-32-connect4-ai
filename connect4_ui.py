# connect4_ui.py
#
# ICS 32 
# Project #2
#
# This module contains utility functions that can be called from a console-
# based UI for a Connect Four game.
# 
# The signatures for the four required functions are provided.
# Hint: It would be useful to create helper functions.

import connect4

DROP = 1
POP = 2

EMPTY_SPACE_CHAR = "."
RED_SPACE_CHAR = "R"
YELLOW_SPACE_CHAR = "Y"

COLUMN_WIDTH_CHARS = 3

INVALID_DIMENSION = -1

def get_turn_from_int(inp: int) -> str:
    if inp == connect4.RED:
        return "RED"
    elif inp == connect4.YELLOW:
        return "YELLOW"

def get_board_dimension(inp: str, min_count: int, max_count: int) -> int:
    try:
        dimension = int(inp)
    except ValueError:
        print("Error: Invalid number entered.")
        return -1
    
    if dimension < min_count or dimension > max_count:
        print(f"Error: Please enter a dimension between {min_count} and {max_count} (inclusive).")
        return -1
    
    return dimension

def make_new_game() -> connect4.GameState:
    '''Asks the user for a board size, then creates a new game and return connect4.GameState'''
    columns = INVALID_DIMENSION
    while columns == INVALID_DIMENSION:
        columns = get_board_dimension(input("Columns: "), connect4.MIN_COLUMNS, connect4.MAX_COLUMNS)
    
    rows = INVALID_DIMENSION
    while rows == INVALID_DIMENSION:
        rows = get_board_dimension(input("Rows: "), connect4.MIN_ROWS, connect4.MAX_ROWS)
    
    gameState = connect4.new_game(columns, rows)
    return gameState

def print_board(gameState: connect4.GameState) -> str:
    '''Returns a string holding the contents of a game board, given a GameState'''
    board = ""
    for col in range(1, connect4.columns(gameState) + 1):
        board += f"{col:<{COLUMN_WIDTH_CHARS}}"
    board += "\n"
    
    for row in range(connect4.rows(gameState)):
        for col in range(connect4.columns(gameState)):
            space = gameState.board[col][row]
            if space == connect4.EMPTY:
                space_char = EMPTY_SPACE_CHAR
            elif space == connect4.RED:
                space_char = RED_SPACE_CHAR
            elif space == connect4.YELLOW:
                space_char = YELLOW_SPACE_CHAR
            board += f"{space_char:<{COLUMN_WIDTH_CHARS}}"
        board += "\n"
    
    board += "\n"
    if connect4.winner(gameState) == connect4.EMPTY:
        board += f"{get_turn_from_int(gameState.turn)}'s turn\n"    
    else:
        board += f"{get_turn_from_int(connect4.winner(gameState))} wins!"    
    
    return board


def choose_move(gameState: connect4.GameState) -> tuple[int, int]:
    '''
    Asks the user to choose a move, returning a tuple whose first element
    is DROP or POP and whose second element is a valid column number.
    '''
    is_move_input_valid = False
    while not is_move_input_valid:
        move_input = input("[D]rop or [P]op? ")
        
        is_move_input_valid = True
        if move_input == "d":
            move = DROP
        elif move_input == "p":
            move = POP
        else:
            print("Error: Invalid move")
            is_move_input_valid = False
    
    is_column_valid = False
    while not is_column_valid:
        is_column_valid = True
        try:
            column = int(input("Column: "))
        except ValueError:
            print("Error: Input is not a valid integer.")
            is_column_valid = False
            continue
        
        if column < 1 or column > connect4.columns(gameState):
            print("Error: Entered column is out of bounds.")
            is_column_valid = False
    
    return (move, column)


def make_move(gameState: connect4.GameState, move: tuple[int, int]) -> connect4.GameState:
    '''
    Makes the given move against the given state, returning the new state.
    For a valid move, return new state.
    
    Raise connect4.InvalidMoveError if invalid operation detected.
    Implement exception handler to catch this exceptions.
    If connect4.InvalidMoveError exception is caught, return original state inside the exception handler.
    '''
    column = move[1] - 1
    
    try:
        if move[0] == DROP:
            newGameState = connect4.drop(gameState, column)
            gameState = newGameState
        elif move[0] == POP:
            newGameState = connect4.pop(gameState, column)
            gameState = newGameState
        else:
            raise connect4.InvalidMoveError()
    except connect4.InvalidMoveError:
            print("Invalid move")
    
            
    return gameState
