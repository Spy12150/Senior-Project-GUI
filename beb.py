import pygame
import random
from MovesList import MovesList
from Board import Board
import copy
import time
from TranspositionTable import TranspositionTable
class beb:
    def __init__(self, depth=3):
        self.depth = depth
        self.list = MovesList()
        self.transposition_table = TranspositionTable

    def get_best_move(self, board, color):

        if color == "w":
            best_move = None
            max_evaluation = -float('inf')
            for move in self.list.get_legal_moves(board, color):
                
                boardcopy = self.Test_Move(move, copy.deepcopy(board))
                if(self.list.get_legal_moves(boardcopy, "b") == [] and self.list.is_king_in_check(boardcopy, "b")):
                    return move
                evaluation = self.minimax(boardcopy, self.depth, color)
                if evaluation > max_evaluation:
                    max_evaluation = evaluation
                    best_move = move
            return best_move
        else:
            best_move = None
            min_evaluation = float('inf')
            for move in self.list.get_legal_moves(board, color):
                boardcopy = self.Test_Move(move, copy.deepcopy(board))
                if(self.list.get_legal_moves(boardcopy, "w") == [] and self.list.is_king_in_check(boardcopy, "w")):
                    return move
                evaluation = self.minimax(boardcopy, self.depth, color)
                if evaluation < min_evaluation:
                    min_evaluation = evaluation
                    best_move = move
            return best_move

    def minimax(self, position, depth, maximizing_player):
        board = position
        if (maximizing_player == "w"):
            otherplayer = "b"
        else:
            otherplayer = "w"
        if depth == 0 or not self.list.get_legal_moves(board, otherplayer):
            return self.evaluate(board)

        tt_entry = self.transposition_table.lookup(position)
        if tt_entry is not None and tt_entry[1] >= depth:
            return tt_entry[0]

        if maximizing_player == "w":
            max_evaluation = -float('inf')
            for move in self.list.get_legal_moves(position, maximizing_player):
                boardcopy = self.Test_Move(move, copy.deepcopy(position))
                evaluation = self.minimax(boardcopy, depth - 1, "b")
                max_evaluation = max(max_evaluation, evaluation)
            self.transposition_table.store(position, max_evaluation, depth) 
            return max_evaluation
        else:
            min_evaluation = float('inf')
            for move in self.list.get_legal_moves(position, maximizing_player):
                boardcopy = self.Test_Move(move, copy.deepcopy(position))
                evaluation = self.minimax(boardcopy, depth - 1, "w")
                min_evaluation = min(min_evaluation, evaluation)
            self.transposition_table.store(position, min_evaluation, depth) 
            return min_evaluation
    def piecesonboard(self, board):
        pieces = 0
        for row in range(8):
            for col in range(8):
                piece = board.board[row][col]
                if(piece != ''):
                    pieces +=1

        return pieces

    def evaluate(self, board):

        score = 0
        for row in range(8):
            for col in range(8):
                piece = board.board[row][col]
                if(piece == "wP"):
                    score += pawnEvalWhite[row][col]
                    score+= 100
                elif(piece == "bP"):
                    score -= pawnEvalBlack[row][col]
                    score -= 100
                elif(piece == "wQ"):
                    score += queenEval[row][col]
                    score +=900
                elif(piece == "bQ"):
                    score -= queenEval[row][col]
                    score -=900
                elif(piece == "wR"):
                    score += rookEvalWhite[row][col]
                    score +=500
                elif(piece == "bR"):
                    score -=  rookEvalBlack[row][col]
                    score -=500
                elif(piece == "wB"):
                    score += bishopEvalWhite[row][col]
                    score +=300
                elif(piece == "wN"):
                    score += knightEval[row][col]
                    score +=300
                elif(piece == "bB"):
                    score -= bishopEvalBlack[row][col]
                    score -= 300
                elif(piece == "bN"):
                    score -= knightEval[row][col]
                    score -=300
                elif(piece == "wK"):
                    if(self.piecesonboard(board) < 9):
                        score += kingEvalEndGameWhite[row][col]
                    else:
                        score += kingEvalWhite[row][col]
                elif(piece == "bK"):
                    if(self.piecesonboard(board) < 9):
                        score -= kingEvalEndGameBlack[row][col]
                    else:
                        score -= kingEvalBlack[row][col]

        
                    
        if(self.list.get_legal_moves(copy.deepcopy(board), "b") == [] and self.list.is_king_in_check(copy.deepcopy(board), "b")):
            score = 999999
        elif(self.list.get_legal_moves(copy.deepcopy(board), "w") == [] and self.list.is_king_in_check(copy.deepcopy(board), "w")):
            score = -999999
            
        
        return score
    def Test_Move(self, move, board):
        boardcopy = board
        start_col = ord(move[0]) - ord('a')
        start_row = 7 - (int(move[1]) - 1)
        end_col = ord(move[2]) - ord('a')
        end_row = 7- (int(move[3]) - 1)
        piece = boardcopy.board[start_row][start_col]
        if(start_row == 7 and start_col == 0):
            board.wqCastle = False
        if(start_row == 7 and start_col == 7):
            board.wkCastle = False
        if(start_row == 0 and start_col == 0):
            board.bqCastle = False
        if(start_row == 0 and start_col == 7):
            board.bkCastle = False
        boardcopy.board[start_row][start_col] = ''
        boardcopy.board[end_row][end_col] = piece
        if(piece=="wK"):
            board.wkCastle = False
            board.wqCastle = False
            
        if(piece == "bK"):
            board.bkCastle = False
            board.bqCastle = False

        if(piece=="wK" and move == "e1g1"):
            boardcopy.board[7][7] = ''
            boardcopy.board[7][5] = "wR"
        if(piece=="wK" and move == "e1c1"):
            boardcopy.board[7][0] = ''
            boardcopy.board[7][3] = "wR"
        
        if(piece=="bK" and move == "e8g8"):
            boardcopy.board[0][7] = ''
            boardcopy.board[0][5] = "wR"
        if(piece=="wK" and move == "e8c8"):
            boardcopy.board[0][0] = ''
            boardcopy.board[0][3] = "wR"
        return boardcopy
pawnEvalBlack = [
    [0,  0,  0,  0,  0,  0,  0,  0],
    [5, 10, 10, -20, -20, 10, 10,  5],
    [5, -5, -10,  10,  10, -10, -5,  5],
    [0,  -10,  -10, 20, 20,  -10,  -10,  0],
    [5,  5, 10, 25, 25, 10,  5,  5],
    [10, 10, 20, 30, 30, 20, 10, 10],
    [50, 50, 50, 50, 50, 50, 50, 50],
    [500, 500, 500, 500, 500, 500, 500, 500]
]
pawnEvalWhite = list(reversed(pawnEvalBlack))

knightEval = [
    [-50, -20, -30, -30, -30, -30, -20, -50],
    [-40, -20, 0, 0, 0, 0, -20, -40],
    [-30, 0, 10, 15, 15, 10, 0, -30],
    [-30, 5, 15, 20, 20, 15, 5, -30],
    [-30, 0, 15, 20, 20, 15, 0, -30],
    [-30, 5, 10, 15, 15, 10, 5, -30],
    [-40, -20, 0, 5, 5, 0, -20, -40],
    [-50, -20, -30, -30, -30, -30, -20, -50]
]

bishopEvalBlack = [
    [-20, -10, -10, -10, -10, -10, -10, -20],
    [-10, 5, 0, 0, 0, 0, 5, -10],
    [-10, 10, 10, 10, 10, 10, 10, -10],
    [-10, 0, 10, 10, 10, 10, 0, -10],
    [-10, 5, 5, 10, 10, 5, 5, -10],
    [-10, 0, 5, 10, 10, 5, 0, -10],
    [-10, 0, 0, 0, 0, 0, 0, -10],
    [-20, -10, -10, -10, -10, -10, -10, -20]
]
bishopEvalWhite = list(reversed(bishopEvalBlack))

rookEvalBlack = [
    [0, 0, 0, 5, 5, 0, 0, 0],
    [-5, 0, 0, 0, 0, 0, 0, -5],
    [-5, 0, 0, 0, 0, 0, 0, -5],
    [-5, 0, 0, 0, 0, 0, 0, -5],
    [-5, 0, 0, 0, 0, 0, 0, -5],
    [-5, 0, 0, 0, 0, 0, 0, -5],
    [5, 10, 10, 10, 10, 10, 10, 5],
    [0, 0, 0, 0, 0, 0, 0, 0]
]
rookEvalWhite = list(reversed(rookEvalBlack))

queenEval = [
    [-20, -10, -10, -5, -5, -10, -10, -20],
    [-10, 0, 0, 0, 0, 0, 0, -10],
    [-10, 0, 5, 5, 5, 5, 0, -10],
    [-5, 0, 5, 5, 5, 5, 0, -5],
    [0, 0, 5, 5, 5, 5, 0, -5],
    [-10, 5, 5, 5, 5, 5, 0, -10],
    [-10, 0, 5, 0, 0, 0, 0, -10],
    [-20, -10, -10, -5, -5, -10, -10, -20]
]

kingEvalBlack = [
    [20, 30, 10, 0, 0, 10, 30, 20],
    [20, 20, 0, 0, 0, 0, 20, 20],
    [-10, -20, -20, -20, -20, -20, -20, -10],
    [20, -30, -30, -40, -40, -30, -30, -20],
    [-30, -40, -40, -50, -50, -40, -40, -30],
    [-30, -40, -40, -50, -50, -40, -40, -30],
    [-30, -40, -40, -50, -50, -40, -40, -30],
    [-30, -40, -40, -50, -50, -40, -40, -30]
]
kingEvalWhite = list(reversed(kingEvalBlack))

kingEvalEndGameBlack = [
    [50, -30, -30, -30, -30, -30, -30, -50,],
    [-30, -30,  0,  0,  0,  0, -30, -30,],
    [-30, -10, 20, 30, 30, 20, -10, -30,],
    [-30, -10, 30, 40, 40, 30, -10, -30,],
    [-30, -10, 30, 40, 40, 30, -10, -30,],
    [-30, -10, 20, 30, 30, 20, -10, -30,],
    [-30, -20, -10,  0,  0, -10, -20, -30,],
    [-50, -40, -30, -20, -20, -30, -40, -50]
]
kingEvalEndGameWhite = list(reversed(kingEvalEndGameBlack))
# fmt: on