import pygame
import os

    #DISPLAY
#resolution
WIN_WIDTH = 800 
WIN_HEIGHT = 500

DISPLAY = (WIN_WIDTH, WIN_HEIGHT)

#size parts
ZOOM = 40

# SCALE
MAXSCALE = 3
MINSCALE = 0.2
#zoom parts distance
OBJKOF = 1.2

        #MINIMAPMAP
#Minimap size
MINIMAPSIZE = WIN_HEIGHT/5

#map size
MAPSIZE = ZOOM*MINIMAPSIZE

# size object on minimap
MIN_SIZE = 3 

    #Enemies and player
#health of enemy
ENHEALTH = 10
# part health
PHEALTH = 100
# alfa player rotation
ALFA = 5
# player speed
SPEED = 7
# enemy create rate
ENEMYRATE, enrate, trail = pygame.USEREVENT+2, 7000, []
#enemy fire rate
EN_FIRE, firetime, trail = pygame.USEREVENT+1, 500, []
# enemy speed
EN_SPEED = 1
# enemy range
RANGE = 400
# cannon ssize
CANNONSIZE = 30

    #PART TYPE
CANNON = 1
SHILD = 2
# cannon atack
CAN_ATACK = 4
#shild color
SH_COLOR = (0,0,200)
# shild think or
SH_THINK = 2
SHHEALTH = 100
SHRADIUS = 100
    #BULLET
# bullet size
BUL_SIZE = 4
# bullet speed
VELOCITY = 20
#bullet time live
BULTIME = 2000

    #Colors of objects
# back ground color  
BACKGROUND_COLOR = (100,100,100)
# player color
PL_COLOR = (0,180,0)
# enemy color
EN_COLOR = (250,0,0)
# cannon color
CAN_COLOR = (0,0,0)
# minimap enemy color 
MIN_EN_COLOR = (250,0,0)

my_unix_command = ['bc']
HOST = 'localhost'
PORT = 50012
BUFF = 1000000
