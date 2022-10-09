import pygame
import json
import utils.settings as settings

class Cell:
    def __init__(self, x:int, y:int, size:int = 48, thickness:int = 3):
        self.x = x
        self.y = y
        self.cellSize = size
        self.w = x + self.cellSize
        self.h = y + self.cellSize
        self.thickness = thickness
        self.visited = False
        self.walls = {'top':True, 'right':True, 'bottom':True, 'left':True}

    def break_walls(self, other):
        if other.x < self.x :
            self.walls['left'] = False
            other.walls['right'] = False

        if other.x > self.x :
            self.walls['right'] = False
            other.walls['left'] = False

        if other.y < self.y :
            self.walls['top'] = False
            other.walls['bottom'] = False

        if other.y > self.y :
            self.walls['bottom'] = False
            other.walls['top'] = False

    def draw(self, screen:pygame.Surface):
        if self.visited:
            pygame.draw.rect(screen, settings.WHITE, (self.x, self.y, self.cellSize, self.cellSize))

        if self.walls['top']:
            pygame.draw.line(screen, settings.BLACK, (self.x, self.y),(self.w, self.y), self.thickness)
        if self.walls['right']:
            pygame.draw.line(screen, settings.BLACK, (self.w, self.y),(self.w, self.h), self.thickness)
        if self.walls['bottom']:
            pygame.draw.line(screen, settings.BLACK, (self.w, self.h),(self.x, self.h), self.thickness)
        if self.walls['left']:
            pygame.draw.line(screen, settings.BLACK, (self.x, self.h),(self.x, self.y), self.thickness)

    #this could be replicated to any class to make easy json output.
    def toJson(self) -> str:
        return json.dumps(self.__dict__, ensure_ascii=False)
    def to_json(self) -> str:
        return self.toJson()
    def __str__(self) -> str:
        return self.toJson()
    def __repr__(self) -> str:
        return self.__str__()
    def __iter__(self):
        yield from self.__dict__.items()