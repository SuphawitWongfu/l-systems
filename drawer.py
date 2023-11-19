import colorsys
import time
from turtle import Turtle, Screen
from plants import P1, P2, P3, P4, P5, P6, Plant

import numpy as np

screen = Screen() 
queue = []
screen_width = 1920
screen_height = 1080
screen.tracer(0) 
screen.setup(screen_width, screen_height)
hsv = (0.6, 100/360, 100/360)



def draw(plant: Plant):
    t = plant.t
    width = plant.line_width
    length = plant.line_length
    current_hsv = plant.start_hsv
    dv = 360/(plant.size + 1)
    angle = plant.angle
    color = colorsys.hsv_to_rgb(hsv[0], hsv[1], hsv[2])
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
                queue.append(package)
            case "]":
                width *= 1/0.8
                current_hsv = (current_hsv[0], current_hsv[1], ((((current_hsv[2]*360) - dv) + 360) % 360)/360)
                color = colorsys.hsv_to_rgb(current_hsv[0], current_hsv[1], current_hsv[2])
                t.pencolor(color)
                t.width(width)
                t.penup()
                position = queue.pop() 
                t.goto(position[0], position[1])
                t.setheading(position[2])
                t.pendown()

def reset_start_position(plant, start_position):
    t = plant.t
    t.penup()
    t.home()
    t.setx(start_position)
    t.sety(-1080 / 2 + 20)
    t.pendown()
    t.setheading(90)

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



def make_forest(n):
    for _ in range(n):
        random_plant = np.random.randint(6)
        size = np.random.randint(5, 7)
        start_hsv = (0.3, np.random.random(), np.random.random())
        line_length = np.random.randint(300, 600)
        line_width = np.random.randint(20)
        angle = np.random.random()*30
        start_postion = np.random.randint(-screen_width/2, screen_width/2)
        if random_plant == 1:
            plant = P1(size=size
                       , start_hsv=start_hsv
                       , line_length=line_length
                       , line_width=line_width
                       , angle=angle)
            l_systems(plant, start_postion)
        elif random_plant == 2:
            plant = P3(size=size
                       , start_hsv=start_hsv
                       , line_length=line_length
                       , line_width=line_width
                       , angle=angle)
            l_systems(plant, start_postion)
        elif random_plant == 3:
            plant = P4(size=size
                       , start_hsv=start_hsv
                       , line_length=line_length
                       , line_width=line_width
                       , angle=angle)
            l_systems(plant, start_postion)
        elif random_plant == 4:
            plant = P5(size=size
                       , start_hsv=start_hsv
                       , line_length=line_length
                       , line_width=line_width
                       , angle=angle)
            l_systems(plant, start_postion)
        elif random_plant == 5:
            plant = P6(size=size
                       , start_hsv=start_hsv
                       , line_length=line_length
                       , line_width=line_width
                       , angle=angle)
            l_systems(plant, start_postion)
        else:
            plant = P2(size=size
                       , start_hsv=start_hsv
                       , line_length=line_length
                       , line_width=line_width
                       , angle=angle)
            l_systems(plant, start_postion)
        time.sleep(0.3)
    screen.mainloop()

make_forest(10)
        
