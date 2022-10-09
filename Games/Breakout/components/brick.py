import pygame
from components.ball import Ball

class Brick:
    def __init__(self, x: int, y: int, width: int, heigh: int, colors: tuple) -> None:
        self.x = x
        self.y = y
        self.width = width
        self.height = heigh
        self.colors = colors
        self.color = self.colors[0]
        self.hit_count = 0
        self.hit_count_max = len(self.colors)

    def draw(self, win: pygame.Surface):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))

    def hit(self):
        self.hit_count += 1
        if self.hit_count < self.hit_count_max:
            self.color = self.colors[self.hit_count]
        else:
            self.color = self.colors[-1]

    def collision(self, ball: Ball):
        if not (ball.x <= self.x + self.width and ball.x >= self.x):
            return False
        if not (ball.y <= self.y + self.height and ball.y >= self.y):
            return False

        self.hit()
        #depends on where it hit.... did it hit a side or bototm or top?
        ball.set_velocity(ball.x_velocity, -ball.y_velocity)
        return True
    
    def is_alive(self):
        return self.hit_count < self.hit_count_max
