import pygame

# Set up the Pygame window
pygame.init()
WIDTH = HEIGHT = 800
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chess Game")

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
BLUE = (0, 0, 255)

# Load chess piece images
images = {}
images["wK"] = pygame.transform.scale(pygame.image.load('data/imgs/wK.png'), (64, 64))
images["wQ"] = pygame.transform.scale(pygame.image.load('data/imgs/wQ.png'), (64, 64))
images["wR"] = pygame.transform.scale(pygame.image.load('data/imgs/wR.png'), (64, 64))
images["wB"] = pygame.transform.scale(pygame.image.load('data/imgs/wB.png'), (64, 64))
images["wN"] = pygame.transform.scale(pygame.image.load('data/imgs/wN.png'), (64, 64))
images["wP"] = pygame.transform.scale(pygame.image.load('data/imgs/wP.png'), (64, 64))
images["bK"] = pygame.transform.scale(pygame.image.load('data/imgs/bK.png'), (64, 64))
images["bQ"] = pygame.transform.scale(pygame.image.load('data/imgs/bQ.png'), (64, 64))
images["bR"] = pygame.transform.scale(pygame.image.load('data/imgs/bR.png'), (64, 64))
images["bB"] = pygame.transform.scale(pygame.image.load('data/imgs/bB.png'), (64, 64))
images["bN"] = pygame.transform.scale(pygame.image.load('data/imgs/bN.png'), (64, 64))
images["bP"] = pygame.transform.scale(pygame.image.load('data/imgs/bP.png'), (64, 64))

# Define the chess board
board = [
    ['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR'],
    ['bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP'],
    ['', '', '', '', '', '', '', ''],
    ['', '', '', '', '', '', '', ''],
    ['', '', '', '', '', '', '', ''],
    ['', '', '', '', '', '', '', ''],
    ['wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP'],
    ['wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR']
]

# Define the square size and font
SQUARE_SIZE = HEIGHT // 8
FONT = pygame.font.SysFont('calibri', 30)

# Draw the chess board
def draw_board():
    for row in range(8):
        for col in range(8):
            color = WHITE if (row + col) % 2 == 0 else GRAY
            pygame.draw.rect(win, color, (col*SQUARE_SIZE, row*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            piece = board[row][col]
            if piece != '':
                win.blit(images[piece], (col*SQUARE_SIZE, row*SQUARE_SIZE))

# Draw the coordinates on the board
def draw_coordinates():
    for i in range(8):
        text = FONT.render(str(i+1), True, BLACK)
        win.blit(text, (5, i*SQUARE_SIZE+20))
        text = FONT.render(chr(97+i), True, BLACK)
        win.blit(text, (i*SQUARE_SIZE+20, HEIGHT-35))

# Main game loop
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        
    # Draw the board and pieces
    draw_board()
    draw_coordinates()

    # Check if the game is over
    pygame.display.update()

pygame.quit()
