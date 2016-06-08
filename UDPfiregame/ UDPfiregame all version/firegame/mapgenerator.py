import pygame
import os
import sys
from pygame import *
from settings import*

def generationmap(PLATFORM_HEIGHT):
    width = WIN_WIDTH/PLATFORM_HEIGHT
    height = WIN_HEIGHT/PLATFORM_HEIGHT
    noise = [[r for r in range(width)] for i in range(height)]
    print "s", width, height  
    return noise, width, height 

    
            
