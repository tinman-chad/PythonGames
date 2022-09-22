import pygame

class Ball:
    defalut_velocity = 5
    radius = 10
    
    def __init__(self, x: int, y: int, color: tuple) -> None:
        self.x = x
        self.y = y - self.radius #need to account for ball size
        self.color = color
        self.x_velocity = 0
        self.y_velocity = -self.defalut_velocity

    def draw(self, win: pygame.Surface) -> None:
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)

    def move(self):
        self.x += self.x_velocity
        self.y += self.y_velocity

    def set_velocity(self, x_velocity, y_velocity):
        self.x_velocity = x_velocity
        self.y_velocity = y_velocity

    def draw(self, win: pygame.Surface) -> None:
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)