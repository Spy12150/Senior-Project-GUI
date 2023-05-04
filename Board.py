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
        self.enPassantable = None
        self.white_king_pos = (7, 4)
        self.black_king_pos = (0, 4)

    def is_valid_move(self, start_row, start_col, end_row, end_col, color):
        piece = self.board[start_row][start_col]
        if(piece[1] == "P"):
            if(color == "w"):
                if(self.board[end_row][end_col] == '' and start_row-end_row == 1 and start_col == end_col):
                    return True
                if(self.board[end_row][end_col] == '' and self.board[end_row+1][end_col] == '' and start_row-end_row == 2 and start_col == end_col and start_row == 6):
                    self.enPassantable = end_col
                    return True
                if(self.board[end_row][end_col] != '' and start_row-end_row == 1 and (start_col - 1 == end_col or start_col + 1 == end_col)):
                    return True
                if end_row == start_row - 1 and abs(end_col - start_col) == 1 and self.board[end_row][end_col] == '' and end_col == self.enPassantable:
                    self.board[start_row][end_col] = ''
                    return True
            elif(color == "b"):
                if(self.board[end_row][end_col] == '' and start_row-end_row == -1 and start_col == end_col):
                    return True
                if(self.board[end_row][end_col] == '' and self.board[end_row-1][end_col] == '' and start_row-end_row == -2 and start_col == end_col and start_row == 1):
                    self.enPassantable = end_col
                    return True
                if(self.board[end_row][end_col] != '' and start_row-end_row == -1 and (start_col - 1 == end_col or start_col + 1 == end_col)):
                    return True
                if end_row == start_row + 1 and abs(end_col - start_col) == 1 and self.board[end_row][end_col] == '' and end_col == self.enPassantable:
                    self.board[start_row][end_col] = ''
                    return True
            
            return False
            
        elif(piece[1] == "N"):

            if(abs(start_row-end_row) == 1 and abs(start_col-end_col) == 2):
                return True
            elif(abs(start_row-end_row) == 2 and abs(start_col-end_col) == 1):
                return True
            
            return False
        elif(piece[1] == "K"):
            if(abs(start_row-end_row) == 1 and abs(start_col-end_col) == 1):
                if(color == "w"):
                    self.white_king_pos = (end_row, end_col)
                else:
                    self.black_king_pos = (end_row, end_col)
                return True
            elif(abs(start_row-end_row) == 0 and abs(start_col-end_col) == 1):
                if(color == "w"):
                    self.white_king_pos = (end_row, end_col)
                else:
                    self.black_king_pos = (end_row, end_col)
                return True
            elif(abs(start_row-end_row) == 1 and abs(start_col-end_col) == 0):
                if(color == "w"):
                    self.white_king_pos = (end_row, end_col)
                else:
                    self.black_king_pos = (end_row, end_col)
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
                print("up down")
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
            if((piece == "wP" and end_row == 0) or (piece == "bP" and end_row == 7)):
                self.board[end_row][end_col] = piece[0] + "Q"
            if(self.is_king_in_check(color)):
                self.board[start_row][start_col] = piece
                self.board[end_row][end_col] = ''
                print("Cannot move here, king is in check")
                return False

        else: 
            print("invalid move")
            return False
        
        

        
        
        return True



    def get_king_pos(self, color):
        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                if self.board[row][col] == color + 'K':
                    return str(row) + str(col)
    def is_king_in_check(self, color):
        king_pos = self.white_king_pos if color == 'w' else self.black_king_pos
        opponent_color = 'b' if color == 'w' else 'w'
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece != '' and piece[0] == opponent_color:
                    if self.is_valid_move(row, col, king_pos[0], king_pos[1], opponent_color):
                        return True
        return False

    def get_squares_in_between(start_coord, end_coord):
        
        # Convert the algebraic notation to (x, y) coordinates
        

        start_x = start_coord[0]
        start_y = start_coord[1]
        end_x = end_coord[0]
        end_y = end_coord[1]

        # Calculate the direction of the movement
        dx = end_x - start_x
        dy = end_y - start_y

        # Check that the movement is diagonal, horizontal, or vertical
        if dx != 0 and dy != 0 and abs(dx) != abs(dy):
            return []

        # Calculate the step size for each coordinate
        step_x = 1 if dx > 0 else -1 if dx < 0 else 0
        step_y = 1 if dy > 0 else -1 if dy < 0 else 0

        # Calculate the number of steps to take in each coordinate
        num_steps = abs(dx) if dx != 0 else abs(dy)

        # Calculate the coordinates of the squares in between
        squares_in_between = []
        for i in range(1, num_steps):
            x = start_x + i * step_x
            y = start_y + i * step_y
            squares_in_between.append(str(x) + str(y))

        return squares_in_between

    def is_checkmate(self,color):
        if(not self.is_king_in_check(color)):
            print("not in check")
            return False

        king_pos = self.white_king_pos if color == 'b' else self.black_king_pos
        opponent_color = 'w' if color == 'w' else 'b'
        checking_piece = ''
        checkingpieces = 0
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece != '' and piece[0] == opponent_color:
                    
                    if self.is_valid_move(row, col, king_pos[0], king_pos[1], opponent_color):
                        checking_piece = (str(row) + str(col))
                        print(checking_piece)
                        checkingpieces += 1
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece != '' and piece[0] == opponent_color:
                    if self.is_valid_move(row, col, int(checking_piece[0]), int(checking_piece[1]), opponent_color):
                        print(str(row) + str(col) + "can take")
                       
                        return False
        for row in range(8):
            for col in range(8):
                inbetween = self.get_squares_in_between()
                for squares in inbetween:
                    piece = self.board[row][col]
                    if piece != '' and piece[0] == opponent_color:
                        if self.is_valid_move(row, col, int(squares[0]), int(squares[1]), opponent_color):
                            print(str(row) + str(col) + "can block")
                         
                            return False

        return True
            
            
        