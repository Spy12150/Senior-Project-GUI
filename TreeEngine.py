from curses import start_color
import pygame
import random

class TreeEngine:
    def __init__(self, depth):
        self.depth = depth
        





    def get_random_moves(self, board, color):
        moves = self.get_legal_moves(board, color)
        if(moves == [] and board.is_king_in_check(color)):
            return "no"
        elif(moves == []):
            return "maybe"
        

        
        
        return moves[random.randint(0, len(moves) - 1)]

    def get_legal_moves(self, board, color):
        moves = []
        boardcopy = board  # create a copy of the board to avoid modifying the original
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
                                
                                
                                if self.move(move, color, boardcopy):
                                    moves.append(move)
                                    boardcopy = board
                    elif piece[1] == "P" and color == "b":
                        movesopt = {(1,-1), (1,1), (1,0), (2,0)}
                        for movenums in movesopt:
                            end_row, end_col = row + movenums[0], col + movenums[1]
                            if end_row >= 0 and end_col >= 0:
                                move = chr(ord('a') + col) + str(8 - row)+ chr(ord('a') + end_col) + str(8 - end_row )
                                if self.move(move, color, boardcopy):
                                    moves.append(move)
                                    boardcopy = board
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
                                if self.move(move, color, boardcopy):
                                    moves.append(move)
                                    boardcopy = board
                    elif piece[1] == "N" and piece[0] == color:
                        movesopt = {(-2,-1), (-1,-2),(-2,1),(1,-2),(2,-1),(-1,2),(2,1),(2,1)}
                        for movenums in movesopt:
                            end_row, end_col = row + movenums[0], col + movenums[1]
                            if end_row >= 0 and end_col >= 0:
                                move = chr(ord('a') + col) + str(8 - row)+ chr(ord('a') + end_col) + str(8 - end_row )
                                
                                
                                if self.move(move, color, boardcopy):
                                    moves.append(move)
                                    
                                    boardcopy = board
                    elif piece[1] == "K" and piece[0] == color:
                        movesopt = []
                        for i in [-1,0,1]:
                            for j in [-1, 0, 1]:
                                movesopt.append((i,j))
                        for movenums in movesopt:
                            end_row, end_col = row + movenums[0], col + movenums[1]
                            if end_row >= 0 and end_col >= 0:
                                move = chr(ord('a') + col) + str(8 - row)+ chr(ord('a') + end_col) + str(8 - end_row )
                                
                                if self.move(move, color, boardcopy):
                                    moves.append(move)
                                    boardcopy = board
                    elif piece[1] == "B" and piece[0] == color:
                        movesopt = []
                        for i in range(17):
                            movesopt.append((i-8,i - 8))
                        for i in range(17):
                            movesopt.append((i - 8,-i + 8))
                        for movenums in movesopt:
                            end_row, end_col = row + movenums[0], col + movenums[1]
                            move = chr(ord('a') + col) + str(8 - row)+ chr(ord('a') + end_col) + str(8 - end_row )
                            
                            if self.move(move, color, boardcopy):
                                    moves.append(move)
                                    boardcopy = board
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
                            
                            if self.move(move, color, boardcopy):
                                    moves.append(move)
                                    boardcopy = board

        return moves


    def move(self, move, color, board):
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

        piece = board.board[start_row][start_col]

        if piece == '':
            print(str(start_row) + str(start_col))
            
            return False
        if(board.board[end_row][end_col] != ''):
            if(board.board[end_row][end_col][0] == color):
                
                
                return False


        if (board.board[start_row][start_col][0] != color):
            
            return False

        if (board.is_valid_move(start_row, start_col, end_row, end_col, color)):
            swapped = board.board[end_row][end_col]
            board.board[start_row][start_col] = ''
            board.board[end_row][end_col] = piece
            if((piece == "wP" and end_row == 0) or (piece == "bP" and end_row == 7)):
                board.board[end_row][end_col] = piece[0] + "Q"
            if(board.is_king_in_check(color)):
                board.board[start_row][start_col] = piece
                board.board[end_row][end_col] = swapped
                
                return False
            board.board[start_row][start_col] = piece
            board.board[end_row][end_col] = swapped

        else: 
            
  
            return False
        
        

        
        
        return True

    