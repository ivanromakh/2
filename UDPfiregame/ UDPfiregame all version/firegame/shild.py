import pygame
from settings import *
from pygame import *


def shild_dam(bullets, parts):
    for bul in bullets:
        for part in parts:
            if part.ptype == SHILD:
                if pygame.sprite.collide_circle(bul, part):
                    if part.radius> 15:
                       part.radius -= 10
                       bul.kill()

def shild_rest(parts):
    for part in parts:
        if part.ptype == SHILD:
            if part.radius < SHRADIUS:
                part.radius+=1
