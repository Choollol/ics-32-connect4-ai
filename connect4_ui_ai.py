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

DROP = 1
POP = 2

PLAYER_COLOR = connect4.RED
AI_COLOR = connect4.YELLOW

def is_move_valid(gameState: connect4.GameState, move: int, column: int) -> bool:
    if move == DROP:
        for i in range(connect4.rows(gameState) - 1, -1, -1):
            if gameState.board[column - 1][i] == connect4.EMPTY:
                return True
    elif move == POP:
        return gameState.board[column - 1][0] == gameState.turn

    return False

def get_single_score(winnerResult: int) -> int:
    if winnerResult == PLAYER_COLOR:
        return -1
    if winnerResult == AI_COLOR:
        return 1
    return 0

def get_win_score(gameState: connect4.GameState) -> int:
    return get_single_score(connect4.winner(gameState))

def simulate_move(gameState: connect4.GameState, move: int, movesRemaining: int, column: int) -> int:
    """Returns 'score' of chosen move"""
    
    if not is_move_valid(gameState, DROP, column):
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
    return total_score

# New function
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
    
    column = random.randint(1, connect4.columns(gameState)) 
    max_score = -100000000
    for col in range(1, connect4.columns(gameState) + 1):
        if not is_move_valid(gameState, DROP, col):
            continue
        score = simulate_move(gameState, DROP, 4, col)
        print(f"Column {col}'s score: {score}")
        if score > max_score:
            max_score = score
            column = col
    
    print(f"Chosen column: {column}")
    return (DROP, column)
    