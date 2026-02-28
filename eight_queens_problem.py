from typing import List, Tuple

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
    
    for i in range(len(board)):
        for j in range(len(board[i])):

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
    

def set_queens(board: List[List[int]], row: int = None, col: int = None) -> List[List[int]]:

    if row >= 8:
        return board, True

    for each_col in range(len(board[row])):
        board[row][each_col] = 1

        if check_placements(board):
            board, solved = set_queens(board, row = row + 1)
            if not solved:
                board[row][each_col] = 0
            else:
                return board, True
        else:
            board[row][each_col] = 0

    return board, False


solved_board = set_queens(
    board=chess_board,
    row=0, col=0
)

print(solved_board)



