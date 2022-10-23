import pygame
from GameInfo import Game, Move

# responsible for the interface of the game
pygame.init()
WIDTH = HEIGHT = 512
SQ_SIZE = 512 // 8
FPS = 15
IMAGES = {}


def load_images():
    for i in ['wP', 'bP', 'bK', 'wK', 'bN', 'wN', 'bQ', 'wQ', 'bR', 'wR', 'bB', 'wB']:
        IMAGES[i] = pygame.image.load(f'images/{i}.png')


def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    screen.fill('WHITE')
    g = Game()
    validMoves = g.get_valid_moves()
    moveMade = False
    load_images()
    running = True
    sqSelected = tuple()
    playerClicks = []
    while running:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False

            elif e.type == pygame.MOUSEBUTTONDOWN:
                location = pygame.mouse.get_pos()
                col = location[0] // SQ_SIZE
                row = location[1] // SQ_SIZE
                print(row, col)
                if g.board[row][col] == '-' and len(playerClicks) == 0:
                    print("Empty square was pressed")
                    print('____________')
                    continue

                if sqSelected == (row, col):
                    print("Move cleared")
                    sqSelected = ()
                    playerClicks = []

                else:
                    print('Click added')
                    sqSelected = (row, col)
                    playerClicks.append(sqSelected)

                if len(playerClicks) == 2:
                    print("Move in process...")
                    move = Move(playerClicks[0], playerClicks[1], g.board)
                    for i in range(len(validMoves)):
                        if move == validMoves[i]:
                            print('Move is made')
                            print(move.get_chess_notation())
                            g.make_move(validMoves[i])
                            moveMade = True

                            print("Clicks Cleared")
                            print(g.white_move)
                            print('_____________________')
                            sqSelected = ()
                            playerClicks = []
                    if not moveMade:
                        playerClicks = [sqSelected]

            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_b:
                    g.undo_move()
                    moveMade = True

        if moveMade:
            validMoves = g.get_valid_moves()
            moveMade = False

        clock.tick(FPS)
        draw_game(screen, g)
        pygame.display.flip()


def draw_game(screen, g):
    draw_board(screen)
    draw_pieces(screen, g)


def draw_board(screen):
    colors = [pygame.Color("white"), pygame.Color('grey')]
    for row in range(8):
        for column in range(8):
            pygame.draw.rect(screen, colors[(row + column) % 2],
                             pygame.Rect(SQ_SIZE * column, SQ_SIZE * row, SQ_SIZE, SQ_SIZE, ))


def draw_pieces(screen, g):
    for row in range(8):
        for column in range(8):
            if g.board[row][column] != '-':
                screen.blit(IMAGES[g.board[row][column]],
                            pygame.Rect(SQ_SIZE * column, SQ_SIZE * row, SQ_SIZE, SQ_SIZE))


if __name__ == '__main__':
    main()
