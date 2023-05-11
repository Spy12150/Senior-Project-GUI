from turtle import color
import pygame
import random
from MovesList import MovesList
from Board import Board
import copy
import time
from TranspositionTable import TranspositionTable
import multiprocessing
from multiprocessing import Pool, cpu_count, freeze_support

class jef:
    def __init__(self, depth, num_processes=2):
        self.depth = depth
        self.list = MovesList()
        self.permeableboard = Board()
        self.num_processes = num_processes



    def max_value(self, board, depth, alpha, beta):
        if depth == 0 or self.list.get_legal_moves(board, "w") == []:
            
            return self.evaluate(board)

        max_score = float('-inf')
        for move in self.list.get_legal_moves(board, "w"):
            new_board = self.Test_Move(move, copy.deepcopy(board))
            score = self.min_value(new_board, depth - 1, alpha, beta)
            max_score = max(max_score, score)
            if(self.depth > depth + 1):
                alpha = max(alpha, max_score)
                if beta <= alpha:
                    break

        return max_score

    def min_value(self, board, depth, alpha, beta):
        if depth == 0 or self.list.get_legal_moves(board, "b") == []:
            return self.evaluate(board)

        min_score = float('inf')
        for move in self.list.get_legal_moves(board, "b"):
            new_board = self.Test_Move(move, copy.deepcopy(board))
            score = self.max_value(new_board, depth - 1, alpha, beta)
            min_score = min(min_score, score)
            if(self.depth > depth + 1):
                beta = min(beta, min_score)
                if beta <= alpha:
                    break

        return min_score


    def get_best_move(self, boardcopy, color):
        board = copy.deepcopy(boardcopy)
        start_time = time.time()
        best_move = None
        alpha = float('-inf')
        beta = float('inf')
        if color == "w":
            legal_moves = self.list.get_legal_moves(boardcopy, "w")
        else:
            legal_moves = self.list.get_legal_moves(boardcopy, "b")

        if self.num_processes == 1: # single process
            for move in legal_moves:
                new_board = self.Test_Move(move, copy.deepcopy(board))
                if self.list.get_legal_moves(new_board, "b" if color == "w" else "w") == [] and self.list.is_king_in_check(new_board, "b" if color == "w" else "w"):
                    return move
                if color == "w":
                    score = self.min_value(new_board, self.depth - 1, alpha, beta)
                    if score > alpha:
                        alpha = score
                        best_move = move
                if color == "b":
                    score = self.max_value(new_board, self.depth - 1, alpha, beta)
                    if score < alpha:
                        alpha = score
                        best_move = move
        else: # multiprocessing
            if __name__ == '__main__':
                freeze_support()
            pool = multiprocessing.Pool(processes=self.num_processes)
            chunksize = len(legal_moves) // self.num_processes
            results = [pool.apply_async(self.evaluate_moves, args=(color, board, legal_moves[i:i+chunksize], alpha, beta)) for i in range(0, len(legal_moves), chunksize)]
            pool.close()
            pool.join()
            for result in results:
                move, score = result.get()
                if score > alpha:
                    alpha = score
                    best_move = move

        return best_move
    def evaluate_moves(self, color, board, moves, alpha, beta):
        best_move = None
        best_score = float('-inf') if color == "w" else float('inf')
        for move in moves:
            new_board = self.Test_Move(move, copy.deepcopy(board))
            if self.list.get_legal_moves(new_board, "b" if color == "w" else "w") == [] and self.list.is_king_in_check(new_board, "b" if color == "w" else "w"):
                return move, float('inf') if color == "w" else float('-inf')
            if(color == "w"):
                score = self.min_value(new_board, self.depth - 1, alpha, beta)
            else:
                score = self.max_value(new_board, self.depth - 1, alpha, beta)
            if color == "w":
                if score > best_score:
                    best_score = score
                    best_move = move
                alpha = max(alpha, score)
                if beta <= alpha:
                    break
            else:
                if score < best_score:
                    best_score = score
                    best_move = move
                beta = min(beta, score)
                if beta <= alpha:
                    break
        return best_move, best_score

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
                        score += kingEvalEndGameBlack[row][col]
                    else:
                        score += kingEvalBlack[row][col]

        
                    
        if(self.list.get_legal_moves(board, "b") == [] and self.list.is_king_in_check(board, "b")):
            score = 999999
        elif(self.list.get_legal_moves(board, "w") == [] and self.list.is_king_in_check(board, "w")):
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
    [0,  0,  0, 20, 20,  0,  0,  0],
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

