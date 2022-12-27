import numpy as np
from datetime import datetime

def see_win(row):
    if (1 in row) and (2 in row) and (3 in row) and (4 in row):
        return True
    if (5 in row) and (6 in row) and (7 in row) and (8 in row):
        return True
    return False


# check legal moves assuming there is a move possible on this position.
def check_legal_moves(board, row, col, white):
    unique, count = np.unique(board, return_counts=True)
    occurrence = dict(zip(unique, count))
    results = []
    for x in range(4):
        if board[x, col] != 0:
            results.append(board[x, col])
        if board[row, x] != 0:
            results.append(board[row, x])
    if board[row + (1 if (row % 2) == 0 else -1), col + (1 if (col % 2) == 0 else -1)]:
        results.append(board[row + (1 if (row % 2) == 0 else -1), col + (1 if (col % 2) == 0 else -1)])
    moves = []
    unique = True
    if white:
        for x in range(1, 5):
            if x + 4 not in results and (unique or occurrence.get(x) is not None or occurrence.get(x+4) is not None):
                moves.append(x)
            if unique and occurrence.get(x) is None and occurrence.get(x + 4) is None:
                unique = False
    else:
        for x in range(5, 9):
            if x - 4 not in results and (unique or occurrence.get(x) is not None or occurrence.get(x-4) is not None):
                moves.append(x)
            if unique and occurrence.get(x) is None and occurrence.get(x - 4) is None:
                unique = False
    pieces = []
    for move in moves:
        if not(occurrence.get(move) is not None and occurrence.get(move) >= 2):
            pieces.append(move)
    return pieces


# check if someone wins
def check_win(board, solution):
    boardBytes = board.tobytes()
    if solution.get(boardBytes) is not None:
        return solution.get(boardBytes)
    win = False
    for pos in range(4):
        win = see_win(board[:, pos]) or win
        win = see_win(board[pos, :]) or win
    win = win or see_win(board[:2, :2])
    win = win or see_win(board[:2, 2:])
    win = win or see_win(board[2:, :2])
    win = win or see_win(board[2:, 2:])
    return win


# check if quadrant is empty
def quadrant_not_empty(board, row, col):
    not_empty = False
    not_empty = board[row, col] != 0 or not_empty
    not_empty = board[row + (1 if (row % 2) == 0 else -1), col] != 0 or not_empty
    not_empty = board[row, col + (1 if (col % 2) == 0 else -1)] != 0 or not_empty
    not_empty = board[row + (1 if (row % 2) == 0 else -1), col + (1 if (col % 2) == 0 else -1)] != 0 or not_empty
    return not_empty


# calculate winner
def solved_white(board, white, turn, solution):
    # base case
    if turn == 17:
        return False
    if turn == 1:
        board[0, 0] = 1
        return solved_white(board, not white, turn + 1, solution)
    moved = []
    for row in range(4):
        for col in range(4):
            if board[row, col] == 0:
                moves = check_legal_moves(board, row, col, white)
                for x in moves:
                    board[row, col] = x
                    if check_win(board, solution):
                        board[row, col] = 0
                        return white
                    board[row, col] = 0
    for row in range(4):
        for col in range(4):
            if board[row, col] == 0:
                moves = check_legal_moves(board, row, col, white)
                quadrant = (0 if (row < 2) == 0 else 1) + (0 if (col < 2) == 0 else 2)
                if [quadrant, moves] not in moved or quadrant_not_empty(board, row, col):
                    for x in moves:
                        board[row, col] = x
                        if solved_white(board, not white, turn + 1, solution) == white:
                            if turn < 7:
                                print('Turn =', turn)
                                print('White win? =', white)
                                print('Board =\n', board)
                                print('Time =', datetime.now())
                            solution[board.tobytes()] = white
                            board[row, col] = 0
                            return white
                        board[row, col] = 0
                    if len(moves) > 0:
                        moved.append([quadrant, moves])
    return not white


# create board
Quantik = np.zeros((4, 4))
solution_quantik = {}
Quantik[0, 0] = 1
Quantik[1, 1] = 6
print(Quantik)
if solved_white(Quantik, True, 3, solution_quantik):
    print('White wins!')
else:
    print('Black wins!')
