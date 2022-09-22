import pygame
import math
from random import Random
from time import sleep

from components.brick import Brick
from components.paddle import Paddle
from components.ball import Ball

#basic set up
pygame.init()
velocity_mod = 0.8

SCREENWIDTH = 800
SCREENHEIGHT = 600
win = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
pygame.display.set_caption("Breakout")

#contsants
FPS = 60
PADDLE_WIDTH = 100
PADDLE_HEIGHT = 15
LIVES_FONT = pygame.font.SysFont("tahoma", 30)

def draw(win: pygame.Surface, paddle: Paddle, ball: Ball, bricks: list, lives: int, score: int, is_playing: bool):
    win.fill((0, 0, 0))
    paddle.draw(win)
    ball.draw(win)

    for brick in bricks:
        brick.draw(win)
    
    if not is_playing:
        display_text("Press space to play")
    else:
        draw_text("Score: " + str(score), 10, 10)
        draw_text("Lives: " + str(lives), SCREENWIDTH, 10)

    pygame.display.update()

def display_text(text: str) -> None:
    text = LIVES_FONT.render(text, 1, (255, 0, 0))
    win.blit(text, (SCREENWIDTH/2 - text.get_width()/2, SCREENHEIGHT/2 - text.get_height()))

def draw_text(text: str, x: int, y: int) -> None:
    text = LIVES_FONT.render(text, 1, (255, 255, 255))
    if y + text.get_height() > SCREENHEIGHT:
        y = SCREENHEIGHT - text.get_height() - 10
    if x + text.get_width() > SCREENWIDTH:
        x = SCREENWIDTH - text.get_width() - 10
    win.blit(text, (x, y))

def ball_collision(ball: Ball):
    if ball.x - ball.radius + 1 <= 0 or ball.x + ball.radius - 1 >= SCREENWIDTH:
        ball.set_velocity(-ball.x_velocity, ball.y_velocity)

    if ball.y - ball.radius <= 0 or ball.y + ball.radius >= SCREENHEIGHT:
        ball.set_velocity(ball.x_velocity, -ball.y_velocity)

def paddle_collision(ball: Ball, paddle: Paddle):
    if not (ball.x <= paddle.x + paddle.width and ball.x >= paddle.x):
        return
    if not (ball.y + ball.radius >= paddle.y):
        return

    paddle_center = paddle.x + paddle.width / 2
    distance_to_center = ball.x - paddle_center
    percent_width = distance_to_center / paddle.width

    angle = percent_width * 90
    angle_radians = math.radians(angle)

    x_velocity = math.sin(angle_radians) * ball.defalut_velocity
    y_velocity = -math.cos(angle_radians) * ball.defalut_velocity

    ball.set_velocity(x_velocity, y_velocity)

def generate_bricks(rows: int, cols: int) -> list:
    gap = 1
    brick_width = SCREENWIDTH // cols - gap 
    brick_height = 20

    bricks = []
    for row in range(rows):
        for col in range(cols):
            bricks.append(Brick(col * brick_width + gap * col, row * brick_height +
                          gap * row + brick_height, brick_width, brick_height, [(255, 0, 0), (0, 255, 0), (0, 0, 255)]))
    return bricks

def main() -> None:
    clock = pygame.time.Clock()
    paddle_x = SCREENWIDTH/2 - PADDLE_WIDTH/2
    paddle_y = SCREENHEIGHT - PADDLE_HEIGHT - 5
    paddle = Paddle(paddle_x, paddle_y, PADDLE_WIDTH, PADDLE_HEIGHT, (255, 255, 255))
    ball = Ball(SCREENWIDTH/2, paddle_y - PADDLE_HEIGHT, (255, 255, 255))
    bricks = generate_bricks(3, 10)
    lives = 3
    level = 1
    score = 0

    def reset() -> None:
        paddle.x = SCREENWIDTH/2 - PADDLE_WIDTH/2
        ball.x = SCREENWIDTH/2
        ball.y = paddle_y - PADDLE_HEIGHT - ball.radius
        #ball.set_velocity(0, -ball.defalut_velocity)

    running = True
    is_playing = False
    paddle_dir = 0
    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
                break

        keys = pygame.key.get_pressed()

        if not keys[pygame.K_RIGHT] and keys[pygame.K_LEFT] and paddle.x > 0:
            if paddle_dir == 0:
                paddle_dir = -1
                paddle.move(-paddle.defalut_velocity * velocity_mod)
            elif paddle_dir == 1:
                paddle_dir = -1
                paddle.move(-paddle.defalut_velocity * -velocity_mod)
            else:
                paddle.move(-paddle.defalut_velocity)
        elif not keys[pygame.K_LEFT] and keys[pygame.K_RIGHT] and paddle.x < SCREENWIDTH - PADDLE_WIDTH:
            if paddle_dir == 0:
                paddle_dir = 1
                paddle.move(paddle.defalut_velocity * velocity_mod)
            elif paddle_dir == -1:
                paddle_dir = 1
                paddle.move(paddle.defalut_velocity * -velocity_mod)
            else:
                paddle.move(paddle.defalut_velocity)
        elif keys[pygame.K_SPACE] and not is_playing:
            is_playing = True
        elif not keys[pygame.K_LEFT] and not keys[pygame.K_RIGHT]:
            paddle_dir = 0

        if is_playing:
            ball.move()
            ball_collision(ball)
            paddle_collision(ball, paddle)

            for brick in bricks[:]:
                brick.collision(ball)
                if not brick.is_alive():
                    score += level * 10
                    if score % 1000 == 0:
                        lives += 1
                    bricks.remove(brick)

            if len(bricks) == 0:
                display_text("You win!")
                sleep(1)
                reset()
                bricks = generate_bricks(3, 10)
                level += 1

            if ball.y + ball.radius >= SCREENHEIGHT:
                lives -= 1
                ball.x = paddle.x + paddle.width/2
                ball.y = paddle.y - PADDLE_HEIGHT - ball.radius

            if lives <= 0:
                display_text("You lose!")
                sleep(2)
                reset()
                bricks = generate_bricks(3, 10)
                lives = 3
                is_playing = False

        draw(win, paddle, ball, bricks, lives, score, is_playing)

    pygame.quit()
    quit()

if __name__ == "__main__":
    main()
