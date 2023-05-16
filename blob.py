import chess
import chess.pgn
import io

pgn_text = '''
[Event "Rated Classical game"]
[Site "https://lichess.org/ntf4qW5C"]
[White "cocinda"]
[Black "mehran35"]
[Result "0-1"]
[UTCDate "2017.01.31"]
[UTCTime "23:00:01"]
[WhiteElo "1627"]
[BlackElo "1827"]
[WhiteRatingDiff "-6"]
[BlackRatingDiff "+6"]
[ECO "B01"]
[Opening "Scandinavian Defense"]
[TimeControl "300+8"]
[Termination "Normal"]

1. e4 d5 2. f3 d4 3. d3 e5 4. h4 Nc6 5. a3 a6 6. g3 f5 7. exf5 Bxf5 8. g4 Bd7 9. h5 Bd6 10. Be2 e4 11. f4 e3 12. f5 Bg3+ 13. Kf1 Qg5 14. Nh3 Qf6 15. Kg2 Qe5 16. c3 Nh6 17. cxd4 Nxd4 18. Nc3 Bc6+ 19. Kf1 Bxh1 20. Ne4 Bxe4 21. dxe4 Qxe4 22. Qa4+ c6 23. Ng1 Nxg4 24. Nf3 O-O-O 25. Kg2 Bf2 26. b3 Ne5 27. Bb2 Qg4+ 28. Kh2 Qg3+ 29. Kh1 Ndxf3 30. Bxe5 Qh3+ 31. Bh2 Qxh2# 0-1

[Event "Rated Correspondence game"]
[Site "https://lichess.org/XVq8XtlR"]
[White "rubens2882"]
[Black "daianebernardi"]
[Result "1/2-1/2"]
[UTCDate "2017.01.31"]
[UTCTime "23:00:00"]
[WhiteElo "1337"]
[BlackElo "1662"]
[WhiteRatingDiff "+86"]
[BlackRatingDiff "-86"]
[ECO "A00"]
[Opening "Van't Kruijs Opening"]
[TimeControl "-"]
[Termination "Normal"]

1. e3 d6 2. d4 g6 3. Qf3 f5 4. Qd1 e6 5. f3 Nh6 6. e4 d5 7. exd5 Bb4+ 8. c3 Ba5 9. dxe6 Bxe6 10. Qe2 Qe7 11. Qe5 Nf7 12. Qxa5 Nc6 13. Qb5 a6 14. Qe2 h5 15. Qd2 Bd5+ 16. Qe2 h4 17
'''


import chess
import chess.pgn

class ChessConverter:
    @staticmethod
    def boardtofen(fen):
        binary = ''
        for element in fen:
            if(element == "P"):
                binary += "0100000"
            elif(element == "R"):
                binary += "0010000"
            elif(element == "N"):
                binary += "0001000"
            elif(element == "B"):
                binary += "0000100"
            elif(element == "Q"):
                binary += "0000010"
            elif(element == "K"):
                binary += "0000001"
            elif(element == "p"):
                binary += "1100000"
            elif(element == "r"):
                binary += "1010000"
            elif(element == "n"):
                binary += "1001000"
            elif(element == "b"):
                binary += "1000100"
            elif(element == "q"):
                binary += "1000010"
            elif(element == "k"):
                binary += "1000001"
            elif(element == "1"):
                binary += "0000000"
            elif(element == "2"):
                binary += "0000000"
                binary += "0000000"
                
            elif(element == "3"):
                binary += "0000000"
                binary += "0000000"
                binary += "0000000"
            elif(element == "4"):
                binary += "0000000"
                binary += "0000000"
                binary += "0000000"
                binary += "0000000"
            elif(element == "5"):
                binary += "0000000"
                binary += "0000000"
                binary += "0000000"
                binary += "0000000"
                binary += "0000000"
            elif(element == "6"):
                binary += "0000000"
                binary += "0000000"
                binary += "0000000"
                binary += "0000000"
                binary += "0000000"
                binary += "0000000"
                
            elif(element == "7"):
                binary += "0000000"
                binary += "0000000"
                binary += "0000000"
                binary += "0000000"
                binary += "0000000"
                binary += "0000000"
                binary += "0000000"
            elif(element == "8"):
                binary += "0000000"
                binary += "0000000"
                binary += "0000000"
                binary += "0000000"
                binary += "0000000"
                binary += "0000000"
                binary += "0000000"
                binary += "0000000"
            elif(element == "w"):
                binary += "0"
            elif(element == "b"):
                binary += "1"

        return binary
    
    def result_to_binary(result):
        if(result == "1-0"):
            return 1
        elif(result == "0-1"):
            return -1
        else:
            return 0
    





            

def generate_fen(game):
    board = chess.Board()
    moves = game.mainline_moves()
    fen_list = []

    for move in moves:
        board.push(move)
        fen_list.append(board.fen())

    return fen_list


def process_game(game):
    # Process each game here
    # You can access game metadata and moves within this function
    
    pgn = chess.pgn.read_game(io.StringIO(pgn_text))
    fen_list = generate_fen(pgn)

    converter = ChessConverter()
    

    for i, fen in enumerate(fen_list):
        print(f"Position {i + 1}: {converter.boardtofen(fen)} ")


pgn_file = open("lichess_db_standard_rated_2017-02.pgn")

# Specify the interval to start processing games
starting_line_interval = 18

# Variable to keep track of the current line number
current_line = 1

while True:
    # Check if the current line is within the desired interval
    if (current_line + 1) % starting_line_interval == 0:
        game = chess.pgn.read_game(pgn_file)

        if game is None:
            break

        # Process each game here
        # You can access game metadata and moves within this loop
        fen_list = generate_fen(game)
        result = game.headers["Result"]
        for i, fen in enumerate(fen_list):
            print(f"Position {i + 1} - Line {current_line}: {fen} Result: {result}")

    # Read the next line
    line = pgn_file.readline()

    if not line:
        break

    current_line += 1

pgn_file.close()

