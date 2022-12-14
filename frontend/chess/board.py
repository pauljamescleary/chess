"""
Draws the board and the "shelf" which is where the pieces will be placed initially
"""

import pygame
from chess.constants import *
from chess.piece import Piece
from chess.queen import Queen
from chess.rook import Rook
from chess.bishop import Bishop


class Board:

    """
    create board
    """
    FPS = 60

    def __init__(self, game_def):
        self.game_def = game_def
        self.ROWS = game_def['ROWS']
        self.COLS = game_def['COLS']
        self.board = []
        self.selected_piece = None
        self.correct = False
        self.wrong = False
        self.done = False
        self.setup_board()
        self.seconds = 0
        self.minutes = 0
        self.hours = 0
        self.frame_count = 0
        self.font_size = 15 #size of timer and labels
    """
    draw squares on board
    """

    def draw_squares(self, win):
        win.fill(GREEN)
        for row in range(self.ROWS):    # self.ROWS
            for col in range(row % 2, self.ROWS, 2):
                pygame.draw.rect(win, WHITE, (row * self.game_def['SQUARE_SIZE'],
                                 col * self.game_def['SQUARE_SIZE'], self.game_def['SQUARE_SIZE'], self.game_def['SQUARE_SIZE']))

    """
    draw shelf on board
    """

    def draw_shelf(self, win):
        pygame.draw.rect(win, BROWN, (0, self.game_def['HEIGHT'], self.game_def['WIDTH'], self.game_def['SHELF_SIZE']))

    """
    draw Start Menu on board
    """

    def draw_start_menu(self, win):
        pygame.draw.rect(
            win, BLACK, (0, self.game_def['HEIGHT'] + self.game_def['SHELF_SIZE'], self.game_def['WIDTH'], self.game_def['START_MENU_HEIGHT']))
        # pygame.draw.rect(win, BLACK, (0, HEIGHT + STARTMENUHEIGHT / 2, WIDTH, SQUARE_SIZE))
        # pygame.font.init()
        # FONT = pygame.font.SysFont('comicsans', 30)
        # LARGE_FONT = pygame.font.SysFont('comicsans', 40)
        # font = FONT.render("R - Reset | SPACE - Start Backtracking | N - Next Level", 1, WHITE)
        # pygame.font.init()
        # win.blit(font, 0, HEIGHT + STARTMENUHEIGHT / 2)
        # font2 = pygame.font.SysFont('comicsans', 30)
        pygame.font.init()
        font1 = pygame.font.SysFont('comicsans', self.font_size)

        img1 = font1.render('R - Reset | N - Next Level', True, WHITE)
        win.blit(img1, (0, self.game_def['HEIGHT'] + self.game_def['SHELF_SIZE'] + font1.get_height()))
        img2 = font1.render('SPACE - Check', True, WHITE)
        win.blit(img2, (0, self.game_def['HEIGHT'] + self.game_def['SHELF_SIZE']))

        # BUTTON_WIDTH = WIDTH // 3 - 10
        # BUTTON_PADDING = 7.5
        # pygame.draw.rect(win, BLACK, (0, HEIGHT + SQUARE_SIZE, WIDTH, START_MENU_HEIGHT))
        # pygame.draw.rect(win, GGREEN, (BUTTON_PADDING, HEIGHT + SQUARE_SIZE + BUTTON_PADDING, BUTTON_WIDTH, START_MENU_HEIGHT - 10))
        # pygame.draw.rect(win, RED, (2*BUTTON_PADDING + BUTTON_WIDTH, HEIGHT + SQUARE_SIZE + BUTTON_PADDING, BUTTON_WIDTH, START_MENU_HEIGHT - 10))
        # pygame.draw.rect(win, BLUE, (3*BUTTON_PADDING+ BUTTON_WIDTH*2, HEIGHT + SQUARE_SIZE + BUTTON_PADDING, BUTTON_WIDTH, START_MENU_HEIGHT - 10))

    """
    sets up the initial state of the board
    """
    def setup_board(self):
        for row in range(self.ROWS+1):
            self.board.append([])

        for row in range(self.ROWS+1):
            for col in range(self.COLS):
                self.board[row].append(0)

        for col in range(self.game_def['NUM_PIECES']):
            self.board[self.ROWS][col] = (globals()[self.game_def['PIECES'][col]](col, self.game_def))

    """
    prints a string representation of board state
    """

    def print_board(self):
        for row in range(self.ROWS+1):
            print(*self.board[row])

    """
    draw the board and pieces on the board
    """

    def draw(self, win, selected_piece):
        self.draw_squares(win)
        self.draw_shelf(win)
        self.draw_start_menu(win)
        self.draw_timer(win)
        for row in range(self.ROWS+1):
            for col in range(self.COLS):
                piece = self.board[row][col]
                if piece != 0 and piece is not selected_piece:
                    piece.draw(win)
                if piece is selected_piece:
                    piece.draw_while_moving(win)
        if self.done:
            self.draw_congrats(win)
        elif self.correct:
            self.draw_correct(win)
        elif self.wrong:
            self.draw_wrong(win)

    """
    returns piece in specified row and col
    """

    def get_piece(self, row, col):
        return self.board[row][col]

    """
    moves piece to specified row and col
    """

    def move(self, piece, row, col):
        self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col]
        piece.move(row, col)

    """
    Returns true if the shelf is empy, false if not
    """

    def is_shelf_empty(self):
        for col in range(self.COLS):
            if self.board[self.ROWS][col] != 0:
                return False

        return True

    """
    Checks every piece on the board to see if it is attacking another piece
    """

    def check(self):
        for row in range(self.ROWS):
            for col in range(self.COLS):
                piece = self.get_piece(row, col)
                if piece != 0:
                    result = piece.check_attacks(self.board, row, col)
                    if not result:
                        return False
        return True

    """
    Sets correct to True
    """

    def is_correct(self):
        self.correct = True

    """
    Draws "CORRECT!" on screen
    """

    def draw_correct(self, win):
        pygame.font.init()
        font = pygame.font.SysFont('comicsansbold', self.game_def['SQUARE_SIZE'])
        text = font.render('CORRECT!', True, GGREEN, BLACK)
        text_rect = text.get_rect(center=(self.game_def['WIDTH'] // 2, self.game_def['HEIGHT'] // 2))
        win.blit(text, text_rect)

    """
    Draws "CONGRATS!" on screen
    """
    def draw_congrats(self, win):
        pygame.font.init()
        font = pygame.font.SysFont('comicsansbold', self.game_def['SQUARE_SIZE'])
        text = font.render('CONGRATS!', True, GOLD, BLACK)
        text_rect = text.get_rect(center=(self.game_def['WIDTH'] // 2, self.game_def['HEIGHT'] // 2))
        win.blit(text, text_rect)

    """
    Set done to True
    """
    def is_done(self):
        self.done = True

    """
    Sets wrong to True
    """

    def is_wrong(self):
        self.wrong = True

    """
    Sets wrong to False
    """

    def is_not_wrong(self):
        self.wrong = False

    """
    Draw "TRY AGAIN!" on screen
    """

    def draw_wrong(self, win):
        pygame.font.init()
        font = pygame.font.SysFont('comicsansbold', self.game_def['SQUARE_SIZE'])
        text = font.render('TRY AGAIN!', True, RED, BLACK)
        text_rect = text.get_rect(center=(self.game_def['WIDTH'] // 2, self.game_def['HEIGHT'] // 2))
        win.blit(text, text_rect)

    def timer(self):
        self.frame_count += 1
        FPS = 60
        if FPS == self.frame_count:
            self.seconds += 1
            self.frame_count = 0
            if self.seconds == 60:
                self.seconds = 0
                self.minutes += 1
                if self.minutes == 60:
                    self.minutes = 0
                    self.hours += 1

    def draw_timer(self, win):
        pygame.font.init()
        font = pygame.font.SysFont('comicsans', self.font_size)
        time_text = font.render(
            "Time: " + str(self.hours) + ":" + str(self.minutes) + ":" + str(self.seconds), True, WHITE)
        time_rect = time_text.get_rect()
        time_rect.topleft = ((0, self.game_def['HEIGHT'] + self.game_def['SHELF_SIZE'] + 2 * font.get_height()))
        win.blit(time_text, time_rect)



