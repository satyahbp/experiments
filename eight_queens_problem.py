from typing import List, Tuple
from copy import deepcopy

chess_board = [
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
]


def check_left_to_right_diagonal(board: List[List[int]], position: Tuple) -> bool:
    
    # towards up:
    next_row = position[0] - 1
    next_column = position[1] - 1
    while next_row >= 0 and next_column >= 0:
        if board[next_row][next_column] == 1:
            return False
        next_row -= 1
        next_column -= 1
    
    # towards down
    next_row = position[0] + 1
    next_column = position[1] + 1
    while next_row < 8 and next_column < 8:
        if board[next_row][next_column] == 1:
            return False
        next_row += 1
        next_column += 1
    
    return True


def check_right_to_left_diagonal(board: List[List[int]], position: Tuple) -> bool:

    # towards up:
    next_row = position[0] - 1
    next_column = position[1] + 1
    while next_row >= 0 and next_column < 8:
        if board[next_row][next_column] == 1:
            return False
        next_row -= 1
        next_column += 1
    
    # towards down
    next_row = position[0] + 1
    next_column = position[1] - 1
    while next_row < 8 and next_column >= 0:
        if board[next_row][next_column] == 1:
            return False
        next_row += 1
        next_column -= 1
    
    return True


def check_placements(board: List[List[int]]) -> bool:
    
    for i in board:
        for j in board[i][j]:

            if board[i][j] == 0:
                continue
            
            # check row:
            for column in range(0, 8):
                if column == j:
                    continue
                if board[i][column] == 1:
                    return False
                
            # check column
            for row in range(0, 8):
                if row == i:
                    continue
                if board[row][j] == 1:
                    return False

            # check left to right diagonal
            if not check_left_to_right_diagonal(board, (i, j)):
                return False 
            
            # check right to left diagonal
            if not check_right_to_left_diagonal(board, (i, j)):
                return False
        
    return True
            



def check_8_queens(board: List[List[int]]) -> bool:
    queen_count = 0
    for i in board:
        for j in board[i]:
            if board[i][j] == 1:
                queen_count += 1

    if queen_count == 8:
        return True
    return False


def set_queens(board: List[List[int]], position: Tuple = None) -> List[List[int]]:

    local_board = deepcopy(board)

    # check base case
    if check_8_queens(local_board):
        return local_board
    
    i = position[0]
    j = position[1]
    while i >= position[0] and i < 8:
        while j >= position[1] and j < 8:
            local_board[i][j] = 1

            if check_placements(local_board):
                local_board = set_queens(local_board, (i + 1, j + 1))
            else:
                local_board[i][j] = 0
            
            j += 1
        i += 1

set_queens(
    board=chess_board,
    position=(0, 0)
)



