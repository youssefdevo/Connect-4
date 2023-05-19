import math
import random
from tkinter import messagebox, ttk
import tkinter as tk

import combo as combo
import pygame
import sys

BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

pygame.init()

SQUARE = 80

c = 7
r = 6
difficulty_level = 0
width = c * SQUARE
height = (r + 2) * SQUARE

size = (width, height)

pygame.display.set_caption("Connect 4 Game")
myFont = pygame.font.SysFont("monospace", 60)
# boardx = [['0'] * c for _ in range(r)]

Empty = (2 * SQUARE)

Circle_Radius = int(SQUARE / 2 - 5)

screen = pygame.display.set_mode(size)

screen.fill(WHITE)


def draw_board(board):
    for c in range(7):
        for r in range(6):
            pygame.draw.rect(screen, BLACK, (c * SQUARE, r * SQUARE + Empty, SQUARE, SQUARE))
            pygame.draw.circle(screen, WHITE, (int(c * SQUARE + SQUARE / 2), int(r * SQUARE + Empty + SQUARE / 2)),
                               Circle_Radius)


def draw_circleAI(board, row, col):
    pygame.draw.circle(screen, BLUE, (int(col * SQUARE + SQUARE / 2), height - int(row * SQUARE + SQUARE / 2)),
                       Circle_Radius)
    pygame.display.update()


def draw_CircleComputer(board, row, col):
    pygame.draw.circle(screen, RED, (int(col * SQUARE + SQUARE / 2), height - int(row * SQUARE + SQUARE / 2)),
                       Circle_Radius)
    pygame.display.update()


# char for each player first player 'R' second 'B'  Red and Blue in GUI
computer = 'R'
Ai = 'B'


# evaluate used after last prediction (when reach max depth) we call this functions in evaluate find it below
# return score like final cost to this path after reach depth

def evaluate_vertical(board, i, j, player, player2):
    value = 0
    p1 = 0
    p2 = 0
    emptyCell = 0

    for k in range(0, 4):
        if board[i + k][j] == player:
            p1 += 1
        elif board[i + k][j] == player2:
            p2 += 1
        else:
            emptyCell += 1

    if p1 == 4:
        value = 100
    elif p2 == 4:
       value = -math.inf
    elif p1 == 3 and emptyCell == 1:
        value = 50
    elif p1 == 2 and emptyCell == 2:
        value = 5
    elif p2 == 3 and emptyCell == 1:
        value = -100

    return value


def evaluate_horizontal(board, i, j, player1, player2):
    value = 0
    p1 = 0
    p2 = 0
    emptyCell = 0

    for k in range(0, 4):
        if j + k < 7 and board[i][j + k] == player1:
            p1 += 1
        elif j + k < 7 and board[i][j + k] == player2:
            p2 += 1
        else:
            emptyCell += 1
    if p1 == 4:
        value = 100
    elif p2 == 4:
        value = -math.inf
    elif p1 == 3 and emptyCell == 1:
        value = 50
    elif p1 == 2 and emptyCell == 2:
        value = 5
    elif p2 == 3 and emptyCell == 1:
        value = -100

    return value


def evaluate_LeftDiagonal(board, i, j, player, player2):
    value = 0
    p1 = 0
    p2 = 0
    emptyCell = 0

    for k in range(0, 4):
        if board[i + k][j + k] == player:
            p1 += 1
        elif board[i + k][j + k] == player2:
            p2 += 1
        else:
            emptyCell += 1
    if p1 == 4:
        value = 100
    elif p2 == 4:
        value = -math.inf
    elif p1 == 3 and emptyCell == 1:
        value = 50
    elif p1 == 2 and emptyCell == 2:
        value = 5
    elif p2 == 3 and emptyCell == 1:
        value = -100
    return value


def evaluate_RightDiagonal(board, i, j, player, player2):
    value = 0
    p1 = 0
    p2 = 0
    emptyCell = 0

    for k in range(0, 4):
        if board[i + k][j - k] == player:
            p1 += 1
        elif board[i + k][j - k] == player2:
            p2 += 1
        else:
            emptyCell += 1
    if p1 == 4:
        value = 100
    elif p2 == 4:
        value = -math.inf
    elif p1 == 3 and emptyCell == 1:
        value = 50
    elif p1 == 2 and emptyCell == 2:
        value = 5
    elif p2 == 3 and emptyCell == 1:
        value = -100
    return value


# used after last prediction
def evaluate(board, player, player2):
    value = 0
    for i in range(0, 6):
        for j in range(0, 7):
            if i + 3 < 6:
                value += evaluate_vertical(board, i, j, player, player2)

            if j + 3 < 7:
                value += evaluate_horizontal(board, i, j, player, player2)

            if i + 3 < 6 and j + 3 < 7:
                value += evaluate_LeftDiagonal(board, i, j, player, player2)

            if i + 3 < 6 and j - 3 >= 0:
                value += evaluate_RightDiagonal(board, i, j, player, player2)

    return value


# check if we reach tie or not
def Board_IS_Empty(board):
    for i in range(0, 6):
        for j in range(0, 7):
            if board[i][j] == '':
                return 0
    return 1


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
            if board[i][j] == board[i + 1][j] == board[i + 2][j] == board[i + 3][j] == computer:
                return 1
            if board[i][j] == board[i + 1][j] == board[i + 2][j] == board[i + 3][j] == Ai:
                return 2
    return 0


def Left_Diagonal_Winner(board):
    for i in range(0, 3):
        for j in range(0, 4):
            if board[i][j] == board[i + 1][j + 1] == board[i + 2][j + 2] == board[i + 3][j + 3] == computer:
                return 1
            if board[i][j] == board[i + 1][j + 1] == board[i + 2][j + 2] == board[i + 3][j + 3] == Ai:
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
    win = Vertical_Winner(board)
    if win > 0:
        return win
    win = Horizontal_Winner(board)
    if win > 0:
        return win
    win = Left_Diagonal_Winner(board)
    if win > 0:
        return win
    win = Right_Diagonal_Winner(board)
    if win > 0:
        return win
    return win


def GameOver(board):
    win = Check_Winner(board)

    if win > 0:
        return win

    return -1


def computer_turn(board, color):
    emptyCell = []

    for j in range(0, 7):
        if board[0][j] == '':
            emptyCell.append(j)

    selected = random.choice(emptyCell)
    for i in range(0, 6):
        if board[5 - i][selected] == '':
            board[5 - i][selected] = color
            draw_CircleComputer(b, i, selected)
            pygame.display.update()

            break


def minimax(board, depth, maxi, player, player2):
    #
    # print("board = ")
    # print_grid(board)
    # print()
    # print()
    isFinished = GameOver(board)
    is_Empty = Board_IS_Empty(board)
    if isFinished > 0:
        if player == Ai:
            if isFinished == 1:
                return -math.inf, -1
            else:
                return math.inf, -1
        else:
            if isFinished == 1:
                return math.inf, -1
            else:
                return -math.inf, -1
    if is_Empty == 1:
        return 0, -1

    if depth == 0:
        return evaluate(board, player, player2), -1

    if maxi:
        best = - math.inf
        best_col = -1
        for j in range(0, 7):
            for i in range(0, 6):
                if board[5 - i][j] == '':
                    board[5 - i][j] = player
                    temp_val, temp_col = minimax(board, depth - 1, not maxi, player, player2)
                    if best == -math.inf:
                        best = temp_val
                        best_col = j
                    elif temp_val > best:
                        best_col = j
                        best = temp_val
                    board[5 - i][j] = ''
                    break

        return best, best_col

    else:
        best = math.inf
        best_col = -1
        for j in range(0, 7):
            for i in range(0, 6):
                if board[5 - i][j] == '':
                    board[5 - i][j] = player2
                    temp_val, temp_col = minimax(board, depth - 1, not maxi, player, player2)
                    if best == math.inf:
                        best = temp_val
                        best_col = j
                    elif temp_val < best:
                        best_col = j
                        best = temp_val
                    board[5 - i][j] = ''
                    break
        return best, best_col


def alpha_beta(board, depth, maxi, alpha, beta):
    """print("board = ")
    print_grid(board)
    print()
    print()"""
    isFinished = GameOver(board)
    is_Empty = Board_IS_Empty(board)
    if isFinished > 0:
        if isFinished == 1:
            return -math.inf, -1
        else:
            return math.inf, -1
    if is_Empty == 1:
        return 0, -1

    if depth == 0:
        return evaluate(board, Ai, computer), -1
    if maxi:
        best = - math.inf
        best_col = -1
        for j in range(0, 7):
            for i in range(0, 6):
                if board[5 - i][j] == '':
                    board[5 - i][j] = Ai
                    temp_val, temp_col = alpha_beta(board, depth - 1, not maxi, alpha, beta)
                    if best == -math.inf:
                        best = temp_val
                        best_col = j
                    elif temp_val > best:
                        best_col = j
                        best = temp_val
                        alpha = best
                    board[5 - i][j] = ''
                    break
            if beta <= alpha:
                break

        return best, best_col

    else:
        best = math.inf
        best_col = -1
        for j in range(0, 7):
            for i in range(0, 6):
                if board[5 - i][j] == '':
                    board[5 - i][j] = computer
                    temp_val, temp_col = alpha_beta(board, depth - 1, not maxi, alpha, beta)
                    if best == math.inf:
                        best = temp_val
                        best_col = j
                    elif temp_val < best:
                        best_col = j
                        best = temp_val
                        beta = best
                    board[5 - i][j] = ''
                    break
            if beta <= alpha:
                break
        return best, best_col


def findOptimalMove_MiniMax(board, player, player2,depth):
    # bestValue, bestMove_col = alpha_beta(board, 0, True, -math.inf, math.inf)
    bestValue, bestMove_col = minimax(board, depth, True, player, player2)
    for i in range(0, 6):
        if board[5 - i][bestMove_col] == '':
            b[5 - i][bestMove_col] = player
            if player == Ai:
                draw_circleAI(b, i, bestMove_col)
            else:
                draw_CircleComputer(b, i, bestMove_col)
            pygame.display.update()
            break


def findOptimalMove_AlphaBeta(board,depth):
    bestValue, bestMove_col = alpha_beta(board, depth, True, -math.inf, math.inf)
    for i in range(0, 6):
        if board[5 - i][bestMove_col] == '':
            b[5 - i][bestMove_col] = Ai
            draw_circleAI(b, i, bestMove_col)
            pygame.display.update()
            break


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

pygame.init()
draw_board(b)
pygame.display.update()


def go():
    turn = 1
    while 1:
        print(GameOver(b))
        print(Board_IS_Empty(b))
        if GameOver(b) > 0 or Board_IS_Empty(b) == 1:
            break
        clock = pygame.time.Clock()
        clock.tick(60)
        if turn % 2 == 0:
            print("Computer:")
            findOptimalMove_MiniMax(b, computer, Ai,3)
        else:
            print("AI:")
            findOptimalMove_AlphaBeta(b,5)
        print()
        print_grid(b)
        turn += 1

        print(GameOver(b))
        print(Board_IS_Empty(b))
    winner = GameOver(b)
    empty = Board_IS_Empty(b)
    if winner > 0 or empty == 1:
        if Check_Winner(b) == 1:
            print("Computer is winner!!!")
            message = myFont.render("Computer wins", 1, RED)
        elif Check_Winner(b) == 2:
            print("AI is winner :)")
            message = myFont.render("Agent wins", 1, BLUE)
        elif Board_IS_Empty(b) == 1:
            print("TIE")
            message = myFont.render("TIE", 1, BLACK)
    if winner==1:
       screen.blit(message,(40,4))
    else:
        screen.blit(message, (100, 5))
    pygame.display.update()
    pygame.time.wait(6000)


if __name__ == '__main__':
    go()
