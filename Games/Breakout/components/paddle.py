import pygame

class Paddle:
    defalut_velocity = 4

    def __init__(self, x: int, y: int, width: int, height: int, color: tuple) -> None:
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color

    def draw(self, win: pygame.Surface) -> None:
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))

    def move(self, direction:float=1.0) -> None:
        self.x += int(self.defalut_velocity * direction)