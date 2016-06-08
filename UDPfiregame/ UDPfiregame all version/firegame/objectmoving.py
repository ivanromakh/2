import math
import pygame
from pygame import *

from settings import *

# rotate all points in polligon around the center    
def rotatepoints(c, points, r):
    s = math.sin(r*math.pi/180)
    cs = math.cos(r*math.pi/180)
    respoints = []
    for p in points:
        # distance 
        tempx = p[0] - c[0]
        tempy = p[1] - c[1]
        
        # zmichennia
        x = tempx*cs - tempy*s
        y = tempx*s + tempy*cs
        
        #update distance 
        respoints.append([c[0] + x, c[1] + y])
    return respoints

