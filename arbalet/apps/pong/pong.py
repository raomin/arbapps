#!/usr/bin/env python
"""
    Arbalet - ARduino-BAsed LEd Table
    pong game
    
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
player_WIDTH = 4
player_SPEED =1

class Pong(object):
    
    def __init__(self, height, width):
        self.score_p1=0
        self.score_p2=0
        
        self.height = height
        self.width = width

        self.all_sprites_group = pygame.sprite.Group()
        self.players_bricks_group = pygame.sprite.Group()
        self.bricks_group = pygame.sprite.Group()

        
        # add sprites to their group
    
        self.player1 = BOSprite('cyan',player_WIDTH,1 )
        self.player2 = BOSprite('cyan',player_WIDTH,1 )
        

        self.all_sprites_group.add(self.player1)
        self.players_bricks_group.add(self.player1)
        self.all_sprites_group.add(self.player2)
        self.players_bricks_group.add(self.player2)

        self.ball = BOSprite("red",1,1)
        self.ball.speed_x = -1
        self.ball.speed_y = -1
        self.all_sprites_group.add(self.ball)
        self.restart()

    def restart(self):
        self.player1.rect.bottom = self.height
        self.player1.rect.left = (self.width - self.player1.image.get_width()) / 2
        self.player2.rect.bottom = 1
        self.player1.rect.left = (self.width - self.player1.image.get_width()) / 2

        self.ball.rect.bottom = self.height // 2
        self.ball.rect.left = self.width // 2
        


    def update(self):
        self.check_hit()
        self.ball.rect = self.ball.rect.move(self.ball.speed_x,self.ball.speed_y)
        # bounce against borders
        if self.ball.rect.x > self.width - 2 or self.ball.rect.x < 1:
            self.ball.speed_x *= -1
        
        
    
    def move_left(self, player):
        if player.rect.left > 0:
            player.rect.move_ip(-player_SPEED, 0)
    def move_right(self,player):
        if player.rect.right < self.width:
            player.rect.move_ip(player_SPEED, 0)

    def check_hit(self):
        hits = pygame.sprite.spritecollide(self.ball, self.players_bricks_group, False)
        if hits:
            hit_rect = hits[0].rect
            # bounce the ball (according to side collided)
            if hit_rect.left > self.ball.rect.left or self.ball.rect.right <= hit_rect.right:
                self.ball.speed_y *= -1
            else:
                self.ball.speed_x *= -1


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

class PongApp(Application):
    def __init__(self):
        Application.__init__(self, touch_mode='quadridirectional')
        self.t0 = time.time()
        self.playing = True
        self.command = {'left': False, 'right': False,'left_p2': False, 'right_p2': False}  # User commands (joy/keyboard)
        self.pong = Pong(self.arbalet.height,self.arbalet.width )


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
                if event.key == pygame.K_RIGHT:
                    self.command['right'] = event.type == pygame.KEYDOWN
                elif event.key == pygame.K_LEFT:
                    self.command['left'] = event.type == pygame.KEYDOWN
                elif event.key == pygame.K_s:
                    self.command['left_p2'] = event.type == pygame.KEYDOWN
                elif event.key == pygame.K_f:
                    self.command['right_p2'] = event.type == pygame.KEYDOWN

        for event in self.arbalet.touch.get(): #event['type'] => Key UP or DOWN
            if event['key'] == 'down':
                self.command['down'] = event['type'] == 'down'
            elif event['key'] == 'right':
                self.command['right'] = event['type'] == 'down'
            elif event['key'] == 'left':
                self.command['left'] = event['type'] == 'down'

        if self.command['left']:
            self.pong.move_left(self.pong.player1)
        elif self.command['right']:
            self.pong.move_right(self.pong.player1)
        elif self.command['right_p2']:
            self.pong.move_right(self.pong.player2)
        elif self.command['left_p2']:
            self.pong.move_left(self.pong.player2)

    def update_view(self):
        self.pong.update()
        self.pong.all_sprites_group.update()

        surf = pygame.Surface((self.width,self.height))
        font = pygame.font.SysFont("freesans", 8)
        text = font.render(str(self.pong.score_p1), True, pygame.Color('white'))
        surf.blit(text,(3,self.height-10))

        text = font.render(str(self.pong.score_p2), True, pygame.Color('white'))
        surf.blit(text,(3,3))

        self.pong.all_sprites_group.draw(surf)
        
        #From pygame surf to arbalet model
        with self.model:
            for w in range(self.width):
                for h in range(self.height):
                    self.model.set_pixel(h, w, surf.get_at((w,h)).normalize()[0:3])

    def check_winner(self):
        if (self.pong.score_p2==10) or self.pong.score_p1 == 10:
            self.playing=False

    def run(self):
        while self.playing:
            self.process_events()
            self.update_view()
            self.process_events()

            if (self.pong.ball.rect.y in [self.arbalet.height, -1] ):#ball missed
                if self.pong.ball.rect.y < 0:
                    self.pong.score_p1 +=1
                else:
                    self.pong.score_p2 +=1
                self.model.flash(2,5)
                self.check_winner()
                self.t0 = time.time()

                self.pong.restart()
            
            else:
                time.sleep(max(0.05,0.2-(time.time()-self.t0)/(self.height*self.width*.5)))

        # Game over
        if self.pong.score_p2==10:
            self.model.write("Player 2 wins", 'deeppink',speed=30)
        else:
            self.model.write("Player 1 wins", 'deeppink',speed=30)