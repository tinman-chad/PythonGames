import pygame, sys
import random
from collections import deque
import utils.settings as settings
from components.cell import Cell

def next_cell(size: int, current, grid):
    '''Get random next valid neighboring cell'''
    i = current.x//size
    j = current.y//size

    opt = []
    # add to the list if cell is not visited
    # and also taking care of edge cases
    if i < rows-1 and not grid[i+1][j].visited:
        opt.append(grid[i+1][j])

    if i > 0 and not grid[i-1][j].visited:
        opt.append(grid[i-1][j])

    if j < cols-1 and not grid[i][j+1].visited:
        opt.append(grid[i][j+1])

    if j > 0 and not grid[i][j-1].visited:
        opt.append(grid[i][j-1])

    try:
        return random.choice(opt)
    except:
        return None

def save_JSON(grid):
    '''Save the maze for loading as new levels in game.'''
    with open("maze_.json", "w") as f:
        f.write("[\n")
        for x in grid:
            f.write("\t[\n")
            for y in x:
                f.write('\t\t'  + y.toJson() + ",\n")
            f.write("\t]\n")
        f.write("]\n")

def save_image(screen):
    '''Save image so I can print it and solve'''
    pygame.image.save(screen, "maze.jpg")

def main(width: int = 480, height: int = 480, size: int = 48, rows: int = 10, cols: int = 10):
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Maze Generator")
    clock = pygame.time.Clock()

    grid = []
    for i in range(rows):
        grid.append([])
        for j in range(cols):
            grid[i].append(Cell(i*size, j*size, size))

    current = grid[0][0]
    current.visited = True
    stack = deque()
    stack.append(current)

    running = True
    while running:
		# Process input (events)
        for event in pygame.event.get():
			# check for closing window
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
                save_JSON(grid)
                save_image(screen)

		# Update
        next_ = next_cell(size, current, grid)
        if next_ is None:
            try:
                current = stack.pop()
            except:
                pass
        else:
            current.break_walls(next_)
            current = next_
            current.visited = True
            stack.append(current)

		# Draw / render
        screen.fill(settings.BLUE)
        for i in range(rows):
            for j in range(cols):
                grid[i][j].draw(screen)
        pygame.display.flip()
        clock.tick(settings.FPS)

if __name__ == '__main__':
    size = settings.size
    rows = settings.rows
    cols = settings.cols
    args = sys.argv[1:]
    for arg in args:
        if "size=" in arg:
            size = int(arg.replace('size=', ''))
        elif "rows=" in arg:
            rows = int(arg.replace('rows=', ''))
        elif "cols=" in arg:
            cols = int(arg.replace("cols=", ''))
    width = rows*size
    height = cols*size
    main(width, height, size, rows, cols)