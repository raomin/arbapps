#!/usr/bin/env python
"""
    Arbalet - ARduino-BAsed LEd Table
    Breakout game
    
    Raomin - from 
    Copyright 2015 Yoan Mollard - Arbalet project - http://github.com/arbalet-project
    License: GPL version 3 http://www.gnu.org/licenses/gpl.html
    """
import time
import random
import numpy
import pygame

from arbalet.core import Application

BRICK_HEIGHT = 1
BRICK_WIDTH = 2
PLAYER_WIDTH = 4
PLAYER_SPEED =1

class Breakout(object):
    colors = ['cyan', 'green', 'deeppink', 'yellow', 'orangered']

    def __init__(self, height, width):
        self.score = 0
        
        self.height = height
        self.width = width

        self.all_sprites_group = pygame.sprite.Group()
        self.player_bricks_group = pygame.sprite.Group()
        self.bricks_group = pygame.sprite.Group()

        
        # add sprites to their group
    
        self.player = BOSprite('cyan',PLAYER_WIDTH,1 )
        
        self.player.rect.bottom = height
        self.player.rect.left = (width - self.player.image.get_width()) / 2

        self.all_sprites_group.add(self.player)
        self.player_bricks_group.add(self.player)

        self.ball = BOSprite("red",1,1)
        self.ball.speed_x = -1
        self.ball.speed_y = -1
        self.ball.rect.bottom = height - 2
        self.ball.rect.left = width / 2
        self.all_sprites_group.add(self.ball)

        for i in xrange((width//(BRICK_WIDTH)-1)):
            for j in xrange(int(height*0.6)): #bricks to 60% of height
                
                c = pygame.Color(0,0,0,0)
                c.hsva=(360//int(height*0.6)*(j) ,100,100,100)
                brick = BOSprite(c, BRICK_WIDTH , BRICK_HEIGHT)
                brick.rect.left = i * (BRICK_WIDTH ) +1
                brick.rect.bottom = j * (BRICK_HEIGHT) + 1

                self.all_sprites_group.add(brick)
                self.bricks_group.add(brick)
                self.player_bricks_group.add(brick)

    def update(self):
        self.check_hit()
        self.ball.rect = self.ball.rect.move(self.ball.speed_x,self.ball.speed_y)
        # bounce against borders
        if self.ball.rect.x > self.width - 2 or self.ball.rect.x < 1:
            self.ball.speed_x *= -1
        if self.ball.rect.y < 1:
            self.ball.speed_y *= -1
        
        
    
    def move_left(self):
        if self.player.rect.left > 0:
            self.player.rect.move_ip(-PLAYER_SPEED, 0)
    def move_right(self):
        if self.player.rect.right < self.width:
            self.player.rect.move_ip(PLAYER_SPEED, 0)

    def check_hit(self):
        hits = pygame.sprite.spritecollide(self.ball, self.player_bricks_group, False)
        if hits:
            hit_rect = hits[0].rect
            # bounce the ball (according to side collided)
            if hit_rect.left > self.ball.rect.left or self.ball.rect.right <= hit_rect.right:
                self.ball.speed_y *= -1
            else:
                self.ball.speed_x *= -1

            # collision with blocks
            if pygame.sprite.spritecollide(self.ball, self.bricks_group, True):
                self.score += len(hits)
                print "Score: %s" % self.score

class BOSprite(pygame.sprite.Sprite):
    # Constructor. Pass in the color of the block,
    # and its x and y position
    def __init__(self, color, width, height):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)

        # Create an image of the block, and fill it with color.
        self.image = pygame.Surface([width, height])
        if isinstance(color,str):
            color = pygame.Color(color)
        self.image.fill(color)

        # Fetch the rectangle object that has the dimensions of the image
        # Update the position of this object by setting the values of rect.x and rect.y
        self.rect = self.image.get_rect()

class BreakOutApp(Application):
    def __init__(self):
        Application.__init__(self, touch_mode='quadridirectional')
        self.score = 0
        self.t0 = time.time()
        self.playing = True
        self.command = {'left': False, 'right': False, 'down': False}  # User commands (joy/keyboard)
        self.breakout = Breakout(self.arbalet.height,self.arbalet.width )

    def process_events(self):
        """
        Sleep until the next step and process user events: game commands + exit
        Previous commands are kept into account and extended events (i.e. a key stayed pressed) are propagated
        :return: True if user asked to abort sleeping (accelerate or quit), False otherwise
        """
        # Process new events
        for event in self.arbalet.events.get():
            # Joystick control
            if event.type == pygame.JOYHATMOTION:
                if event.value[0] == 1:
                    self.command['right'] = True
                elif event.value[0] == -1:
                    self.command['left'] = True
                elif event.value[0] == 0:
                    self.command['left'] = False
                    self.command['right'] = False
            # Keyboard control
            elif event.type in [pygame.KEYDOWN, pygame.KEYUP]:
                if event.key == pygame.K_DOWN:
                    self.command['down'] = event.type == pygame.KEYDOWN
                elif event.key == pygame.K_RIGHT:
                    self.command['right'] = event.type == pygame.KEYDOWN
                elif event.key == pygame.K_LEFT:
                    self.command['left'] = event.type == pygame.KEYDOWN

        for event in self.arbalet.touch.get(): #event['type'] => Key UP or DOWN
            if event['key'] == 'down':
                self.command['down'] = event['type'] == 'down'
            elif event['key'] == 'right':
                self.command['right'] = event['type'] == 'down'
            elif event['key'] == 'left':
                self.command['left'] = event['type'] == 'down'

        if self.command['left']:
            self.breakout.move_left()
        if self.command['right']:
            self.breakout.move_right()

    def update_view(self):
        self.breakout.update()
        self.breakout.all_sprites_group.update()

        surf = pygame.Surface((self.width,self.height))
        font = pygame.font.SysFont("freesans", 8)
        text = font.render(str(self.breakout.score), True, pygame.Color('white'))
        surf.blit(text,(3,self.height-10))

        self.breakout.all_sprites_group.draw(surf)
        
        with self.model:
            for w in range(self.width):
                for h in range(self.height):
                    self.model.set_pixel(h, w, surf.get_at((w,h)).normalize()[0:3])

    def run(self):
        while self.playing:
            self.process_events()
            self.update_view()
            self.process_events()
            if (self.breakout.ball.rect.y > self.arbalet.height) or len(self.breakout.bricks_group)==0 :#ball missed or no more bricks
                break
            else:
                time.sleep(max(0.05,0.3-(time.time()-self.t0)/(self.height*self.width)))

        # Game over
        self.model.flash(1,4)
        if len(self.breakout.bricks_group)==0:
            self.model.write("Bravo! Score final: {}".format(self.breakout.score), 'deeppink',speed=25)
        elif self.breakout.score > 0:
            self.model.write("GAME OVER! Score final: {}".format(self.breakout.score), 'deeppink',speed=25)