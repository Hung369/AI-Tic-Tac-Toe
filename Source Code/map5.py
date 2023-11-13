import copy
import random
import sys
import pygame
import numpy as np

# Constants variables
width = 800
height = width
ROWS = 5
COLS = ROWS
CellSize = width // COLS

Line_width = 15
Circle_width = 15
Cross_width = 25
# radius for Circle
r = CellSize // 3
# Mock position for X character
Space = 30

# Colors for game feature
Background = (0, 0, 0)
Line_Color = (255, 255, 255)
Circle_Color = (0, 0, 250)
Cross_Color = (250, 0, 0)
theme = (0, 255, 0)
text_color = (255, 0, 255)

# initialize pygame object
pygame.init()
screen = pygame.display.set_mode((width, height))
img = pygame.image.load('./some_images/download.jpg')
pygame.display.set_caption('DRAGON-FANG')
pygame.display.set_icon(img)
font = pygame.font.Font('freesansbold.ttf', 52)


# Functions for operation
def CountSequence(a, number):
    count = 0
    oppo = 0
    for i in range(len(a)):
        if a[i] == number:
            count += 1
        elif a[i] != 0 and a[i] != number:
            oppo += 1

    if oppo == 1:
        if (a[0] != number and a[0] != 0) or (a[len(a) - 1] != number and a[len(a) - 1] != 0):
            return count
        else:
            count = 0
    elif oppo > 1:
        count = 0

    return count


def StateVal(human, machine):
    val = 0
    if human <= 1 and machine != 0:
        if machine == 4:
            val = -(10 ** 4)
        elif machine == 3:
            val = -(10 ** 3)
        elif machine == 2:
            val = -(10 ** 2)
        elif machine == 1:
            val = -(10 ** 1)
    if machine <= 1 and human != 0:
        if human == 4:
            val = (10 ** 4)
        elif human == 3:
            val = (10 ** 3)
        elif human == 2:
            val = (10 ** 2)
        elif human == 1:
            val = (10 ** 1)
    return val


def CalMainAndLines(pate):
    m_element = CountSequence(pate, 2)  # AI
    h_element = CountSequence(pate, 1)  # player
    value = 0
    if (m_element <= 1 and h_element != 0) or (m_element != 0 and h_element <= 1):
        if pate[0] == 1 or pate[0] == 2:
            value += StateVal(h_element, m_element)
        elif pate[len(pate) - 1] == 1 or pate[len(pate) - 1] == 2:
            value += StateVal(h_element, m_element)
        elif h_element == 0 or m_element == 0:
            value += StateVal(h_element, m_element)

    return value


def CountSubDiag(sub, number):
    count = 0
    oppo = 0
    for i in range(len(sub)):
        if sub[i] == number:
            count += 1
        elif sub[i] != 0 and sub[i] != number:
            oppo += 1

    if oppo >= 1:
        count = 0

    return count


# Classes
class Board:
    def __init__(self):
        self.squares = np.zeros((ROWS, COLS))
        self.empty_cells = self.squares
        self.marked_sqrs = 0

    def GG(self, show=False):
        for col in range(COLS):
            if (self.squares[0][col] == self.squares[1][col] == self.squares[2][col] == self.squares[3][col] != 0) or \
                    (self.squares[1][col] == self.squares[2][col] == self.squares[3][col] == self.squares[4][col] != 0):
                if show:
                    if self.squares[2][col] == 2:
                        color = Circle_Color
                    else:
                        color = Cross_Color
                    x = (col * CellSize + CellSize // 2, 20)
                    y = (col * CellSize + CellSize // 2, height - 20)
                    pygame.draw.line(screen, color, x, y, Line_width)
                return self.squares[2][col]

        for row in range(ROWS):
            if (self.squares[row][0] == self.squares[row][1] == self.squares[row][2] == self.squares[row][3] != 0) or \
                    (self.squares[row][1] == self.squares[row][2] == self.squares[row][3] == self.squares[row][4] != 0):
                if show:
                    if self.squares[row][2] == 2:
                        color = Circle_Color
                    else:
                        color = Cross_Color
                    x = (20, row * CellSize + CellSize // 2)
                    y = (width - 20, row * CellSize + CellSize // 2)
                    pygame.draw.line(screen, color, x, y, Line_width)
                return self.squares[row][2]

        # main desc diagonal
        if (self.squares[0][0] == self.squares[1][1] == self.squares[2][2] == self.squares[3][3] != 0) or (
                self.squares[1][1] == self.squares[2][2] == self.squares[3][3] == self.squares[4][4] != 0):
            if show:
                if self.squares[1][1] == 2:
                    color = Circle_Color
                else:
                    color = Cross_Color

                pygame.draw.line(screen, color, (20, 20), (width - 20, height - 20), Cross_width)
            return self.squares[1][1]

        # lower desc diagonal
        if self.squares[1][0] == self.squares[2][1] == self.squares[3][2] == self.squares[4][3] != 0:
            if show:
                if self.squares[1][0] == 2:
                    color = Circle_Color
                else:
                    color = Cross_Color

                pygame.draw.line(screen, color, (20, 20 + CellSize), (width - 20 - CellSize, height - 20), Cross_width)
            return self.squares[1][0]

        # upper desc diagonal
        if self.squares[0][1] == self.squares[1][2] == self.squares[2][3] == self.squares[3][4] != 0:
            if show:
                if self.squares[0][1] == 2:
                    color = Circle_Color
                else:
                    color = Cross_Color

                pygame.draw.line(screen, color, (20 + CellSize, 20), (width - 20, height - 20 - CellSize), Cross_width)
            return self.squares[0][1]

        # main asc diagonal
        if (self.squares[4][0] == self.squares[3][1] == self.squares[2][2] == self.squares[1][3] != 0) or (
                self.squares[3][1] == self.squares[2][2] == self.squares[1][3] == self.squares[0][4] != 0):
            if show:
                if self.squares[3][1] == 2:
                    color = Circle_Color
                else:
                    color = Cross_Color

                pygame.draw.line(screen, color, (20, height - 20), (width - 20, 20), Cross_width)
            return self.squares[3][1]

        # upper asc diagonal
        if self.squares[3][0] == self.squares[2][1] == self.squares[1][2] == self.squares[0][3] != 0:
            if show:
                if self.squares[3][0] == 2:
                    color = Circle_Color
                else:
                    color = Cross_Color

                pygame.draw.line(screen, color, (20, height - 20 - CellSize), (width - 20 - CellSize, 20), Cross_width)
            return self.squares[3][0]

        # lower asc diagonal
        if self.squares[4][1] == self.squares[3][2] == self.squares[2][3] == self.squares[1][4] != 0:
            if show:
                if self.squares[4][1] == 2:
                    color = Circle_Color
                else:
                    color = Cross_Color

                pygame.draw.line(screen, color, (20 + CellSize, height - 20), (width - 20, 20 + CellSize), Cross_width)
            return self.squares[4][1]

        return 0

    def MarkCell(self, row, col, player):
        self.squares[row][col] = player
        self.marked_sqrs += 1

    def EmptyCell(self, row, col):
        return self.squares[row][col] == 0

    def getEmptyCells(self):
        empty_cells = []
        for row in range(ROWS):
            for col in range(COLS):
                if self.EmptyCell(row, col):
                    empty_cells.append((row, col))

        return empty_cells

    def isBoardFull(self):
        return self.marked_sqrs == 25

    def getWinningPattern(self):
        WinPattern = list()
        # rows
        for row in range(ROWS):
            WinPattern.append([self.squares[row][0], self.squares[row][1], self.squares[row][2], self.squares[row][3],
                               self.squares[row][4]])

        # columns
        for col in range(COLS):
            WinPattern.append([self.squares[0][col], self.squares[1][col], self.squares[2][col], self.squares[3][col],
                               self.squares[4][col]])

        # sub increase diag
        WinPattern.append([self.squares[4][1], self.squares[3][2], self.squares[2][3], self.squares[1][4]])  # 11
        WinPattern.append([self.squares[3][0], self.squares[2][1], self.squares[1][2], self.squares[0][3]])  # 12

        # main increase diag
        WinPattern.append([self.squares[4][0], self.squares[3][1], self.squares[2][2], self.squares[1][3],
                           self.squares[0][4]])  # 13

        # sub decrease diag
        WinPattern.append([self.squares[0][1], self.squares[1][2], self.squares[2][3], self.squares[3][4]])  # 14
        WinPattern.append([self.squares[1][0], self.squares[2][1], self.squares[3][2], self.squares[4][3]])  # 15

        # main decrease diag
        WinPattern.append([self.squares[0][0], self.squares[1][1], self.squares[2][2], self.squares[3][3],
                           self.squares[4][4]])  # 16

        return WinPattern

    def Calculation(self):
        state = 0
        pat = self.getWinningPattern()
        for i in range(len(pat)):
            if i in range(10):  # rows and cols (0-9)
                state += CalMainAndLines(pat[i])
            elif i == 11 or i == 12 or i == 14 or i == 15:  # sub diagonals
                m = CountSubDiag(pat[i], 2)
                h = CountSubDiag(pat[i], 1)
                if (h == 0 and m != 0) or (m == 0 and h != 0):
                    state += StateVal(h, m)
            elif i == 13 or i == 16:  # main diagonals
                state += CalMainAndLines(pat[i])

        return state


class AI:
    def __init__(self, player=2):
        self.player = player
        self.best = None

    def minimax(self, depth, board, maximizing, alpha, beta):
        empty_cells = board.getEmptyCells()
        val = board.Calculation()
        best_move = None

        if len(empty_cells) > 24:
            if board.EmptyCell(2, 2):
                best_move = (2, 2)
                return None, best_move
            while True:
                x = random.choice([1, 2, 3])
                y = random.choice([1, 2, 3])
                if board.EmptyCell(x, y):
                    best_move = (x, y)
                    return None, best_move

        if depth == 0:
            case = board.GG()
            if case == 1:
                return (10 ** 4), None
            elif case == 2:
                return -1 * (10 ** 4), None
            elif board.isBoardFull():
                return 0, None
            else:
                return val, best_move

        if maximizing:
            for (row, col) in empty_cells:
                temp_board = copy.deepcopy(board)
                temp_board.MarkCell(row, col, 1)
                val = self.minimax(depth - 1, temp_board, False, alpha, beta)[0]
                if val > alpha:
                    alpha = val
                    best_move = (row, col)
                    self.best = best_move
                elif alpha >= beta:
                    break

            return alpha, best_move
        elif not maximizing:
            for (row, col) in empty_cells:
                temp_board = copy.deepcopy(board)
                temp_board.MarkCell(row, col, self.player)
                val = self.minimax(depth - 1, temp_board, True, alpha, beta)[0]
                if val < beta:
                    beta = val
                    best_move = (row, col)
                    self.best = best_move
                elif alpha >= beta:
                    break

            return beta, best_move

    # main function for AI
    def DragonFang(self, main_board):
        depth = 4
        value, move = self.minimax(depth, main_board, False, -10000, 10000)
        if move is None:
            move = self.best
        return move


# Create Board Lines function
def show_lines():
    screen.fill(Background)
    pygame.draw.line(screen, Line_Color, (CellSize, 0), (CellSize, height), Line_width)
    pygame.draw.line(screen, Line_Color, (width - CellSize, 0), (width - CellSize, height), Line_width)
    pygame.draw.line(screen, Line_Color, (CellSize * 2, 0), (CellSize * 2, height), Line_width)
    pygame.draw.line(screen, Line_Color, (width - CellSize * 2, 0), (width - CellSize * 2, height), Line_width)

    pygame.draw.line(screen, Line_Color, (0, CellSize), (width, CellSize), Line_width)
    pygame.draw.line(screen, Line_Color, (0, height - CellSize), (width, height - CellSize), Line_width)
    pygame.draw.line(screen, Line_Color, (0, CellSize * 2), (width, CellSize * 2), Line_width)
    pygame.draw.line(screen, Line_Color, (0, height - CellSize * 2), (width, height - CellSize * 2), Line_width)


class Game:
    def __init__(self, p):
        self.board = Board()
        self.ai = AI()
        self.player = p
        self.running = True
        show_lines()

    # Draw Functions
    def draw_fig(self, row, col):
        if self.player == 1:  # X player
            start = (col * CellSize + Space, row * CellSize + Space)
            end = (col * CellSize + CellSize - Space, row * CellSize + CellSize - Space)
            pygame.draw.line(screen, Cross_Color, start, end, Cross_width)
            start = (col * CellSize + Space, row * CellSize + CellSize - Space)
            end = (col * CellSize + CellSize - Space, row * CellSize + Space)
            pygame.draw.line(screen, Cross_Color, start, end, Cross_width)

        elif self.player == 2:  # Y player
            center = (col * CellSize + CellSize // 2, row * CellSize + CellSize // 2)
            pygame.draw.circle(screen, Circle_Color, center, r, Circle_width)

    # Game Operating Functions
    def make_move(self, row, col):
        self.board.MarkCell(row, col, self.player)
        self.draw_fig(row, col)
        self.next_turn()

    def next_turn(self):
        self.player = self.player % 2 + 1

    def isover(self):
        if self.board.GG(show=True) == 1:
            text = font.render('Player won the game', True, text_color, theme)
            textRect = text.get_rect()
            textRect.center = (width // 2, height // 2)
            screen.blit(text, textRect)
        elif self.board.GG(show=True) == 2:
            text = font.render('AI won the game', True, text_color, theme)
            textRect = text.get_rect()
            textRect.center = (width // 2, height // 2)
            screen.blit(text, textRect)
        elif self.board.isBoardFull():
            text = font.render('Draw', True, text_color, theme)
            textRect = text.get_rect()
            textRect.center = (width // 2, height // 2)
            screen.blit(text, textRect)
        return self.board.GG(show=False) != 0 or self.board.isBoardFull()

    def reset(self, p):
        self.__init__(p)


def Main():
    p = 1
    game = Game(p)
    board = game.board
    DF = game.ai

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                # press SPACE-BAR to rematch
                if event.key == pygame.K_SPACE:
                    game.reset(p)
                    board = game.board
                    DF = game.ai

            # Human player
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                row = pos[1] // CellSize
                col = pos[0] // CellSize

                if board.EmptyCell(row, col) and game.running:
                    game.make_move(row, col)
                    if game.isover():
                        game.running = False
                        p = p % 2 + 1

        # AI initial call
        if game.player == DF.player and game.running:
            pygame.display.update()
            row, col = DF.DragonFang(board)
            game.make_move(row, col)

            if game.isover():
                game.running = False
                p = p % 2 + 1

        pygame.display.update()


if __name__ == "__main__":
    Main()
