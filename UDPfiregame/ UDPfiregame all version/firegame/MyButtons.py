# -*- coding: cp1252 -*-
#/usr/bin/env python
#Simon H. Larsen
#Buttons.py - example
#Project startet: d. 28. august 2012
#Import pygame modules and Buttons.py(it must be in same dir)


import pygame, Buttons
from pygame.locals import *
from settings import WIN_WIDTH



#Initialize pygame
pygame.init()



#Update the display and show the button
def update_display(screen, button, y, cost, width):
        #Parameters:          surface,   color,         x,      y,  length, height, width,    text,      text_color
        if width == 0:
            button.create_button(screen, (200,200,200), WIN_WIDTH-40, y, 32,    32,    0,        str(cost), (255,255,255))
        else:
            button.create_button(screen, (200,200,200), width, y, 32,    32,    0,        str(cost), (255,255,255))    
                
def createbuttons(): 
    button = Buttons.Button()
    return button

