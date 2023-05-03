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

    def is_valid_move(self, start_row, start_col, end_row, end_col, color):
        piece = self.board[start_row][start_col]
        if(piece[1] == "P"):
            if(color == "w"):
                if(self.board[end_row][end_col] == '' and start_row-end_row == 1 and start_col == end_col):
                    return True
                if(self.board[end_row][end_col] == '' and start_row-end_row == 2 and start_col == end_col and start_row == 6):
                    return True
                if(self.board[end_row][end_col] != '' and start_row-end_row == 1 and (start_col - 1 == end_col or start_col + 1 == end_col)):
                    return True
            elif(color == "b"):
                if(self.board[end_row][end_col] == '' and start_row-end_row == -1 and start_col == end_col):
                    return True
                if(self.board[end_row][end_col] == '' and start_row-end_row == -2 and start_col == end_col and start_row == 1):
                    return True
                if(self.board[end_row][end_col] != '' and start_row-end_row == -1 and (start_col - 1 == end_col or start_col + 1 == end_col)):
                    return True
            else:
                return False
            
        if(piece[1] == "N"):
            print(abs(start_row-end_row))
            print(abs(start_col-end_col))

            if(abs(start_row-end_row) == 1 and abs(start_col-end_col) == 2):
                return True
            elif(abs(start_row-end_row) == 2 and abs(start_col-end_col) == 1):
                return True
            else:
                return False
        if(piece[1] == "K"):
            if(abs(start_row-end_row) == 1 and abs(start_col-end_col) == 1):
                return True
            elif(abs(start_row-end_row) == 0 and abs(start_col-end_col) == 1):
                return True
            elif(abs(start_row-end_row) == 1 and abs(start_col-end_col) == 0):
                return True
            else:
                return False
        if(piece[1] == "R"):
            print("rook move")
            if(start_row-end_row == 0):
                print("side side")
                print(end_col - start_col)
                for i in range(0, (end_col - start_col)):
                    if(self.board[start_row][start_col + i] != '' and i != 0):
                        return False
            elif(start_col-end_col == 0):
                print("up down")
                print(start_row - end_row)
                for i in range(0, (end_row - start_row)):
                    if(self.board[start_row - i][start_col] != '' and i != 0):
                        return False
            else:
                print("Invalid Rook")
                return False
            
            return True

                
        else:
            return True
                

        
        



    
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
        if(self.board[end_row][end_col] != ''):
            if(self.board[end_row][end_col][0] == color):
                print("U cant take ur own pieces")
                return False


        print(self.board[start_row][start_col])
        if (self.board[start_row][start_col][0] != color):
            print("wrong color")
            return False

        if (self.is_valid_move(start_row, start_col, end_row, end_col, color)):
            self.board[start_row][start_col] = ''
            self.board[end_row][end_col] = piece

        else: 
            print("invalid move")
            return False
        

        
        
        return True
    