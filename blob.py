import chess
import chess.pgn
import io
import tensorflow as tf
import numpy as np

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

        return binary[:449]
    
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

Fens = []
Results = []

while True:
    # Check if the current line is within the desired interval
    print(f"\rProgress: {(current_line/183552715)*100}%", end='')

    if (current_line + 1) % starting_line_interval == 0:
        game = chess.pgn.read_game(pgn_file)

        if game is None:
            break

        # Process each game here
        # You can access game metadata and moves within this loop
        fen_list = generate_fen(game)
        result = game.headers["Result"]
        converter = ChessConverter()
        binaryResult = converter.result_to_binary(result)

        for i, fen in enumerate(fen_list):
            Fens.append(np.array([int(j) for j in (converter.boardtofen(fen))]))
            Results.append(binaryResult)

    # Read the next line
    line = pgn_file.readline()

    if not line:
        break

    current_line += 1

pgn_file.close()
tokenizer = Tokenizer()
tokenizer.fit_on_texts([first_455])



# Convert text to sequences of tokens
sequences = tokenizer.texts_to_sequences([first_455])

# Pad sequences to a fixed length
max_length = 449
padded_sequences = tf.keras.preprocessing.sequence.pad_sequences(sequences, maxlen=max_length)


model = tf.keras.models.Sequential([
    tf.keras.layers.InputLayer(449),
    tf.keras.layers.Dense(512, activation='relu'),
    tf.keras.layers.Dense(512, activation='relu'),
    tf.keras.layers.Dense(1),
])

model.compile(
    optimizer='adam',
    loss= "mean_squared_error",
    metrics=[accuracy])

model.fit(
    x = np.asarray(Fens),
    y = np.asarray(Results),
    epochs = 5,
    batch_size = 100,
    validation_split = 0.2
)

model.save("predictor.h5")





