import colorsys
import time
from abc import ABC, abstractmethod
from turtle import Turtle, Screen

import numpy as np

screen = Screen() 
queue = []
screen_width = 1920
screen_height = 1080
screen.tracer(0) 
screen.setup(screen_width, screen_height)
hsv = (0.6, 100/360, 100/360)

class Plant(ABC):
    grammar: str
    t: Turtle
    def __init__(self, size: int, start_hsv: tuple, line_length: int, line_width: int, angle: float):
        self.size = size
        self.start_hsv = start_hsv
        self.line_length = line_length
        self.line_width = line_width
        self.angle = angle
        self.t = Turtle()
    @abstractmethod
    def mutate(self):
        pass

class draw_object:
    def __init__(self, position: tuple, color: tuple, heading: float, is_back: bool, width: int):
        self.position = position
        self.color = color
        self.heading = heading
        self.is_back = is_back
        self.width = width

def draw(plant: Plant):
    t = plant.t
    objs = []
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
    pos = t.pos()
    heading = t.heading()
    obj = draw_object((pos[0], pos[1], 0), color, heading, False, width)
    objs.append(obj)
    return objs

def rotate_y(angle, point):
    rotation_y = np.array([[np.cos(angle), 0, -np.sin(angle)],
                          [0, 1, 0],
                          [np.sin(angle), 0,  np.cos(angle)]])
    return np.matmul(rotation_y, point)

def project(point):
    projection = np.array([[1,0,0],[0,1,0]])
    return np.matmul(projection, point) 

def redraw(objs, string, plant):
    t = plant.t
    for i in range(len(objs)):
        obj = objs[i]
        t.width(obj.width)
        t.pencolor(obj.color)
        t.setheading(obj.heading)
        xyz = np.array(obj.position)
        if string[i] == "+" :
            rx, ry, rz = rotate_y(0, xyz)
            px, py = project(np.array([rx, ry, rz]))
            objs[i].position = (px, py, rz)
            t.goto(px, py)
        elif string[i] == "-":
            xy = np.array(obj.position)
            rx, ry, rz = rotate_y(0, xy)
            px, py = project(np.array([rx, ry, rz]))
            objs[i].position = (px, py, rz)
            t.goto(px, py)
        elif obj.is_back:
            t.penup()
            t.goto(obj.position[0], obj.position[1])
            t.pendown()
        else:
            t.goto(obj.position[0], obj.position[1])
    return objs

def rotate_obj(objs, angle):
    for obj in objs:
        xy = np.array(obj.position)
        rx, ry, rz = rotate_y(angle, xy)
        px, py = project(np.array([rx, ry, rz]))
        obj.position = (px, py, rz)
    return objs

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
    coords = []
    for _ in range(plant.size):
        line_length *= 0.5
        plant.line_length = line_length
        t.clear()
        t.width(width)
        coords = draw(plant)
        screen.update()
        plant.mutate()
        reset_start_position(plant, start_position)
    '''
    for _ in range(plant.size):
        angle = 2*pi/plant.size
        t.penup()
        t.home()
        t.sety(-1080/2 + 20)
        t.pendown()
        t.setheading(90)
        coords = rotate_obj(coords, angle)
        coords = redraw(coords, plant.grammar, angle)
        screen.update()
        time.sleep(0.1)
    '''

class P1(Plant):
    grammar = "G"

    def __init__(self, size, start_hsv, line_length, line_width, angle):
        super().__init__(size, start_hsv, line_length, line_width, angle)

    def mutate(self):
        mutated_grammar = ""
        for character in self.grammar:
            match character:
                case "F":
                    if(np.random.randint(2)) == 0 :
                        mutated_grammar += "FF"
                    else:
                        mutated_grammar += "FFF"
                case "G":
                    if(np.random.randint(2)) == 0 :
                        mutated_grammar += "FB"
                    else:
                        mutated_grammar += "FBB"
                case "B":
                    mutated_grammar += "[-FB][+FB]"
                case _:
                    mutated_grammar += character
        self.grammar = mutated_grammar
                    


class P2(Plant):
    grammar = "F"
    def __init__(self, size, start_hsv, line_length, line_width, angle):
        super().__init__(size, start_hsv, line_length, line_width, angle)
    def mutate(self):
        mutated_grammar = ""
        for character in self.grammar:
            match character:
                case "F":
                    if(np.random.randint(2)) == 0 :
                        mutated_grammar += "FF-[-F+F+F]+[+F-F-F]"
                    else:
                        mutated_grammar += "FF+[+F-F-F]-[-F+F+F]"
                case _:
                    mutated_grammar += character
        self.grammar = mutated_grammar


def make_forest(n):
    for _ in range(n):
        random_plant = np.random.randint(2)
        size = np.random.randint(5, 7)
        start_hsv = (np.random.random(), np.random.random(), np.random.random())
        line_length = np.random.randint(300, 600)
        line_width = np.random.randint(20)
        angle = np.random.random()*30
        start_postion = np.random.randint(-screen_width/2, screen_width/2)
        if random_plant == 1:
            plant = P1(size=size, start_hsv=start_hsv, line_length=line_length, line_width=line_width, angle=angle)
            l_systems(plant, start_postion)
        else:
            plant = P2(size=size, start_hsv=start_hsv, line_length=line_length, line_width=line_width, angle=angle)
            l_systems(plant, start_postion)
        time.sleep(0.5)
    screen.mainloop()

make_forest(100)
        
