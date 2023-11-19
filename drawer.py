import colorsys
import time
from turtle import Screen

import numpy as np

from plants import P1, P2, P3, P4, P5, P6, Plant

'''
this file contain all drawing logic, including setting up screen and drawing using turtle
'''

screen = Screen()
screen_width = 1920
screen_height = 1080
screen.tracer(0) 
screen.setup(screen_width, screen_height)


'''
this function receives a plant class instance as an input and draw it
'''
def draw(plant: Plant):
    stack = []
    t = plant.t
    width = plant.line_width
    length = plant.line_length
    current_hsv = plant.start_hsv
    dv = 360/(plant.size + 1)
    angle = plant.angle
    color = colorsys.hsv_to_rgb(current_hsv[0],current_hsv[1], current_hsv[2])
    t.pencolor(color)
    for c in plant.grammar:
        match c:
            case "F":
                t.forward(length)
            case "G":
                t.forward(length)
            case "B":
                t.forward(length)
            case "+":
                if np.random.randint(2):
                    t.right(angle)
                else:
                    t.right(angle + 5)
            case "-":
                if np.random.randint(2):
                    t.left(angle)
                else:
                    t.left(angle + 5)
            case "[":
                width *= 0.8
                current_hsv = (current_hsv[0], current_hsv[1], (((current_hsv[2] * 360) + dv)% 360)/360)
                color = colorsys.hsv_to_rgb(current_hsv[0], current_hsv[1], current_hsv[2])
                t.pencolor(color)
                t.width(width)
                position = t.pos()
                heading = t.heading()
                package = (position[0], position[1], heading) 
                stack.append(package)
            case "]":
                width *= 1/0.8
                current_hsv = (current_hsv[0], current_hsv[1], ((((current_hsv[2]*360) - dv) + 360) % 360)/360)
                color = colorsys.hsv_to_rgb(current_hsv[0], current_hsv[1], current_hsv[2])
                t.pencolor(color)
                t.width(width)
                t.penup()
                position = stack.pop()
                t.goto(position[0], position[1])
                t.setheading(position[2])
                t.pendown()

'''
this function resets the turtle position to the beginning position according to the given start_position
'''
def reset_start_position(plant, start_position):
    t = plant.t
    t.penup()
    t.home()
    t.setx(start_position)
    t.sety(-1080 / 2 + 20)
    t.pendown()
    t.setheading(90)

'''
This function keeps applying the rules in each plant instances and draw them for plant.size iterations
'''
def l_systems(plant, start_position):
    t = plant.t
    line_length = plant.line_length
    width = plant.line_width
    reset_start_position(plant, start_position)
    for _ in range(plant.size):
        line_length *= 0.5
        plant.line_length = line_length
        t.clear()
        t.width(width)
        draw(plant)
        screen.update()
        plant.mutate()
        reset_start_position(plant, start_position)


'''
this function randomly generate n plants with random parameters.
'''
def make_forest(n, plants=None):
    if plants is None:
        plants = [P1, P2, P3, P4, P5, P6]
    for _ in range(n):
        random_plant = np.random.randint(len(plants))
        size = np.random.randint(5, 7)
        start_hsv = (0.3, np.random.random(), np.random.random())
        line_length = np.random.randint(300, 600)
        line_width = np.random.randint(20)
        angle = np.random.random()*30
        start_postion = np.random.randint(-screen_width/2, screen_width/2)
        plant = plants[random_plant](size=size
                        , start_hsv=start_hsv
                       , line_length=line_length
                        , line_width=line_width
                        , angle=angle)
        l_systems(plant, start_postion)
        time.sleep(0.5)

'''
this function draw all currently available 6 type of trees
'''
def display():
    plant_1 = P1(size=6
                 , start_hsv=(0.3, 100/360, 100/360)
                 , line_length=600
                 , line_width=15
                 , angle=25.7)

    plant_2 = P2(size=6
                 , start_hsv=(0.3, 100/360, 100/360)
                 , line_length=600
                 , line_width=15
                 , angle=22.5)

    plant_3 = P3(size=6
                 , start_hsv=(0.3, 100/360, 100/360)
                 , line_length=600
                 , line_width=10
                 , angle=25.7)

    plant_4 = P4(size=6
                 , start_hsv=(0.3, 100/360, 100/360)
                 , line_length=600
                 , line_width=15
                 , angle=25.7)

    plant_5 = P5(size=6
                 , start_hsv=(0.3, 100/360, 100/360)
                 , line_length=600
                 , line_width=15
                 , angle=25.7)

    plant_6 = P6(size=7
                 , start_hsv=(0.3, 100/360, 100/360)
                 , line_length=600
                 , line_width=10
                 , angle=25.7)

    l_systems(plant_1, -screen_width/2 + 200)
    l_systems(plant_2, -screen_width/2 + 600)
    l_systems(plant_3, 0)
    l_systems(plant_4, 200)
    l_systems(plant_5, screen_width/2 - 600)
    l_systems(plant_6, screen_width/2 - 200)

#unccommnet display() to see all available type of trees
#display()
make_forest(100)
screen.mainloop()
        
