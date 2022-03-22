# handles the board aspects
import pygame
from .constants import BLACK, ROWS, RED, SQUARE_SIZE, COLS, WHITE
from .piece import Piece

class Board:
    def __init__(self):
        self.board = []
        self.red_left = self.white_left = 12
        self.red_kings = self.white_kings = 0
        self.create_board()

    def draw_squares(self, win):
       win.fill(BLACK)
       for row in range(ROWS):
           for col in range(row % 2, ROWS, 2): # create the square patterns on the table
               pygame.draw.rect(win, RED, (row * SQUARE_SIZE, col * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    def move(self, piece, row, col):
        self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col]
        piece.move(row, col)

        if row == ROWS - 1 or row == 0:
            piece.make_king()
            if piece.color == WHITE:
                self.white_kings += 1
            else:
                self.red_kings += 1

    def get_piece(self, row, col):
        return self.board[row][col]

    def create_board(self):
        for row in range(ROWS):
            self.board.append([])# represent the elements of each line
            for col in range(COLS):
                if col % 2 == ((row + 1) % 2): # draw pieces only in the black squares
                    if row < 3:
                        self.board[row].append(Piece(row, col, WHITE))
                    elif row > 4:
                        self.board[row].append(Piece(row, col, RED))
                    else:
                        self.board[row].append(0) # blank space between pieces
                else:
                    self.board[row].append(0) # make sure that if there isn't a piece, there's a blank space

    def draw(self, win):
        self.draw_squares(win)
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece != 0:
                    piece.draw(win)

    def remove(self, pieces):
        for piece in pieces:
            self.board[piece.row][piece.col] = 0
            if piece != 0:
                if piece.color == RED:
                    self.red_left -= 1
                else:
                    self.white_left -= 1

    def winner(self):
        if self.red_left <= 0:
            return "White won the game !!!"
        elif self.white_left <= 0:
            return "Red has won the game !!!"
        return None

    def get_valid_moves(self, piece):
        moves = {} # store valid moves
        left = piece.col - 1
        right = piece.col + 1
        row = piece.row

        if piece.color == RED or piece.king:
            # se vermelho, a peca se move para cima, entao o movimento se inicia numa linha a frente da peca
            # checa ate onde deve se checar os movimentos, -3 significa que desejamos olhar apenas duas linhas acima da que partimos

            moves.update(self._traverse_left(row -1, max(row-3, -1), -1, piece.color, left))
            moves.update(self._traverse_right(row - 1, max(row - 3, -1), -1, piece.color, right))

        if piece.color == WHITE or piece.king:
            moves.update(self._traverse_left(row + 1, min(row + 3, ROWS), 1, piece.color, left))
            moves.update(self._traverse_right(row + 1, min(row + 3, ROWS), 1, piece.color, right))
        # Como moves é um dicionário, moves.update retorna um dicionário que se funde com moves, assim não tendo que fazer moves = ...
        return moves

    # these two functions check the diagonals, to see if there's a possible movement
    def _traverse_left(self, start, stop, step, color, left, skipped = []):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if left < 0: # if we look outside the table
                break

            current = self.board[r][left]
            if current == 0: # we found a blank space
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r, left)] = last + skipped
                else:
                    moves[(r, left)] = last

                if last: # preparing to take another piece,
                    if step == -1:
                        row = max(r-3, 0)
                    else:
                        row = min(r+3, ROWS)

                    moves.update(self._traverse_left(r+step, row, step, color, left-1, skipped=last))
                    moves.update(self._traverse_right(r+step, row, step, color, left+1, skipped=last))
                break

            # Se encontrarmos uma cor que seja a cor da peca que esta efetuando a jogada, nao podemos fazer este movimento
            elif current.color == color:
                break
            # Caso contrario, significa que e outra cor, significando que podemos fazer o movimento e comer a peca
            else:
                last = [current]

            left -= 1

        return moves

    def _traverse_right(self, start, stop, step, color, right, skipped = []):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if right >= COLS:  # Se estivermos olhando fora do tabuleiro
                break

            current = self.board[r][right]
            if current == 0:  # Significa que achamos um quadrado vazio
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r, right)] = last + skipped
                else:
                    moves[(r, right)] = last

                if last:  # Se preparando para comer mais de uma peca
                    if step == -1:
                        row = max(r - 3, 0)
                    else:
                        row = min(r + 3, ROWS)

                    moves.update(self._traverse_left(r + step, row, step, color, right - 1, skipped=last))
                    moves.update(self._traverse_right(r + step, row, step, color, right + 1, skipped=last))
                break
            elif current.color == color:
                break
            else:
                last = [current]

            right += 1

        return moves