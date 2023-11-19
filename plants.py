from abc import ABC, abstractmethod
from turtle import Turtle
import numpy as np

'''
This file contains plant types which are defined as classes
'''
class Plant(ABC):
    # the string of symbols use to draw
    grammar: str
    # each plant has their own turtle, so they can draw separately
    t: Turtle
    def __init__(self, size: int, start_hsv: tuple, line_length: int, line_width: int, angle: float):
        self.size = size
        self.start_hsv = start_hsv
        self.line_length = line_length
        self.line_width = line_width
        self.angle = angle
        self.t = Turtle()

    # apply its own rule to its own grammar to generate the new grammar
    @abstractmethod
    def mutate(self):
        pass

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

class P3(Plant):
    grammar = "F"
    def __init__(self, size, start_hsv, line_length, line_width, angle):
        super().__init__(size, start_hsv, line_length, line_width, angle)
    def mutate(self):
        mutated_grammar = ""
        for character in self.grammar:
            match character:
                case "F":
                    mutated_grammar += "F[+F]F[-F]F"
                case _:
                    mutated_grammar += character
        self.grammar = mutated_grammar

class P4(Plant):
    grammar = "F"
    def __init__(self, size, start_hsv, line_length, line_width, angle):
        super().__init__(size, start_hsv, line_length, line_width, angle)
    def mutate(self):
        mutated_grammar = ""
        for character in self.grammar:
            match character:
                case "F":
                    mutated_grammar += "F[+F]F[-F][F]"
                case _:
                    mutated_grammar += character
        self.grammar = mutated_grammar

class P5(Plant):
    grammar = "G"
    def __init__(self, size, start_hsv, line_length, line_width, angle):
        super().__init__(size, start_hsv, line_length, line_width, angle)
    def mutate(self):
        mutated_grammar = ""
        for character in self.grammar:
            match character:
                case "F":
                    mutated_grammar += "FF"
                case "G":
                    mutated_grammar += "F[+G]F[-G]+G"
                case _:
                    mutated_grammar += character
        self.grammar = mutated_grammar

class P6(Plant):
    grammar = "G"
    def __init__(self, size, start_hsv, line_length, line_width, angle):
        super().__init__(size, start_hsv, line_length, line_width, angle)
    def mutate(self):
        mutated_grammar = ""
        for character in self.grammar:
            match character:
                case "F":
                    mutated_grammar += "FF"
                case "G":
                    mutated_grammar += "F[+G][-G]FG"
                case _:
                    mutated_grammar += character
        self.grammar = mutated_grammar
