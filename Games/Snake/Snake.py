from hashlib import new
from time import time
import turtle
import time
import random

# starting delay for each round
start_delay = 0.4
# current variable values
delay = start_delay
score = 0
high_score = 0
# snake body parts
segments = []
#screen and sprites
window = turtle.Screen()
head = turtle.Turtle()
food = turtle.Turtle()
pen = turtle.Turtle()

# movement of the snake
def go_up():
    if head.direction != "down":
        head.direction = "up"

def go_down():
    if head.direction != "up":
        head.direction = "down"

def go_left():
    if head.direction != "right":
        head.direction = "left"

def go_right():
    if head.direction != "left":
        head.direction = "right"

def move():
    if head.direction == "up":
        y = head.ycor()
        head.sety(y + 20)
    
    if head.direction == "down":
        y = head.ycor()
        head.sety(y - 20)

    if head.direction == "left":
        x = head.xcor()
        head.setx(x - 20)

    if head.direction == "right":
        x = head.xcor()
        head.setx(x + 20)

def writescore(score, high_score):
    pen.clear()
    pen.write(f"Score: {score} High Score: {high_score}", align="center", font=("Courier", 24, "normal"))

def death():
    time.sleep(1)
    head.goto(0, 0)
    head.direction = "stop"

    for segment in segments:
        segment.goto(1000, 1000)

    segments.clear()

    score = 0

    delay = start_delay

    writescore(score, high_score)

def spawnFood(x, y, colors, shapes):
    food.color(colors)
    food.shape(shapes)
    food.goto(x, y)

def gamesetup():
    # setting up the screen
    
    window.title("Snake Game")
    window.bgcolor("dark green")
    window.setup(width=600, height=600)
    window.tracer(0)

    # creating the head of the snake
    
    head.shape("square")
    head.color("black")
    head.penup()
    death()

    # creating the food
    food.speed(0)
    colors = random.choice(["red", "green", "blue", "yellow", "orange", "purple"])
    shapes = random.choice(["circle", "square", "triangle", "classic"])
    food.penup()
    spawnFood(0, 100, colors, shapes)
    

    # text for the display
    
    pen.speed(0)
    pen.shape("square")
    pen.color("white")
    pen.penup()
    pen.hideturtle()
    pen.goto(0, 260)
    writescore(score, high_score)

    # keyboard bindings
    window.listen()
    window.onkeypress(go_up, "w")
    window.onkeypress(go_down, "s")
    window.onkeypress(go_left, "a")
    window.onkeypress(go_right, "d")

gamesetup()

#game loop
while True:
    window.update()

    #check for death
    if head.xcor() > 290 or head.xcor() < -290 or head.ycor() > 290 or head.ycor() < -290:
        death()
    
    # check for eating the food
    if head.distance(food) < 20:
        x = random.randint(-270, 270)
        y = random.randint(-270, 270)
        colors = random.choice(["red", "green", "blue", "yellow", "orange", "purple"])
        shapes = random.choice(["circle", "square", "triangle", "classic"])
        spawnFood(x, y, colors, shapes)

        new_segment = turtle.Turtle()
        new_segment.speed(0)
        new_segment.shape("square") 
        new_segment.color("grey")
        new_segment.penup()
        segments.append(new_segment)
        delay -= 0.001
        score += 10
        if score > high_score:
            high_score = score
        
        writescore(score, high_score)
    
    #handle the body positioning
    for index in range(len(segments) - 1, 0, -1):
        x = segments[index - 1].xcor()
        y = segments[index - 1].ycor()
        segments[index].goto(x, y)
    
    if len(segments) > 0:
        x = head.xcor()
        y = head.ycor()
        segments[0].goto(x, y)
    
    #process movement
    move()
    
    #check for collision with the body
    for segment in segments:
        if segment.distance(head) < 20:
            death()
        
    time.sleep(delay)
