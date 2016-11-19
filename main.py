import random
import pygame
from pygame.locals import *

if not pygame.image.get_extended():
    raise(SystemExit, 'Sorry, extended image module required')


TICK_MS = 150

board = []
for row in range(20):
    board.append([])
    for col in range(10):
        board[row].append(0)

all_figures = {
    # Z
    0: (((0, 0), (0, 1), (1, 1), (1, 2)),
        ((0, 1), (1, 0), (1, 1), (2, 0))),
    # S
    1: (((0, 1), (0, 2), (1, 0), (1, 1)),
        ((0, 0), (1, 0), (1, 1), (2, 1))),
    # L
    2: (((0, 0), (1, 0), (2, 0), (2, 1)),
        ((0, 2), (1, 0), (1, 1), (1, 2)),
        ((0, 0), (0, 1), (0, 2), (1, 0)),
        ((0, 0), (0, 1), (1, 1), (2, 1))),
    # back-L
    3: (((0, 1), (1, 1), (2, 0), (2, 1)),
        ((0, 0), (1, 0), (1, 1), (1, 2)),
        ((0, 0), (0, 1), (1, 0), (2, 0)),
        ((0, 0), (0, 1), (0, 2), (1, 2))),
    # I
    4: (((0, 0), (1, 0), (2, 0), (3, 0)),
        ((0, 0), (0, 1), (0, 2), (0, 3))),
    # O
    5: (((0, 0), (0, 1), (1, 0), (1, 1)),),
    # T
    6: (((0, 0), (0, 1), (0, 2), (1, 1)),
        ((0, 0), (1, 0), (1, 1), (2, 0)),
        ((0, 1), (1, 0), (1, 1), (1, 2)),
        ((0, 1), (1, 0), (1, 1), (2, 1)))
}

timer = pygame.time.Clock()

pygame.init()
window_size = (300, 600)
screen = pygame.display.set_mode(window_size, 0, 32)
pygame.display.set_caption('PyTatris')
bgColor = (255, 255, 255)
block = pygame.image.load('pic.png')
figure_pos = [4, 0]  # 4 colon, 0 row
running = True


def check_collision(board, figure, x, y):
    new_figure = []
    figure_pos = (x, y)
    for i in figure:
        new_figure.append(tuple(map(sum, zip(i, figure_pos))))
    for shape in new_figure:
        if shape[0] >= 10 or shape[0] < 0:
            return True
        elif shape[1] >= 20:
            return True
        if board[shape[1]][shape[0]]:
            return True
    return False


def save_board(board, figure, x, y):
    new_figure = []
    figure_pos = (x, y)
    for i in figure:
        new_figure.append(tuple(map(sum, zip(i, figure_pos))))
    for shape in new_figure:
        board[shape[1]][shape[0]] = 1
    new_board = []
    for num, row in enumerate(board):
        if min(row) == 1:
            new_board = list()
            new_board.append([])
            for _ in range(10):
                new_board[0].append(0)
            new_board.extend(board[:num])
            new_board.extend(board[num+1:])
            board = new_board
    return board


def draw_board(screen, board):
    x=y=0
    for row in board:
        for col in row:
            if col:
                screen.blit(block, (x, y))
            x += 30
        y += 30
        x = 0


def draw_figure(screen, figure, figure_pos):
    new_figure = []
    for shape in figure:
        new_figure.append(tuple(map(sum, zip(shape, figure_pos))))
    for shape in new_figure:
        screen.blit(block, tuple(x * 30 for x in shape))

full_figure = None
figure_rotation = 0

while running:
    screen.fill(bgColor)
    # for loop through the event queue
    if not full_figure:
        full_figure = all_figures[random.randint(0, 6)]
        figure_rotation = 0
        if check_collision(board, full_figure[figure_rotation], figure_pos[0], figure_pos[1]):
            running = False
    figure = full_figure[figure_rotation]

    draw_board(screen, board)
    #draw_figure(screen, figure, figure_pos)

    if not check_collision(board, figure, figure_pos[0], figure_pos[1]+1):
        draw_board(screen, board)
        figure_pos[1] += 1
        draw_figure(screen, figure, figure_pos)
    else:
        board = save_board(board, figure, figure_pos[0], figure_pos[1])
        screen.fill(bgColor)
        draw_board(screen, board)
        figure_pos = [4, 0]
        full_figure = None

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
            elif event.key == K_UP and full_figure:
                figure_rotation = (figure_rotation + 1) % len(full_figure)
                screen.fill(bgColor)
                draw_board(screen, board)
                figure = full_figure[figure_rotation]
                new_figure = []
                for shape in figure:
                    new_figure.append(list(map(sum, zip(shape, figure_pos))))

                if figure_pos[0] > 7 or figure_pos[0] < 3:
                    while max(i[0] for i in new_figure) >= 10:
                        figure_pos[0] -= 1
                        for shape in new_figure:
                            shape[0] -= 1
                    while min(i[0] for i in new_figure) < 0:
                        figure_pos[0] += 1
                        for shape in new_figure:
                            shape[0] += 1
                if check_collision(board, figure, figure_pos[0], figure_pos[1]):
                    y = figure_pos[1]
                    while check_collision(board, figure, figure_pos[0], y):
                        y -= 1
                    save_board(board, figure, figure_pos[0], y)
                    draw_board(screen, board)
                    figure_pos = [4, 0]
                    full_figure = None



                draw_figure(screen, figure, figure_pos)

                pygame.display.update()

            elif event.key in [K_RIGHT, K_LEFT]:
                x, y = figure_pos
                if event.key == K_LEFT:
                    x -= 1
                elif event.key == K_RIGHT:
                    x += 1
                if not check_collision(board, figure, x, y):
                    figure_pos[0] = x
                screen.fill(bgColor)
                draw_board(screen, board)
                draw_figure(screen, figure, figure_pos)
                pygame.display.update()

        elif event.type == QUIT:
            running = False

    pygame.time.wait(TICK_MS)