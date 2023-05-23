from MovesList import MovesList
from Board import Board
import copy
from TranspositionTable import TranspositionTable

class IvoryCE:
    def __init__(self, depth):
        self.depth = depth
        self.permeableboard = Board()
        self.moves_list = MovesList()
        self.transposition_table = TranspositionTable()

    def evaluate(self, board):
        piece_values = {
            "P": 1,
            "N": 3,
            "B": 3,
            "R": 5,
            "Q": 9,
            "K": 0
        }

        material_score = 0
        for row in board:
            for piece in row:
                if piece:
                    color = piece[0]
                    piece_type = piece[1]
                    if color == 'w':
                        material_score += piece_values[piece_type.upper()]
                    else:
                        material_score -= piece_values[piece_type.upper()]

        pawn_structure_score = self.evaluate_pawn_structure(board)

        piece_activity_score = self.evaluate_piece_activity(board)

        total_score = material_score + pawn_structure_score + piece_activity_score
        return total_score

    def evaluate_pawn_structure(self, board):
        pawn_structure_score = 0
    
        # Evaluate doubled pawns and isolated pawns
        white_pawns = []
        black_pawns = []
        for row in range(8):
            for col in range(8):
                piece = board[row][col]
                if piece == "P":
                    white_pawns.append((row, col))
                elif piece == "p":
                    black_pawns.append((row, col))
    
        white_pawn_files = [col for (_, col) in white_pawns]
        black_pawn_files = [col for (_, col) in black_pawns]
    
        doubled_pawns = len(white_pawns) - len(set(white_pawn_files))
        doubled_pawns -= len(black_pawns) - len(set(black_pawn_files))
        pawn_structure_score -= 0.5 * doubled_pawns
    
        isolated_white_pawns = 0
        for file in white_pawn_files:
            if file - 1 not in white_pawn_files and file + 1 not in white_pawn_files:
                isolated_white_pawns += 1
        pawn_structure_score -= 0.3 * isolated_white_pawns
    
        isolated_black_pawns = 0
        for file in black_pawn_files:
            if file - 1 not in black_pawn_files and file + 1 not in black_pawn_files:
                isolated_black_pawns += 1
        pawn_structure_score += 0.3 * isolated_black_pawns
    
        return pawn_structure_score
    
    def evaluate_piece_activity(self, board):
        piece_activity_score = 0
    
        # Evaluate piece mobility
        white_mobility = len(self.moves_list.get_legal_moves(board, "w"))
        black_mobility = len(self.moves_list.get_legal_moves(board, "b"))
        piece_activity_score += 0.1 * (white_mobility - black_mobility)
    
        # Evaluate centralized piece positions
        white_centralized_pieces = 0
        black_centralized_pieces = 0
        for row in range(8):
            for col in range(8):
                piece = board[row][col]
                if piece.isupper():
                    if piece == "N":
                        distance_to_center = abs(row - 3.5) + abs(col - 3.5)
                        if distance_to_center <= 2:
                            white_centralized_pieces += 1
                    else:
                        distance_to_center = abs(row - 4.5) + abs(col - 4.5)
                        if distance_to_center <= 2:
                            white_centralized_pieces += 1
                elif piece.islower():
                    if piece == "n":
                        distance_to_center = abs(row - 3.5) + abs(col - 3.5)
                        if distance_to_center <= 2:
                            black_centralized_pieces += 1
                    else:
                        distance_to_center = abs(row - 4.5) + abs(col - 4.5)
                        if distance_to_center <= 2:
                            black_centralized_pieces += 1
    
        piece_activity_score += 0.2 * (white_centralized_pieces - black_centralized_pieces)
    
        return piece_activity_score
    
    
    def get_best_move(self, boardcopy, color, depth):
        board = copy.deepcopy(boardcopy)
        best_move = None
        best_score = float('-inf') if color == "w" else float('inf')
        alpha = float('-inf')
        beta = float('inf')
        legal_moves = self.moves_list.get_legal_moves(boardcopy, color)
        n = len(legal_moves)

        # Sort moves based on capture-centric move ordering
        ordered_moves = []
        capture_moves = []
        quiet_moves = []
        for move in legal_moves:
            if self.moves_list.is_capture_move(move, board):
                capture_moves.append(move)
            else:
                quiet_moves.append(move)
        ordered_moves.extend(capture_moves)
        ordered_moves.extend(quiet_moves)

        for i, move in enumerate(ordered_moves):
            new_board = self.test_move(move, copy.deepcopy(board))
            if color == "w" and self.moves_list.get_legal_moves(new_board, "b") == [] and self.moves_list.is_king_in_check(new_board, "b"):
                return move
            elif color == "b" and self.moves_list.get_legal_moves(new_board, "w") == [] and self.moves_list.is_king_in_check(new_board, "w"):
                return move

            if depth == 0:
                score = self.evaluate(new_board)
            else:
                score = -self.get_best_move(new_board, "b" if color == "w" else "w", depth - 1)

            if color == "w" and score > best_score:
                best_score = score
                best_move = move
            elif color == "b" and score < best_score:
                best_score = score
                best_move = move

            if color == "w":
                alpha = max(alpha, score)
                if beta <= alpha:
                    break
            else:
                beta = min(beta, score)
                if beta <= alpha:
                    break

            progress = (i + 1) / n
            print(f"\rProgress: {progress * 100}%", end='')

        return best_move
    
    
    
