import pygame
from settings import *


class Minimap():
    def __init__(self):
        self.zoom = ZOOM
        self.image = pygame.Surface((MINIMAPSIZE, MINIMAPSIZE))
        self.image.fill((0,0,0))

    def draw(self, screen, enemies, player, players):
        x = player.rect.center[0]/ZOOM
        y = player.rect.center[1]/ZOOM
        
        self.image.fill((0,0,0))
        pygame.draw.circle(self.image, (0,0,250), (MINIMAPSIZE/2, MINIMAPSIZE/2), MIN_SIZE, MIN_SIZE)
            
        for en in enemies:
            #first point
            x1 = int(en[1][0])/ZOOM
            y1 = int(en[1][1])/ZOOM
            
            if x1<= x+MINIMAPSIZE/2 and x1>= x-MINIMAPSIZE/2:
                if y1<= y+MINIMAPSIZE/2 and y1>= y-MINIMAPSIZE/2:
                    pygame.draw.circle(self.image, MIN_EN_COLOR, (MINIMAPSIZE/2 + (x1-x),MINIMAPSIZE/2 + (y1-y)), MIN_SIZE, MIN_SIZE)

        for pl in players:
            #first point
            x1 = int(pl[1][0])/ZOOM
            y1 = int(pl[1][1])/ZOOM
            
            if x1<= x+MINIMAPSIZE/2 and x1>= x-MINIMAPSIZE/2:
                if y1<= y+MINIMAPSIZE/2 and y1>= y-MINIMAPSIZE/2:
                    pygame.draw.circle(self.image, (0,250,0) , (MINIMAPSIZE/2 + (x1-x),MINIMAPSIZE/2 + (y1-y)), MIN_SIZE, MIN_SIZE)
        screen.blit(self.image, (10,10))
