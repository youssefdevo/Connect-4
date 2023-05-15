import random

# char for each player first player 'R' second 'B'  Red and Blue in GUI
computer = 'R'
Ai = 'B'


# evaluate used after last prediction (when reach max depth) we call this functions in evaluate find it below
# return score like final cost to this path after reach depth

def evaluate_vertical(board, i, j):
    value = 0
    ai = 0
    comp = 0
    empty = 0

    for k in range(0, 4):
        if board[i + k][j] == Ai:
            ai += 1
        elif board[i + k][j] == computer:
            comp += 1
        else:
            empty += 1

    if ai == 4:
        value = 60
    elif ai == 3 and empty == 1:
        value = 40
    elif ai == 2 and empty == 2:
        value = 20
    elif comp == 3 and empty == 1:
        value = -60

    return value


def evaluate_horizontal(board, i, j):
    value = 0
    ai = 0
    comp = 0
    empty = 0

    for k in range(0, 4):
        if j + k < 7 and board[i][j + k] == Ai:
            ai += 1
        elif j + k < 7 and i + k < 6 and board[i + k][j + k] == computer:
            comp += 1
        else:
            empty += 1

    if ai == 4:
        value = 60
    elif ai == 3 and empty == 1:
        value = 40
    elif ai == 2 and empty == 2:
        value = 20
    elif comp == 3 and empty == 1:
        value = -60

    return value


def evaluate_LeftDiagonal(board, i, j):
    value = 0
    ai = 0
    comp = 0
    empty = 0

    for k in range(0, 4):
        if board[i + k][j + k] == Ai:
            ai += 1
        elif board[i + k][j + k] == computer:
            comp += 1
        else:
            empty += 1

    if ai == 4:
        value = 60
    elif ai == 3 and empty == 1:
        value = 40
    elif ai == 2 and empty == 2:
        value = 20
    elif comp == 3 and empty == 1:
        value = -60

    return value


def evaluate_RightDiagonal(board, i, j):
    value = 0
    ai = 0
    comp = 0
    empty = 0

    for k in range(0, 4):
        if board[i + k][j - k] == Ai:
            ai += 1
        elif board[i + k][j - k] == computer:
            comp += 1
        else:
            empty += 1

    if ai == 4:
        value = 60
    elif ai == 3 and empty == 1:
        value = 40
    elif ai == 2 and empty == 2:
        value = 20
    elif comp == 3 and empty == 1:
        value = -60

    return value


# used after last prediction
def evaluate(board):
    value = 0
    for i in range(0, 6):
        for j in range(0, 7):
            if i + 3 < 6:
                value += evaluate_vertical(board, i, j)

            if j + 3 < 7:
                value += evaluate_horizontal(board, i, j)

            if i + 3 < 6 and j + 3 < 7:
                value += evaluate_LeftDiagonal(board, i, j)

            if i + 3 < 6 and j - 3 >= 0:
                value += evaluate_RightDiagonal(board, i, j)

    return value


# check if we reach tie or not
def Board_IS_Empty(board):
    for i in range(0, 6):
        for j in range(0, 7):
            if board[i][j] == '':
                return 1
    return 0


# check winner after each step in algorithm we call this functions Check_Winner 1-->computer win 2->>Ai Win  0 -> no
# winner
def Horizontal_Winner(board):
    for i in range(0, 6):
        for j in range(0, 4):
            if board[i][j] == board[i][j + 1] == board[i][j + 2] == board[i][j + 3] == computer:
                return 1
            if board[i][j] == board[i][j + 1] == board[i][j + 2] == board[i][j + 3] == Ai:
                return 2
    return 0


def Vertical_Winner(board):
    for i in range(0, 3):
        for j in range(0, 7):
            if board[i][j] == board[i + 1][j] == board[i + 2][i] == board[i + 3][j] == computer:
                return 1
            if board[i][j] == board[i + 1][j] == board[i + 2][j] == board[i + 3][j] == Ai:
                return 2
    return 0


def Left_Diagonal_Winner(board):
    for i in range(0, 3):
        for j in range(0, 4):
            if board[i][j] == board[i + 1][j + 1] == board[i + 2][j + 2] == board[i + 3][j + 3] == computer:
                return 1
            if board[i][j] == board[i + 1][j + 1] == board[i + 2][j + 2] == board[i + 1][j + 3] == Ai:
                return 2
    return 0


def Right_Diagonal_Winner(board):
    for i in range(0, 3):
        for j in range(3, 7):
            if board[i][j] == board[i + 1][j - 1] == board[i + 2][j - 2] == board[i + 3][j - 3] == computer:
                return 1
            if board[i][j] == board[i + 1][j - 1] == board[i + 2][j - 2] == board[i + 3][j - 3] == Ai:
                return 2
    return 0


# use after each step
def Check_Winner(board):

    winner = Vertical_Winner(board)
    if winner > 0:
        return winner
    winner = Horizontal_Winner(board)
    if winner > 0:
        return winner
    winner = Left_Diagonal_Winner(board)
    if winner > 0:
        return winner
    winner = Right_Diagonal_Winner(board)
    if winner > 0:
        return winner
    return winner


def GameOver(board):
    winner = Check_Winner(board)

    if winner > 0:
        return winner
    elif Board_IS_Empty(board):
        return 0

    return -1


def computer_turn(board, color):
    empty = []
    for i in range(0, 6):
        for j in range(0, 7):
            if board[5 - i][j] == '' and (i == 0 or board[6 - i][j] != ''):
                empty.append((5 - i, j))

    selected = random.choice(empty)
    board[selected[0]][selected[1]] = color
    return


def minimax(board, depth, maxi):
    if GameOver(board) != 0 or Board_IS_Empty(board) == 0:
        return 0

    cur = evaluate(board)

    if depth == 4:
        return cur

    if not Board_IS_Empty(board):
        return 0

    if maxi:
        best = - 1000000
        for i in range(0, 6):
            for j in range(0, 7):
                if board[5 - i][j] == '' and (i == 0 or board[6 - i][j] != ''):
                    board[5 - i][j] = Ai
                    best = max(best, minimax(board, depth + 1, not maxi))
                    board[5 - i][j] = ''

        return best

    else:
        best = 1000000
        for i in range(0, 6):
            for j in range(0, 7):
                if board[5 - i][j] == '' and (i == 0 or board[6 - i][j] != ''):
                    board[5 - i][j] = computer
                    best = min(best, minimax(board, depth + 1, not maxi))
                    board[5 - i][j] = ''
        return best


def findOptimalMove(board):
    bestValue = -100000
    bestMove = (-1, -1)
    for i in range(0, 6):
        for j in range(0, 7):

            if board[5 - i][j] == '' and (i == 0 or board[6 - i][j] != ''):
                board[5 - i][j] = Ai
                tempMove = minimax(board, 0, False)
                board[5 - i][j] = ''

                if tempMove > bestValue:
                    bestMove = (5 - i, j)
                    bestValue = tempMove

    b[bestMove[0]][bestMove[1]] = Ai


def print_grid(grid):
    for row in grid:
        for element in row:
            if element == '':
                print('_', end=' ')
            else:
                print(element, end=' ')
        print()  # Move to the next line after printing each row


b = [['', '', '', '', '', '', ''],
     ['', '', '', '', '', '', ''],
     ['', '', '', '', '', '', ''],
     ['', '', '', '', '', '', ''],
     ['', '', '', '', '', '', ''],
     ['', '', '', '', '', '', '']]

if __name__ == '__main__':
    for z in range(6 * 7):
        if GameOver(b) != 0 or not Board_IS_Empty(b):
            if Check_Winner(b) == 1:
                print("Computer is winner!!!")
            elif Check_Winner(b) == 2:
                print("AI is winner :)")
            elif Check_Winner(b) == 0:
                print("TIE")
            break
        print("Computer:")
        computer_turn(b, computer)
        print_grid(b)
        print()
        if GameOver(b) != 0 or not Board_IS_Empty(b):
            if Check_Winner(b) == 1:
                print("Computer is winner!!!")
            elif Check_Winner(b) == 2:
                print("AI is winner :)")
            elif Check_Winner(b) == 0:
                print("TIE")
            break
        print("AI:")
        findOptimalMove(b)
        print_grid(b)
        print()
