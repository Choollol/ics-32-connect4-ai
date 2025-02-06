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
    
    if movesRemaining == 0:
        return get_win_score(gameState)
    
    if move == DROP:
        try:
            newGameState = connect4.drop(gameState, column)
            gameState = newGameState
        except connect4.GameOverError:
            return get_win_score(gameState)
        except connect4.InvalidMoveError:
            return -1000
        except ValueError:
            return -1000
    
    column = 1
    max_score = 0
    for col in range(1, connect4.columns(gameState) + 1):
        score = simulate_move(gameState, DROP, movesRemaining - 1, col)
        if score > max_score:
            max_score = score
            column = col
    return get_win_score(gameState) + simulate_move(gameState, DROP, movesRemaining - 1, column)

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
    max_score = 0
    for col in range(1, connect4.columns(gameState) + 1):
        score = simulate_move(gameState, DROP, 5, col)
        print(f"Column {col}'s score: {score}")
        if score > max_score:
            max_score = score
            column = col
    
    print(f"Chosen column: {column}")
    return (DROP, column)
    