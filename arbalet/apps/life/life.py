#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Arbalet - ARduino-BAsed LEd Table
    Life - Generate a game of life

    Author - Raomin - http://github.com/arbalet-project
    License: GPL version 3 http://www.gnu.org/licenses/gpl.html
"""
from random import randint, uniform, choice
from arbalet.core import Application, Rate
import os, sys, inspect
from numpy import array
import time
import copy
from sys import exit
from table import Table


class Life(Application):

    def __init__(self, parser, rate):
        Application.__init__(self, parser)
        self.rate = Rate(rate)
        self.t = Table(self.height, self.width, 3)
        print(self.t.table)


    def close(self, reason='unknown'):
        Application.close(self, reason)


    def render(self):
        with self.model:
            self.model.set_all('black')
            self.model.data_frame
            for y in range(0, self.height):
                for x in range(0, self.width):
                    if (self.t.table[y][x]==1):
                        self.model.set_pixel(y,x,array((uniform(0, 1),uniform(0, 1),uniform(0, 1))))

    def turn(self):
        """Turn"""
        nt = copy.deepcopy(self.t.table)
        with self.model:
            self.model.set_all('black')
            self.model.data_frame
            for y in range(0, self.height):
                for x in range(0, self.width):
                    neighbours = self.t.liveNeighbours(y, x)
                    if self.t.table[y][x] == 0:
                        if neighbours == 3:
                            nt[y][x] = 1
                    else:
                        if (neighbours < 2) or (neighbours > 3):
                            nt[y][x] = 0
            self.t.table = nt

    def run(self):
        while True:
            self.turn()
            self.render()
            for i in range(10):
                self.rate.sleep()
