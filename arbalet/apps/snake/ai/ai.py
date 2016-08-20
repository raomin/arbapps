#!/usr/bin/env python
"""
    Simple snake AI
    License: GPL version 3 http://www.gnu.org/licenses/gpl.html

    Arbalet - ARduino-BAsed LEd Table
    Copyright 2015 Yoan Mollard - Arbalet project - http://github.com/arbalet-project
    License: GPL version 3 http://www.gnu.org/licenses/gpl.html
"""
from arbalet.core import Arbapixel
from ..snake import Snake, LEFT, RIGHT, UP, DOWN
from numpy import zeros, array
from numpy.linalg import norm


class SnakeAI(Snake):
    FOOD = Arbapixel(Snake.FOOD_COLOR)
    BODY = Arbapixel(Snake.PIXEL_COLOR)
    
    SCORE_FOOD_ATTRACTION = 100
    SCORE_FOOD_TARGET = 500
    SCORE_BODY_ATTRACTION = -5
    SCORE_BODY_TARGET = -500
    
    def __init__(self, argparser):
        Snake.__init__(self, argparser, touch_mode='off')
        self.potential_field = zeros((self.height, self.width))

    def process_extras(self):
        self.update_potential_field() # Update for visu only # TODO Lock model to avoid black flashing at high speed
        for h in range(self.height):
            for w in range(self.width):
                if self.model.get_pixel(h, w) not in [SnakeAI.FOOD, SnakeAI.BODY] :
                    color = Arbapixel('white')*(self.potential_field[h, w]/100)  # TODO find better brightness adaption
                    self.model.set_pixel(h, w, color)
    
    
    def update_potential_field(self):
        for h in range(self.height):
            for w in range(self.width):
                pixel = array((h, w))
                score = 0
                if self.model.get_pixel(h, w) == SnakeAI.FOOD:
                    score = SnakeAI.SCORE_FOOD_TARGET
                elif self.model.get_pixel(h, w) == SnakeAI.BODY:
                    score = SnakeAI.SCORE_BODY_TARGET
                else:
                    for food in self.FOOD_POSITIONS:
                        food = array(food)
                        distance = norm(food - pixel)
                        score += SnakeAI.SCORE_FOOD_ATTRACTION/distance
                    for body in self.queue:
                        body = array(body)
                        distance = norm(food - pixel)
                        score += SnakeAI.SCORE_BODY_ATTRACTION/distance
                self.potential_field[h, w] = score           
    
    def process_events(self):
        self.update_potential_field()
        directions = {'left': (0, -1), 'up': (-1, 0), 'right': (0, 1), 'down':(1, 0)}
        max_score = -float('inf')
        for name, direction in directions.items():
            next_x = (self.HEAD[0] + direction[0])%self.height
            next_y = (self.HEAD[1] + direction[1])%self.width
            score = self.potential_field[next_x][next_y]
            print("Decision {} has a score of {}".format(name, score))
            if score > max_score:
                max_score = score
                decision = direction
                decision_name = name
        print("Choosen decision {} score {}".format(decision_name, max_score))
        self.DIRECTION = decision

