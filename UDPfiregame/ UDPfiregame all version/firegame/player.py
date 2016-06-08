import pygame
import math
from pygame import *
import random


from settings import *
from bullet import Bullets
from objectmoving import *
from mygame4 import enzooming


class Player(sprite.Sprite):
    def __init__(self, x, y, whoIam, ispart, ptype):
        sprite.Sprite.__init__(self)
        self.whoIam = whoIam
        self.rect = Rect(x, y, ZOOM, ZOOM)
        self.id = random.random()
        self.num = 0
        #zoom
        self.zoom = ZOOM
        # part or player    
        self.ispart = ispart
        self.ptype = ptype
        #coordianates surface
        if ispart == False: 
            self.rect.x = x
            self.rect.y = y
        else:
            self.rect.x = x
            self.rect.y = y
        #alfa
        self.alfa = 0
        if self.ptype == CANNON:
            # vectors of points
            self.vec1 = [self.rect.x, self.rect.y+ZOOM/2]
            self.vec2 = [self.rect.x + ZOOM, self.rect.y]
            self.vec3 = [self.rect.x + ZOOM, self.rect.y + ZOOM]
            self.points = [self.vec1, self.vec2, self.vec3]
            self.sendp = [self.vec1, self.vec2, self.vec3, self.id, False]
 
            self.myposx = 0.0
            self.myposy = 0.0
        #zoom popravka
        self.zoomx = 0.0
        self.zoomy = 0.0 
        # speed
        self.speed = float(SPEED)
        # if enemy
        if whoIam == False:
            self.health = ENHEALTH
            self.fradius = RANGE 
            self.radius = int(self.fradius)
            self.status = 0
            #zoom popravka float
            self.movex = 0.0
            self.movey = 0.0
            self.atack = CAN_ATACK
            self.plid = 0
        # if player
        if whoIam == True:
            self.health = PHEALTH
            #player vector
            self.movex = 0.0
            self.movey = 0.0
            self.ismoveup = False
            self.ismovedown = False
            self.isrotateleft = False
            self.isrotateright = False
            self.partposx = 0
            self.partposy = 0
            self.atack = CAN_ATACK
        # if it is part     
        if ispart == True:
            # angle
            if self.ptype == SHILD:
                self.shhealth = SHHEALTH
                # vectors of points
                self.vec1 = [self.rect.x, self.rect.y]
                self.vec2 = [self.rect.x + ZOOM, self.rect.y]
                self.vec3 = [self.rect.x + ZOOM, self.rect.y + ZOOM]
                self.vec4 = [self.rect.x, self.rect.y + ZOOM]
                self.points = [self.vec1, self.vec2, self.vec3, self.vec4]
                print self.points
                self.radius = SHHEALTH
                self.myposx = 0.0
                self.myposy = 0.0
            self.alfa = 0
            #zoom popravka float
            self.movex = 0.0
            self.movey = 0.0
            #position pasrt on player
            self.partposx = 0
            self.partposy = 0
            
    # draw poligon and cannon
    def draw(self, screen, pos, scale):
        if self.whoIam == False:
            pygame.draw.polygon(screen, EN_COLOR, self.points)
        else:
            x = enzooming(self.points, self.rect.center, self.myposx, self.myposy, scale)
            print x
            pygame.draw.polygon(screen, PL_COLOR, x)
        if self.ptype == CANNON:    
            pygame.draw.circle(screen, (0,0,250), self.rect.center, int(BUL_SIZE*scale), int(BUL_SIZE*scale))
        elif self.ptype == SHILD:
            pygame.draw.circle(screen, SH_COLOR, self.rect.center, self.radius, SH_THINK)
    
    # find new vector of speed
    # moving is cameramove in class Camera
    # moving is by this vector speed
    def shiftmove(self):
        self.sendp[0][0] = self.points[0][0] + self.myposx
        self.sendp[0][1] = self.points[0][1] + self.myposy
        self.sendp[1][0] = self.points[1][0] + self.myposx
        self.sendp[1][1] = self.points[1][1] + self.myposy 
        self.sendp[2][0] = self.points[2][0] + self.myposx
        self.sendp[2][1] = self.points[2][1] + self.myposy
        
    def move(self, speed):
        xy = math.fabs(self.points[0][0] - self.rect.center[0])+math.fabs(self.points[0][1] - self.rect.center[1])        
        x = 0
        y = 0
        if xy!=0:
            x = self.speed*(self.points[0][0] - self.rect.center[0])/xy
            y = self.speed*(self.points[0][1] - self.rect.center[1])/xy

        if self.whoIam == True:
            self.movex = x
            self.movey = y
            self.myposx += x
            self.myposy += y
            
        else:
            self.rect.x += x
            self.rect.y += y
            self.points[0][0] += x
            self.points[0][1] += y
            self.points[1][0] += x
            self.points[1][1] += y 
            self.points[2][0] += x
            self.points[2][1] += y
            
            self.rect = findcent(self.alfa, self.points, self.rect, self.ptype)
              
    # move on map, change zoom, rotate all objects and player
    def update(self, speed, zoom, player):

        # move on map
        if self.whoIam == False and speed !=0:     
              self.move(speed)
        
        # if he is a player
        # rotate or move  
        if self.whoIam == True and self.ispart == False:
            if self.ismoveup == True:
                self.move(speed*zoom)
            if self.ismovedown == True:
                self.move(-speed*zoom)
            if self.isrotateleft == True:
                self.rotate(-1,0)
            if self.isrotateright == True:
                self.rotate(1, 0)
        if self.ispart == True:
            if self.isrotateleft == True:
                self.rotate(-1, player)
            if self.isrotateright == True:
                self.rotate(1, player)
            
                
    # rotate object around the center    
    def rotate(self, x, player):
        alfa = 0
        # increase all point angles
        if x>0:
            self.alfa += ALFA
            alfa = ALFA
        elif x<0:
            self.alfa -= ALFA
            alfa = -ALFA
        if alfa != 0:
            if self.ispart == True:
                #rotate poligon points
                self.points = rotatepoints(player.rect.center, self.points, alfa)
                self.rect = findcent(self.alfa, self.points, self.rect, self.ptype)
            else:    
                #rotate poligon points
                self.points = rotatepoints(self.rect.center, self.points, alfa)

    # rotate object around the center    
    def rottoanhle(self, alfa, player):
        if self.ispart == True:
            self.points = rotatepoints(player.rect.center, self.points, alfa)
            alfa = 0
            self.rect = findcent(self.alfa, self.points, self.rect, self.ptype)
        else:    
            self.points = rotatepoints(self.rect.center, self.points, alfa)
     
    # create bullet in class Bullets
    def shoot(self, pos):
        bul = Bullets(self.rect.center, pos, self.atack, self.id, self.num)
        if self.num< 10:
            self.num+=1
        else:
            self.num = 0
        return bul

def findcent(alfa, points, rect, ptype):
    if ptype == CANNON: 
        x = ZOOM*math.cos(alfa*math.pi/180)
        y = ZOOM*math.sin(alfa*math.pi/180)
                   
        # where alfa = 90, 180, ... where cos and sin uncorect                 
        rect.x = points[0][0] - ZOOM/2 +  x
        if alfa%90 != 0:
            rect.y = points[0][1] - ZOOM/2 + y
        elif alfa%180 == 1:
            rect.y  = points[0][1] - ZOOM/2
        elif alfa%90 == 1:
            rect.y  = points[0][1]
        return rect
    elif ptype == SHILD:
        x = WIN_WIDTH
        y = WIN_HEIGHT
        for p in points:
            if p[0]<x:
                x = p[0]
            if p[1]<y:
                y = p[1]
        rect.x = x
        rect.y = y
        return rect

# draw recived player
def pldraw(screen, points, color):
    pygame.draw.polygon(screen, color, points)
    
