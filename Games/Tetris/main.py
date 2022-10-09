import pygame
import random
from components.shapes import *
from components.piece import Piece
from time import sleep

pygame.font.init()


'''
10x20 square grid
shapes: S, Z, I, O, J, L, T
represented in order by 0 - 6
'''
#contsants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 700
PLAYBLE_WIDTH = SCREEN_WIDTH - 500
PLAYBLE_HEIGHT = SCREEN_HEIGHT - 100
BLOCKSIZE = 30
FPS = 120

top_left_x = (SCREEN_WIDTH - PLAYBLE_WIDTH) // 2
top_left_y = (SCREEN_HEIGHT - PLAYBLE_HEIGHT) // 2


def create_grid(locked_pos={}):
    grid = [[(0,0,0) for _ in range(10)] for _ in range(20)]

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if (j,i) in locked_pos:
                c = locked_pos[(j,i)]
                grid[i][j] = c
    return grid

def convert_shape_format(shape):
    positions = []
    direction = shape.shape[shape.rotation % len(shape.shape)]

    for i, line in enumerate(direction):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                positions.append((shape.x + j, shape.y + i))

    for i, pos in enumerate(positions):
        positions[i] = (pos[0] - 2, pos[1] - 4)

    return positions

def valid_space(shape, grid):
    accepted_positions = [[(j,i) for j in range(10) if grid[i][j] == (0,0,0)] for i in range(20)]
    accepted_positions = [j for sub in accepted_positions for j in sub]
    formatted = convert_shape_format(shape)

    for pos in formatted:
        if pos not in accepted_positions:
            if pos[1] > -1:
                return False
    return True

def is_lost(positions):
    for pos in positions:
        x, y = pos
        if y < 1:
            return True
    return False

def get_shape():
    shape = random.choice(shape_list)
    color = random.choice(shape_colors)
    return Piece(5, 0, shape, color)

def draw_text_middle(text, size, color, surface):
    font = pygame.font.SysFont('tahoma', size, bold=True)
    label = font.render(text, 1, color) # just need label rect size.
    draw_text(text, size, top_left_x + PLAYBLE_WIDTH / 2 - (label.get_width() / 2), top_left_y + PLAYBLE_HEIGHT / 2 - label.get_height() / 2, color, surface)

def draw_text(text, size, x, y, color, surface):
    font = pygame.font.SysFont('tahoma', size, bold=True)
    label = font.render(text, 1, color)

    surface.blit(label, (x, y))

def draw_grid(surface, row, col):
    sx = top_left_x
    sy = top_left_y
    for i in range(row):
        pygame.draw.line(surface, (128,128,128), (sx, sy + i * BLOCKSIZE), (sx + PLAYBLE_WIDTH, sy + i * BLOCKSIZE))
        for j in range(col):
            pygame.draw.line(surface, (128,128,128), (sx + j * BLOCKSIZE, sy), (sx + j * BLOCKSIZE, sy + PLAYBLE_HEIGHT))

def clear_rows(grid, locked):
    inc = 0
    for i in range(len(grid)-1, -1, -1):
        row = grid[i]
        if (0,0,0) not in row:
            inc += 1
            ind = i
            for j in range(len(row)):
                try:
                    del locked[(j,i)]
                except:
                    continue
    if inc > 0:
        for key in sorted(list(locked), key=lambda x: x[1])[::-1]:
            x, y = key
            if y < ind:
                newKey = (x, y + inc)
                locked[newKey] = locked.pop(key)
    return inc

def draw_next_shape(shape, surface):
    font = pygame.font.SysFont('tahoma', 30)
    label = font.render('Next Shape', 1, (255,255,255))

    sx = top_left_x + PLAYBLE_WIDTH + 50
    sy = top_left_y + PLAYBLE_HEIGHT / 3 - label.get_height() / 3
    direction = shape.shape[shape.rotation % len(shape.shape)]

    for i, line in enumerate(direction):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                pygame.draw.rect(surface, shape.color, (sx + j * BLOCKSIZE, sy + i * BLOCKSIZE, BLOCKSIZE, BLOCKSIZE), 0)

    surface.blit(label, (sx + 10, sy - 40))

def draw_window(surface):
    surface.fill((0,0,0))
    #title
    font = pygame.font.SysFont('tahoma', 60)
    label = font.render('Tetris', 1, (255,255,255))
    surface.blit(label, (top_left_x + PLAYBLE_WIDTH / 2 - (label.get_width() / 2), 30))

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            pygame.draw.rect(surface, grid[i][j], (top_left_x + j * BLOCKSIZE, top_left_y + i * BLOCKSIZE, BLOCKSIZE, BLOCKSIZE), 0)

    draw_grid(surface, 20, 10)
    pygame.draw.rect(surface, (255,0,0), (top_left_x, top_left_y, PLAYBLE_WIDTH, PLAYBLE_HEIGHT), 4)
    #pygame.display.update()

def main():
    global grid

    locked_positions = {}
    grid = create_grid(locked_positions)

    change_piece = False
    running = True
    current_piece = get_shape()
    next_piece = get_shape()
    clock = pygame.time.Clock()
    fall_time = 0
    level_time = 0
    fall_speed = 0.27
    score = 0

    while running:
        grid = create_grid(locked_positions)
        fall_time += clock.get_rawtime()
        level_time += clock.get_rawtime()
        clock.tick(FPS)

        if level_time/1000 > 5:
            level_time = 0
            if fall_speed > 0.12:
                fall_speed -= 0.005

        if fall_time/1000 > fall_speed:
            fall_time = 0
            current_piece.y += 1
            if not(valid_space(current_piece, grid)) and current_piece.y > 0:
                current_piece.y -= 1
                change_piece = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_piece.x -= 1
                    if not(valid_space(current_piece, grid)):
                        current_piece.x += 1
                if event.key == pygame.K_RIGHT:
                    current_piece.x += 1
                    if not(valid_space(current_piece, grid)):
                        current_piece.x -= 1
                if event.key == pygame.K_DOWN:
                    current_piece.y += 1
                    if not(valid_space(current_piece, grid)):
                        current_piece.y -= 1
                if event.key == pygame.K_UP:
                    current_piece.rotation += 1
                    if not(valid_space(current_piece, grid)):
                        current_piece.rotation -= 1
                if event.key == pygame.K_SPACE:
                    while valid_space(current_piece, grid):
                        current_piece.y += 1
                    current_piece.y -= 1
                    
        shape_pos = convert_shape_format(current_piece)

        for i in range(len(shape_pos)):
            x, y = shape_pos[i]
            if y > -1:
                grid[y][x] = current_piece.color

        if change_piece:
            for pos in shape_pos:
                p = (pos[0], pos[1])
                locked_positions[p] = current_piece.color
            current_piece = next_piece
            next_piece = get_shape()
            change_piece = False
            score += clear_rows(grid, locked_positions) * 10

        draw_window(win)
        draw_next_shape(next_piece, win)
        pygame.display.update()

        if is_lost(locked_positions):
            draw_text_middle("You Lost", 40, (255,255,255), win)
            pygame.display.update()
            pygame.time.delay(2000)
            runnig = False

    draw_text("Score: " + str(score), 40, top_left_x, top_left_y, (255,255,255), win)
    
    pygame.display.update()
    pygame.time.delay(2000)

def main_menu():
    running = True
    while running:
        win.fill((0,0,0))
        draw_text_middle("Press Any Key To Play", 60, (255,255,255), win)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                main()

        sleep(0.5) # just to make things  less intensive

if __name__ == '__main__':
    win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Tetris')
    main_menu()