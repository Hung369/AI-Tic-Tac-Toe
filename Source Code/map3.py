import copy
import random
import sys
import pygame
import numpy as np

# Constants variables
width = 800
height = 800
ROWS = 3
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


# Classes
class Board:
    def __init__(self):
        self.squares = np.zeros((ROWS, COLS))
        self.empty_cells = self.squares
        self.marked_sqrs = 0

    def GG(self, show=False):
        for col in range(COLS):
            if self.squares[0][col] == self.squares[1][col] == self.squares[2][col] != 0:
                if show:
                    if self.squares[0][col] == 2:
                        color = Circle_Color
                    else:
                        color = Cross_Color
                    x = (col * CellSize + CellSize // 2, 20)
                    y = (col * CellSize + CellSize // 2, height - 20)
                    pygame.draw.line(screen, color, x, y, Line_width)
                return self.squares[0][col]

        for row in range(ROWS):
            if self.squares[row][0] == self.squares[row][1] == self.squares[row][2] != 0:
                if show:
                    if self.squares[row][0] == 2:
                        color = Circle_Color
                    else:
                        color = Cross_Color
                    x = (20, row * CellSize + CellSize // 2)
                    y = (width - 20, row * CellSize + CellSize // 2)
                    pygame.draw.line(screen, color, x, y, Line_width)
                return self.squares[row][0]

        if self.squares[0][0] == self.squares[1][1] == self.squares[2][2] != 0:
            if show:
                if self.squares[1][1] == 2:
                    color = Circle_Color
                else:
                    color = Cross_Color

                pygame.draw.line(screen, color, (20, 20), (width - 20, height - 20), Cross_width)
            return self.squares[1][1]

        if self.squares[2][0] == self.squares[1][1] == self.squares[0][2] != 0:
            if show:
                if self.squares[1][1] == 2:
                    color = Circle_Color
                else:
                    color = Cross_Color

                pygame.draw.line(screen, color, (20, height - 20), (width - 20, 20), Cross_width)
            return self.squares[1][1]

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
        return self.marked_sqrs == 9


class AI:
    def __init__(self, player=2):
        self.player = player

    def minimax(self, board, maximizing):
        # case AI go first.
        if len(board.getEmptyCells()) == 9:
            row = random.choice([0, 1, 2])
            col = random.choice([0, 1, 2])
            move = (row, col)
            return None, move

        case = board.GG()
        if case == 1:
            return 1, None
        elif case == 2:
            return -1, None
        elif board.isBoardFull():
            return 0, None

        if maximizing:
            maxVal = -100
            best_move = None
            empty_cells = board.getEmptyCells()

            for (row, col) in empty_cells:
                temp_board = copy.deepcopy(board)
                temp_board.MarkCell(row, col, 1)
                val = self.minimax(temp_board, False)[0]
                if val > maxVal:
                    maxVal = val
                    best_move = (row, col)

            return maxVal, best_move

        elif not maximizing:
            minVal = 100
            best_move = None
            empty_cells = board.getEmptyCells()

            for (row, col) in empty_cells:
                temp_board = copy.deepcopy(board)
                temp_board.MarkCell(row, col, self.player)
                val = self.minimax(temp_board, True)[0]
                if val < minVal:
                    minVal = val
                    best_move = (row, col)

            return minVal, best_move

    # main function for AI
    def DragonFang(self, main_board):
        val, move = self.minimax(main_board, False)
        return move


# Create Board Lines function
def show_lines():
    screen.fill(Background)
    pygame.draw.line(screen, Line_Color, (CellSize, 0), (CellSize, height), Line_width)
    pygame.draw.line(screen, Line_Color, (width - CellSize, 0), (width - CellSize, height), Line_width)
    pygame.draw.line(screen, Line_Color, (0, CellSize), (width, CellSize), Line_width)
    pygame.draw.line(screen, Line_Color, (0, height - CellSize), (width, height - CellSize), Line_width)


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
