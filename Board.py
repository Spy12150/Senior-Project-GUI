import pygame
import time

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
        self.enPassantable = None
        self.bqCastle = True
        self.bkCastle = True
        self.wqCastle = True
        self.wkCastle = True
        self.white_king_pos = (7, 4)
        self.black_king_pos = (0, 4)

    def is_valid_move(self, start_row, start_col, end_row, end_col, color):
        piece = self.board[start_row][start_col]
        if(piece[1] == "P"):
            if(color == "w"):
                if(self.board[end_row][end_col] == '' and start_row-end_row == 1 and start_col == end_col):
                    self.enPassantable = None
                    return True
                if(start_row == 7):
                    if(self.board[end_row][end_col] == '' and self.board[end_row+1][end_col] == '' and start_row-end_row == 2 and start_col == end_col and start_row == 6):
                        self.enPassantable = end_col
                        return True
                if(self.board[end_row][end_col] != '' and start_row-end_row == 1 and (start_col - 1 == end_col or start_col + 1 == end_col)):
                    self.enPassantable = None
                    return True
                if end_row == start_row - 1 and abs(end_col - start_col) == 1 and self.board[end_row][end_col] == '' and end_col == self.enPassantable:
                    self.enPassantable = None
                    self.board[start_row][end_col] = ''
                    return True
            elif(color == "b"):
                if(self.board[end_row][end_col] == '' and start_row-end_row == -1 and start_col == end_col):
                    self.enPassantable = None
                    return True
                if(start_row == 1):
                    if(self.board[end_row][end_col] == '' and self.board[end_row-1][end_col] == '' and start_row-end_row == -2 and start_col == end_col and start_row == 1):
                        self.enPassantable = end_col
                        return True
                if(self.board[end_row][end_col] != '' and start_row-end_row == -1 and (start_col - 1 == end_col or start_col + 1 == end_col)):
                    self.enPassantable = None
                    return True
                if end_row == start_row + 1 and abs(end_col - start_col) == 1 and self.board[end_row][end_col] == '' and end_col == self.enPassantable:
                    self.enPassantable = None
                    self.board[start_row][end_col] = ''
                    return True
            
            return False
            
        elif(piece[1] == "N"):
            
            if(abs(start_row-end_row) == 1 and abs(start_col-end_col) == 2):
                self.enPassantable = None
                return True
            elif(abs(start_row-end_row) == 2 and abs(start_col-end_col) == 1):
                self.enPassantable = None
                return True
            
            return False
        elif(piece[1] == "K"):

            

            if(abs(start_row-end_row) == 1 and abs(start_col-end_col) == 1):
                if(color == "w"):
                    self.white_king_pos = (end_row, end_col)
                else:
                    self.black_king_pos = (end_row, end_col)
                self.enPassantable = None
                
                return True
            elif(abs(start_row-end_row) == 0 and abs(start_col-end_col) == 1):
                if(color == "w"):
                    self.white_king_pos = (end_row, end_col)
                else:
                    self.black_king_pos = (end_row, end_col)
                self.enPassantable = None
                
                return True
            elif(abs(start_row-end_row) == 1 and abs(start_col-end_col) == 0):
                if(color == "w"):
                    self.white_king_pos = (end_row, end_col)
                else:
                    self.black_king_pos = (end_row, end_col)
                self.enPassantable = None
                
                return True
            elif(start_col - end_col == 2 and start_row == end_row and start_row == 7 and self.wqCastle and color == "w"):
                print("attempted castle Q")
                for i in [0, 1, 2]:
                    opponent_color = 'b' if color == 'w' else 'w'
                    if(self.board[start_row][start_col - i]!= '' and i!= 0):
                        return False
                    for row in range(8):
                        for col in range(8):
                            piece = self.board[row][col]
                            if piece != '' and piece[0] == opponent_color:
                                if self.is_valid_move(row, col, start_row, start_col - i, opponent_color):
                                    return False
                
                self.board[7][0] = ''
                self.board[7][3] = "wR"
                return True
            elif(end_col - start_col == 2 and start_row == end_row and start_row == 7 and self.wkCastle and color == "w"):
                print("attempted castle")
                for i in [0, 1, 2]:
                    if(self.board[start_row][start_col + i] != '' and i!= 0):
                        print("square occupied")
                        print(str(start_row) + str(start_col + i))
                        return False
                    opponent_color = 'b' if color == 'w' else 'w'
                    for row in range(8):
                        for col in range(8):
                            piece = self.board[row][col]
                            if piece != '' and piece[0] == opponent_color:
                                if self.is_valid_move(row, col, start_row, start_col + i, opponent_color):
                                    print("square attacked")
                                    return False
                
                self.board[7][7] = ''
                self.board[7][5] = "wR"
                return True
            elif(start_col - end_col == 2 and start_row == end_row and start_row == 0 and self.bqCastle and color == "b"):
                for i in [0, 1, 2]:
                    opponent_color = 'b' if color == 'w' else 'w'
                    if(self.board[start_row][start_col - i] != '' and i!= 0):
                        return False
                    for row in range(8):
                        for col in range(8):
                            piece = self.board[row][col]
                            if piece != '' and piece[0] == opponent_color:
                                if self.is_valid_move(row, col, start_row, start_col - i, opponent_color):
                                    return False
                
                self.board[0][0] = ''
                self.board[0][3] = "wR"
                return True
            elif(end_col - start_col == 2 and start_row == end_row and start_row == 0 and self.bkCastle and color == "b"):
                for i in [0, 1, 2]:
                    if(self.board[start_row][start_col + i] != '' and i!= 0):
                        return False
                    opponent_color = 'b' if color == 'w' else 'w'
                    for row in range(8):
                        for col in range(8):
                            piece = self.board[row][col]
                            if piece != '' and piece[0] == opponent_color:
                                if self.is_valid_move(row, col, start_row, start_col + i, opponent_color):
                                    return False
                
                self.board[0][7] = ''
                self.board[0][5] = "wR"
                return True

            else:
                return False
        elif(piece[1] == "R"):
            if(start_row-end_row == 0):

                if(end_col - start_col >= 0):
                    for i in range(0, (end_col - start_col)):
                        if(self.board[start_row][start_col + i] != '' and i != 0 and i != (end_col - start_col)):
                            return False
                else:
                    for i in range(0, (start_col - end_col)):
                        if(self.board[start_row][start_col - i] != '' and i != 0 and i != (start_col - end_col)):
                            return False
            elif(start_col-end_col == 0):
                if(end_row - start_row >= 0):
                    for i in range(0, (end_row - start_row)):
                        if(self.board[start_row + i][start_col] != '' and i != 0 and i != (end_row - start_row)):
                            return False
                else:
                    for i in range(0, (start_row - end_row)):
                        if(self.board[start_row - i][start_col] != '' and i != 0 and i != (start_row - end_row)):
                            return False
            else:
                return False
                
            self.enPassantable = None
            


            return True
        elif(piece[1] == "B"):
            diffrow = end_row - start_row
            diffcol = end_col - start_col
            if(abs(diffrow) != abs(diffcol)):
                return False
            elif(diffrow >= 0 and diffcol >=0):
                for i in range(0, (diffcol)):
                    if(self.board[start_row + i][start_col + i] != '' and i != 0 and i != abs(diffcol)):
                        return False
            elif(diffrow <= 0 and diffcol <=0):
                for i in range(0, abs(diffcol)):
                    if(self.board[start_row - i][start_col - i] != '' and i != 0 and i != abs(diffcol)):
                        return False
            elif(diffrow >= 0 and diffcol <=0):
                for i in range(0, abs(diffcol)):
                    if(self.board[start_row + i][start_col - i] != '' and i != 0 and i != abs(diffcol)):
                        return False
            elif(diffrow <= 0 and diffcol >=0):
                for i in range(0, abs(diffcol)):
                    if(self.board[start_row - i][start_col + i] != '' and i != 0 and i != abs(diffcol)):
                        return False
            self.enPassantable = None
            return True
        elif(piece[1] == "Q"):
            diffrow = end_row - start_row
            diffcol = end_col - start_col
            if(start_row-end_row == 0):

                if(end_col - start_col >= 0):
                    for i in range(0, (end_col - start_col)):
                        if(self.board[start_row][start_col + i] != '' and i != 0 and i != (end_col - start_col)):
                            return False
                else:
                    for i in range(0, (start_col - end_col)):
                        if(self.board[start_row][start_col - i] != '' and i != 0 and i != (start_col - end_col)):
                            return False
            elif(start_col-end_col == 0):
            
                if(end_row - start_row >= 0):
                    for i in range(0, (end_row - start_row)):
                        if(self.board[start_row + i][start_col] != '' and i != 0 and i != (end_row - start_row)):
                            return False
                else:
                    for i in range(0, (start_row - end_row)):
                        if(self.board[start_row - i][start_col] != '' and i != 0 and i != (start_row - end_row)):
                            return False
            
            elif(abs(diffrow) != abs(diffcol)):
                return False
            elif(diffrow >= 0 and diffcol >=0):
                for i in range(0, (diffcol)):
                    if(self.board[start_row + i][start_col + i] != '' and i != 0 and i != abs(diffcol)):
                        return False
            elif(diffrow <= 0 and diffcol <=0):
                for i in range(0, abs(diffcol)):
                    if(self.board[start_row - i][start_col - i] != '' and i != 0 and i != abs(diffcol)):
                        return False
            elif(diffrow >= 0 and diffcol <=0):
                for i in range(0, abs(diffcol)):
                    if(self.board[start_row + i][start_col - i] != '' and i != 0 and i != abs(diffcol)):
                        return False
            elif(diffrow <= 0 and diffcol >=0):
                for i in range(0, abs(diffcol)):
                    if(self.board[start_row - i][start_col + i] != '' and i != 0 and i != abs(diffcol)):
                        return False

            self.enPassantable = None
            return True
            
                
            

                
        else:
            return False

    def moveTest(self, move, color):
        if(len(move) != 4):
            
            return False
        
        start_col = ord(move[0]) - ord('a')
        start_row = 7 - (int(move[1]) - 1)
        end_col = ord(move[2]) - ord('a')
        end_row = 7- (int(move[3]) - 1)

        

        if(len(str(start_col) + str(start_row) + str(end_col) + str(end_row)) != 4):
            
            return False

        if str(start_col) not in '01234567' or str(end_col) not in '01234567' or str(start_row) not in '01234567' or str(end_row) not in '01234567':
            
            return False

        piece = self.board[start_row][start_col]

        if piece == '':
            
            return False
        if(self.board[end_row][end_col] != ''):
            if(self.board[end_row][end_col][0] == color):
                
                
                return False


        if (self.board[start_row][start_col][0] != color):
            
            return False

        if (self.is_valid_move(start_row, start_col, end_row, end_col, color)):
            swapped = self.board[end_row][end_col]
            self.board[start_row][start_col] = ''
            self.board[end_row][end_col] = piece
            if((piece == "wP" and end_row == 0) or (piece == "bP" and end_row == 7)):
                self.board[end_row][end_col] = piece[0] + "Q"
            if(self.is_king_in_check(color)):
                self.board[start_row][start_col] = piece
                self.board[end_row][end_col] = swapped
            
                
                return False
            self.board[start_row][start_col] = piece
            self.board[end_row][end_col] = swapped

        else: 
            
  
            return False
        
        

        
        
        return True
                

    def get_legal_moves(self, color):
        moves = []
        boardcopy = self  # create a copy of the board to avoid modifying the original
        for row in range(8):
            for col in range(8):
                piece = boardcopy.board[row][col]
                if piece != '' and piece[0] == color:
                    if piece[1] == "P" and color == "w":
                        movesopt = {(-1,-1), (-1,1), (-1,0), (-2,0)}
                        for movenums in movesopt:
                            end_row, end_col = row + movenums[0], col + movenums[1]
                            if end_row >= 0 and end_col >= 0:
                                move = chr(ord('a') + col) + str(8 - row)+ chr(ord('a') + end_col) + str(8 - end_row )
                                
                                
                                if boardcopy.moveTest(move, color):
                                    moves.append(move)
                                    boardcopy = self
                    elif piece[1] == "P" and color == "b":
                        movesopt = {(1,-1), (1,1), (1,0), (2,0)}
                        for movenums in movesopt:
                            end_row, end_col = row + movenums[0], col + movenums[1]
                            if end_row >= 0 and end_col >= 0:
                                move = chr(ord('a') + col) + str(8 - row)+ chr(ord('a') + end_col) + str(8 - end_row )
                                if boardcopy.moveTest(move, color):
                                    moves.append(move)
                                    boardcopy = self
                    elif piece[1] == "R" and piece[0] == color:
                        movesopt = []
                        for i in range(17):
                            movesopt.append((0,i - 8))
                        for i in range(17):
                            movesopt.append((i - 8,0))
                        for movenums in movesopt:
                            end_row, end_col = row + movenums[0], col + movenums[1]
                            if end_row >= 0 and end_col >= 0:
                                move = chr(ord('a') + col) + str(8 - row)+ chr(ord('a') + end_col) + str(8 - end_row )
                                if boardcopy.moveTest(move, color):
                                    moves.append(move)
                                    boardcopy = self
                    elif piece[1] == "N" and piece[0] == color:
                        movesopt = {(-2,-1), (-1,-2),(-2,1),(1,-2),(2,-1),(-1,2),(2,1),(2,1)}
                        for movenums in movesopt:
                            end_row, end_col = row + movenums[0], col + movenums[1]
                            if end_row >= 0 and end_col >= 0:
                                move = chr(ord('a') + col) + str(8 - row)+ chr(ord('a') + end_col) + str(8 - end_row )
                                
                                
                                if boardcopy.moveTest(move, color):
                                    moves.append(move)
                                    
                                    boardcopy = self
                    elif piece[1] == "K" and piece[0] == color:
                        movesopt = []
                        for i in [-1,0,1]:
                            for j in [-1, 0, 1]:
                                movesopt.append((i,j))
                        for movenums in movesopt:
                            end_row, end_col = row + movenums[0], col + movenums[1]
                            if end_row >= 0 and end_col >= 0:
                                move = chr(ord('a') + col) + str(8 - row)+ chr(ord('a') + end_col) + str(8 - end_row )
                                
                                if boardcopy.moveTest(move, color):
                                    moves.append(move)
                                    boardcopy = self
                    elif piece[1] == "B" and piece[0] == color:
                        movesopt = []
                        for i in range(17):
                            movesopt.append((i-8,i - 8))
                        for i in range(17):
                            movesopt.append((i - 8,-i + 8))
                        for movenums in movesopt:
                            end_row, end_col = row + movenums[0], col + movenums[1]
                            move = chr(ord('a') + col) + str(8 - row)+ chr(ord('a') + end_col) + str(8 - end_row )
                            
                            if boardcopy.moveTest(move, color):
                                    moves.append(move)
                                    boardcopy = self
                    elif piece[1] == "Q" and piece[0] == color:
                        movesopt = []
                        for i in range(17):
                            movesopt.append((0,i - 8))
                        for i in range(17):
                            movesopt.append((i - 8,0))
                        for i in range(17):
                            movesopt.append((i-8,i - 8))
                        for i in range(17):
                            movesopt.append((i - 8,-i + 8))
                        for movenums in movesopt:
                            move = chr(ord('a') + col) + str(8 - row)+ chr(ord('a') + col + movenums[1]) + str(8 - row + movenums[0])
                            
                            if boardcopy.moveTest(move, color):
                                    moves.append(move)
                                    boardcopy = self
                    boardcopy.board = self.board

        return moves
        

    
    def move(self, move, color, legalmoves):
        
        if(move in legalmoves):
            start_col = ord(move[0]) - ord('a')
            start_row = 7 - (int(move[1]) - 1)
            end_col = ord(move[2]) - ord('a')
            end_row = 7- (int(move[3]) - 1)
            piece = self.board[start_row][start_col]
            if(start_row == 7 and start_col == 0):
                self.wqCastle = False
            if(start_row == 7 and start_col == 7):
                self.wkCastle = False
            if(start_row == 0 and start_col == 0):
                self.bqCastle = False
            if(start_row == 0 and start_col == 7):
                self.bkCastle = False
            self.board[start_row][start_col] = ''
            self.board[end_row][end_col] = piece
            if(piece=="wK"):
                self.wkCastle = False
                self.wqCastle = False
            if(piece == "bK"):
                self.bkCastle = False
                self.bqCastle = False

            if(piece == "wP" and end_row == 0):
                self.board[end_row][end_col] = "wQ"
            if(piece == "bP" and end_row == 7):
                self.board[end_row][end_col] = "bQ"
            if(piece=="wK" and move == "e1g1"):
                self.board[7][7] = ''
                self.board[7][5] = "wR"
            if(piece=="wK" and move == "e1c1"):
                self.board[7][0] = ''
                self.board[7][3] = "wR"
            
            if(piece=="bK" and move == "e8g8"):
                self.board[0][7] = ''
                self.board[0][5] = "bR"
            if(piece=="bK" and move == "e8c8"):
                self.board[0][0] = ''
                self.board[0][3] = "bR"
            return True
        return False
        

    def toFen(self):
        fen = ""
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if(piece == "wP"):
                    fen += "P"
                elif(piece == "bP"):
                    fen += "p"
                elif(piece == "wQ"):
                    fen += "Q"
                elif(piece == "bQ"):
                    fen += "q"
                elif(piece == "wR"):
                    fen += "R"
                elif(piece == "bR"):
                    fen += "r"
                elif(piece == "wB"):
                    fen += "B"
                elif(piece == "wN"):
                    fen += "N"
                elif(piece == "bB"):
                    fen += "b"
                elif(piece == "bN"):
                    fen += "n"
                elif(piece == "wK"):
                    fen += "K"
                elif(piece == "bK"):
                    fen += "k"
                else:
                    if fen[-1].isnumeric() :
                        fen = fen[:-1] + str(int(fen[-1]) + 1)
                    else:
                        fen += "1"
            fen += "/"

        
        return fen[:-1]
        

    #     print("it gets here")
    #     print("it gets here")
    #     if(len(move) != 4):
            
    #         return False
        
    #     start_col = ord(move[0]) - ord('a')
    #     start_row = 7 - (int(move[1]) - 1)
    #     end_col = ord(move[2]) - ord('a')
    #     end_row = 7- (int(move[3]) - 1)

        

    #     if(len(str(start_col) + str(start_row) + str(end_col) + str(end_row)) != 4):
            
    #         return False

    #     if str(start_col) not in '01234567' or str(end_col) not in '01234567' or str(start_row) not in '01234567' or str(end_row) not in '01234567':
            
    #         return False

    #     piece = self.board[start_row][start_col]

    #     if piece == '':
            
    #         return False
    #     if(self.board[end_row][end_col] != ''):
    #         if(self.board[end_row][end_col][0] == color):
                
                
    #             return False


    #     if (self.board[start_row][start_col][0] != color):
            
    #         return False

    #     if (self.is_valid_move(start_row, start_col, end_row, end_col, color)):
    #         swapped = self.board[end_row][end_col]
    #         self.board[start_row][start_col] = ''
    #         self.board[end_row][end_col] = piece
    #         if((piece == "wP" and end_row == 0) or (piece == "bP" and end_row == 7)):
    #             self.board[end_row][end_col] = piece[0] + "Q"
    #         if(self.is_king_in_check(color)):
    #             self.board[start_row][start_col] = piece
    #             self.board[end_row][end_col] = swapped
                
    #             return False

    #     else: 
            
  
    #         return False
        
        

        
    #     print(move)
    #     return True



    # def get_king_pos(self, color):
    #     for row in range(len(self.board)):
    #         for col in range(len(self.board[row])):
    #             if self.board[row][col] == color + 'K':
    #                 return str(row) + str(col)
    # def is_king_in_check(self, color):
    #     king_pos = self.white_king_pos if color == 'w' else self.black_king_pos
    #     opponent_color = 'b' if color == 'w' else 'w'
    #     for row in range(8):
    #         for col in range(8):
    #             piece = self.board[row][col]
    #             if piece != '' and piece[0] == opponent_color:
                    
    #                 if self.is_valid_move(row, col, king_pos[0], king_pos[1], opponent_color):
    #                     print(str(row) + ", " + str(col))
    #                     print(str(king_pos[0]) + ", " + str(king_pos[1]))
    #                     print(piece)
    #                     return True
    #     return False

    # def get_squares_in_between(self, start_coord, end_coord):
        
    #     # Convert the algebraic notation to (x, y) coordinates
        

    #     start_x = int(start_coord[0])
    #     start_y = int(start_coord[1])
    #     end_x = int(end_coord[0])
    #     end_y = int(end_coord[1])

    #     # Calculate the direction of the movement
    #     dx = end_x - start_x
    #     dy = end_y - start_y

    #     # Check that the movement is diagonal, horizontal, or vertical
    #     if dx != 0 and dy != 0 and abs(dx) != abs(dy):
    #         return []

    #     # Calculate the step size for each coordinate
    #     step_x = 1 if dx > 0 else -1 if dx < 0 else 0
    #     step_y = 1 if dy > 0 else -1 if dy < 0 else 0

    #     # Calculate the number of steps to take in each coordinate
    #     num_steps = abs(dx) if dx != 0 else abs(dy)

    #     # Calculate the coordinates of the squares in between
    #     squares_in_between = []
    #     for i in range(1, num_steps):
    #         x = start_x + i * step_x
    #         y = start_y + i * step_y
    #         squares_in_between.append(str(x) + str(y))

    #     return squares_in_between

    # def is_checkmate(self,color):
    #     replacableboard = self.board
    #     if(not self.is_king_in_check(color)):
    #         print("no check")
    #         return False

    #     print("king is in")

    #     moves = self.get_legal_moves(color)

    #     for move in moves:
    #         start_col = ord(move[0]) - ord('a')
    #         start_row = 7 - (int(move[1]) - 1)
    #         end_col = ord(move[2]) - ord('a')
    #         end_row = 7- (int(move[3]) - 1)
    #         piece = self.board[start_row][start_col]
    #         swapped = self.board[end_row][end_col]
    #         self.board[start_row][start_col] = ''
    #         self.board[end_row][end_col] = piece
    #         if((piece == "wP" and end_row == 0) or (piece == "bP" and end_row == 7)):
    #             self.board[end_row][end_col] = piece[0] + "Q"
    #         if(self.is_king_in_check(color)):
    #             self.board[start_row][start_col] = piece
    #             self.board[end_row][end_col] = swapped
                
    #             return False   
    #     if(len(moves) != 0):
    #         return False
    #     return True
    # def is_stalemate(self, color, moves):
    #     if(self.is_king_in_check(color)):
    #         return False

        
    #     if (len(moves) == 0):
    #         return True

    #     pieces = []
    #     for row in range(8):
    #         for col in range(8):
    #             piece = self.board[row][col]
    #             if piece != '' and piece[1] != "K":
    #                 pieces.append("piece")
    #                 if(len(pieces) > 2):
    #                     return False
    #     if(len(pieces) == 0):
    #         return True
    #     if(len(pieces) == 1 and (pieces[0][1] == "N" or pieces[0][1] == "B")):
    #         return True
    #     if(len(pieces) == 1 and (pieces[0][1] == "N" and pieces[1][1] == "N")):
    #         return True

    #     return False
    
            
            
        