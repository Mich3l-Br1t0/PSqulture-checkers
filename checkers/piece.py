# handles the piece aspects
import pygame
from .constants import SQUARE_SIZE, GREY, CROWN


class Piece:
    PADDING = 15 # distance of the checker to the square border
    OUTLINE = 2

    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.color = color
        self.king = False
        self.x = 0
        self.y = 0
        self.calc_pos()

    def calc_pos(self): # tells the position
        self.x = SQUARE_SIZE * self.col + SQUARE_SIZE // 2 # Important to draw the circle in the middle of the square
        self.y = SQUARE_SIZE * self.row + SQUARE_SIZE // 2

    def make_king(self):
        self.king = True

    def draw(self, win):
        radius = SQUARE_SIZE//2 - self.PADDING
        pygame.draw.circle(win, GREY, (self.x, self.y), radius + self.OUTLINE) # first we draw a big circle
        pygame.draw.circle(win, self.color, (self.x, self.y), radius) # then a less big than the previous, so we can have a border in the piece
        if self.king:
            win.blit(CROWN, (self.x - CROWN.get_width()//2, self.y - CROWN.get_width()//2))

    def move(self, row, col):
        self.row = row
        self.col = col
        self.calc_pos() # recalculate the position after movement

    def __repr__(self): # Ajudar a debugar o codigo
        return str(self.color)
