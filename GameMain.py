import pygame

import GameInfo
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
    moveMade = False  # flag var for when move is made
    animate = False  # flag move for when to animate the move
    load_images()  # loading images before loop
    running = True
    sqSelected = tuple()  # keep track of last user input
    playerClicks = []  # keep track of clicks
    gameOver = False
    while running:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
            # mouse clicks handler
            elif e.type == pygame.MOUSEBUTTONDOWN:
                if not gameOver:
                    location = pygame.mouse.get_pos()
                    col = location[0] // SQ_SIZE
                    row = location[1] // SQ_SIZE

                    if sqSelected == (row, col):  # same square clicked twice, undo the click
                        sqSelected = ()
                        playerClicks = []

                    else:
                        sqSelected = (row, col)  # user clicked square add to playerClicks
                        playerClicks.append(sqSelected)

                    if len(playerClicks) == 2:
                        move = Move(playerClicks[0], playerClicks[1], g.board)
                        for i in range(len(validMoves)):
                            if move == validMoves[i]:
                                print(move.get_chess_notation())
                                g.make_move(validMoves[i])
                                moveMade = True
                                animate = True
                                sqSelected = ()
                                playerClicks = []
                        if not moveMade:
                            playerClicks = [sqSelected]
            # key handler
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_b:  # undo when 'b'
                    g.undo_move()
                    animate = False
                    moveMade = True

                if e.key == pygame.K_r:  # reset board when "r" pressed
                    g = GameInfo.Game()
                    validMoves = g.get_valid_moves()
                    sqSelected = ()
                    playerClicks = []
                    moveMade = False
                    animate = False

        if moveMade:
            if animate:
                animateMove(g.log[-1], screen, g, clock)
            validMoves = g.get_valid_moves()
            moveMade = False
            animate = False

        draw_game(screen, g, validMoves, sqSelected)
        if g.checkmate:
            gameOver = True
            if g.white_move:
                draw_text(screen, 'Black wins by checkmate!')
            else:
                draw_text(screen, 'White wins by checkmate!')

        elif g.stalemate:
            gameOver = True
            draw_text(screen, 'Stalemate')
        clock.tick(FPS)
        pygame.display.flip()


def draw_game(screen, g, validMoves, sqselected):
    draw_board(screen)
    highlitght_squares(screen, g, validMoves, sqselected)
    draw_pieces(screen, g)


def draw_board(screen):
    global colors
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


def highlitght_squares(screen, g, validMoves, sqselected):
    if sqselected != ():
        row, column = sqselected
        if g.board[row][column][0] == (
        'w' if g.white_move else 'b'):  # check if sqSelected is a piece that can be moved(note the nested check
            s = pygame.Surface((SQ_SIZE, SQ_SIZE), )
            s.set_alpha(100)
            s.fill(pygame.Color('green'))
            screen.blit(s, (column * SQ_SIZE, row * SQ_SIZE))
            s.fill(pygame.Color('yellow'))
            for move in validMoves:
                if move.startRow == row and move.startColumn == column:
                    screen.blit(s, ((move.endColumn * SQ_SIZE, move.endRow * SQ_SIZE)))


def animateMove(move, screen, g, clock):
    global colors
    dR = move.endRow - move.startRow
    dC = move.endColumn - move.startColumn
    framesPerSquare = 10  # frames to move one square
    frameCount = (abs(dR) + abs(dC)) * framesPerSquare
    for frame in range(frameCount + 1):
        r, c = ((move.startRow + dR * frame / frameCount, move.startColumn + dC * frame / frameCount))
        draw_board(screen)
        draw_pieces(screen, g)
        # erase the piece moved from its ending square
        color = colors[(move.endRow + move.endColumn) % 2]
        endSquare = pygame.Rect(move.endColumn * SQ_SIZE, move.endRow * SQ_SIZE, SQ_SIZE, SQ_SIZE)
        pygame.draw.rect(screen, color, endSquare)
        # draw captured pice if exists
        if move.pieceCaptured != '-':
            screen.blit(IMAGES[move.pieceCaptured], endSquare)
        # draw moving piece
        screen.blit(IMAGES[move.pieceMoved], pygame.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))
        pygame.display.flip()
        clock.tick(60)


def draw_text(screen, text):
    font = pygame.font.SysFont('Comic Sans', 32, True, False)
    textObject = font.render(text, False, pygame.Color('blue'))
    textLocation = pygame.Rect(0, 0, WIDTH, HEIGHT).move(WIDTH / 2 - textObject.get_width() / 2,
                                                         HEIGHT / 2 - textObject.get_height() / 2)
    screen.blit(textObject, textLocation)
    textObject = font.render(text, False, pygame.Color('Black'))
    screen.blit(textObject, textLocation.move(2, 2))


if __name__ == '__main__':
    main()
