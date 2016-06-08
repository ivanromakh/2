import pygame
from pygame import *
from settings import *
import math

class Bullets(sprite.Sprite):
    def __init__(self, start, end, atack, plid, num):
        sprite.Sprite.__init__(self)
        self.rect = Rect(start[0], start[1], BUL_SIZE, BUL_SIZE)
        #ZOOM AND NAME
        self.num = num
        self.atack = atack
        # surfaces
        self.id = plid

        # position for move
        self.start = start
        self.end = end
        
        # SPEED VECTOR
        self.xvel = 0.0
        self.yvel = 0.0
        
        # DISTANCE FOR BEGIN
        self.posx = end[0] - start[0] + 0.0
        self.posy = end[1] - start[1] + 0.0

        #SPEED 
        self.velocity = VELOCITY
        self.size = BUL_SIZE

        #time from start
        self.time = time.get_ticks()
        self.mathxy = math.fabs(end[0] - start[0])+math.fabs(end[1] - start[1]) 
            
        # SPEED VECTOR FOR BULLET FLY    
        if self.mathxy != 0:
            self.xvel = self.velocity*(self.posx)/self.mathxy
            self.yvel = self.velocity*(self.posy)/self.mathxy
        
    def updat(self):
        # destroy at some time 
        if self.time + BULTIME <= time.get_ticks():
            self.kill()
        # BULLET FLY
        self.rect.x = self.rect.x + self.xvel
        self.rect.y = self.rect.y + self.yvel
        
