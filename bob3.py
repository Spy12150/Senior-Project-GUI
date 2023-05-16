import pygame
import random
from MovesList import MovesList
from Board import Board
import copy
import time
from TranspositionTable import TranspositionTable
class bob3:
    def __init__(self, depth):
        self.depth = depth
        self.list = MovesList()
        self.transposition_table = TranspositionTable()
        self.moves = 0

    def get_best_move(self, board, color):

        moves = self.list.get_legal_moves(board, color)

        # n = len(moves)
            
        # i = 0
        # self.moves += 1


        if color == "w":
            best_move = None
            max_evaluation = -float('inf')
            for move in moves:
                
                boardcopy = self.Test_Move(move, copy.deepcopy(board))
                if(self.list.get_legal_moves(boardcopy, "b") == [] and self.list.is_king_in_check(boardcopy, "b")):
                    return move
                if self.piecesonboard(boardcopy) < 4:
                    evaluation = self.minimax(boardcopy, 6, "b")
                else:
                    evaluation = self.minimax(boardcopy, 1, "b")
                
                # print(f"\rProgress: {(i/n)*100}%", end='')
                if evaluation > max_evaluation:
                    max_evaluation = evaluation
                    best_move = move
                if evaluation == max_evaluation:
                    best_move = random.choice([best_move, move])
            return best_move
        else:
            best_move = None
            min_evaluation = float('inf')
            for move in moves:
                boardcopy = self.Test_Move(move, copy.deepcopy(board))
                if(self.list.get_legal_moves(boardcopy, "w") == [] and self.list.is_king_in_check(boardcopy, "w")):
                    return move
                
                if self.piecesonboard(boardcopy) < 4:
                    evaluation = self.minimax(boardcopy, 6, "w")
                else:
                    evaluation = self.minimax(boardcopy, 1, "w")
                
                
                # print(f"\rProgress: {(i/n)*100}%", end='')
                if evaluation < min_evaluation:
                    min_evaluation = evaluation
                    best_move = move
                if evaluation == min_evaluation:
                    best_move = random.choice([best_move, move])
            return best_move
    
        

    def minimax(self, board, depth, color, alpha=-float('inf'), beta=float('inf')):
        board = board

        moves = self.list.get_legal_moves(board, color)
        if depth == 0 or not moves:
            return self.evaluate(board)

        tt_entry = self.transposition_table.lookup(board)
        if tt_entry is not None and tt_entry[1] >= depth:
            return tt_entry[0]

        if color == "w":
            max_evaluation = -float('inf')
            for move in moves:
                boardcopy = self.Test_Move(move, copy.deepcopy(board))
                if self.piecesonboard(boardcopy) < 4:
                    evaluation = self.minimax(boardcopy, depth - 1, "b", alpha, beta)
                else:
                    evaluation = self.minimax(boardcopy, depth - 1, "b", alpha, beta)
                max_evaluation = max(max_evaluation, evaluation)
                alpha = max(alpha, max_evaluation)
                if alpha >= beta:
                    break
            self.transposition_table.store(board, max_evaluation, depth)
            return max_evaluation
        else:
            min_evaluation = float('inf')
            for move in moves:
                boardcopy = self.Test_Move(move, copy.deepcopy(board))
                if self.piecesonboard(boardcopy) < 4:
                    evaluation = self.minimax(boardcopy, depth - 1, "w", alpha, beta)
                else:
                    evaluation = self.minimax(boardcopy, depth - 1, "w", alpha, beta)
                min_evaluation = min(min_evaluation, evaluation)
                beta = min(beta, min_evaluation)
                if alpha >= beta:
                    break
            self.transposition_table.store(board, min_evaluation, depth)
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
                    if self.moves < 17:
                        score += pawnEvalWhite[row][col]
                    else:
                        score += (7-row)*8
                    score+= 100
                    if(board.board[row - 1][col] == "wP"):
                        score -= 30
                    if(self.list.isTempo(piece, row, col, board)):
                        score += 30
                elif(piece == "bP"):
                    if self.moves < 17:
                        score -= pawnEvalBlack[row][col]
                    else:
                        score -= row*8
                    score -= 100
                    if board.board[row - 1][col] == "wP":
                        score += 30
                    if(self.list.isTempo(piece, row, col, board)):
                        score -= 30
                elif(piece == "wQ"):
                    score += queenEval[row][col]
                    score +=900
                    if(self.list.isTempo(piece, row, col, board)):
                        score += 30
                    
                elif(piece == "bQ"):
                    score -= queenEval[row][col]
                    score -=900
                    if(self.list.isTempo(piece, row, col, board)):
                        score -= 30
                elif(piece == "wR"):
                    score += rookEvalWhite[row][col]
                    score +=500
                    if(self.list.isTempo(piece, row, col, board)):
                        score += 30
                elif(piece == "bR"):
                    score -=  rookEvalBlack[row][col]
                    score -=500
                    if(self.list.isTempo(piece, row, col, board)):
                        score -= 30
                elif(piece == "wB"):
                    score += bishopEvalWhite[row][col]
                    score +=300
                    if(self.list.isTempo(piece, row, col, board)):
                        score += 30
                elif(piece == "wN"):
                    score += knightEval[row][col]
                    score +=300
                    if(self.list.isTempo(piece, row, col, board)):
                        score += 30
                elif(piece == "bB"):
                    score -= bishopEvalBlack[row][col]
                    score -= 300
                    if(self.list.isTempo(piece, row, col, board)):
                        score -= 30
                elif(piece == "bN"):
                    score -= knightEval[row][col]
                    score -=300
                    if(self.list.isTempo(piece, row, col, board)):
                        score -= 30
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
    [20, 30, -10, 0, 0, -10, 30, 20],
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