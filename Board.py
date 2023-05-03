from curses import start_color
import pygame

class Board:
    def __init__(self):
        self.board = [
        ['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR'],
        ['bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP'],
        ['', '', '', '', '', '', '', ''],
        ['', '', '', '', '', '', '', ''],
        ['', '', '', '', '', '', '', ''],
        ['', '', '', '', '', '', '', ''],
        ['wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP'],
        ['wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR']
        ]
        self.whiteQcastle = True
        self.whiteKcastle = True
        self.blackQcastle = True
        self.blackKcastle = True
    
    def move(self, move, color):
        if(len(move) != 4):
            return False
        
        start_col = ord(move[0]) - ord('a')
        start_row = 7 - (int(move[1]) - 1)
        end_col = ord(move[2]) - ord('a')
        end_row = 7- (int(move[3]) - 1)

        print(start_row)


        if str(start_col) not in '01234567' or str(end_col) not in '01234567' or str(start_row) not in '01234567' or str(end_row) not in '01234567':

            print("Invalid move. Please enter a move in the format 'e2e4'.")
            return False

        piece = self.board[start_row][start_col]

        if piece == '':
            print("choose a piece")
            return False


        print(self.board[start_row][start_col])
        if (self.board[start_row][start_col][0] != color):
            print("wrong color")
            return False

        

        self.board[start_row][start_col] = ''
        self.board[end_row][end_col] = piece
        
        return True
        
        


