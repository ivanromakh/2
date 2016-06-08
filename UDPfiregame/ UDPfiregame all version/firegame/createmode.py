import pygame
from pygame import *
import player
from settings import *
from shild import shild_dam, shild_rest

# start create object mode
def createmode(screen, p, pausa, cannon, shild, pos, upispres, parts, zoom, kof, myplayer):
    create = 0
    for e in pygame.event.get():
        if e.type == pygame.MOUSEBUTTONDOWN:     
            if pausa.pressed(pos):
                p = False
            elif cannon.pressed(pos):
                upispres=CANNON
            elif shild.pressed(pos):
                upispres=SHILD    
        
        if e.type == pygame.MOUSEBUTTONUP:
            if upispres > 0:
                squeres = []
                ishere  = False
                print "mouse", pos[0], pos[1]
                for part in parts:
                    squeres.append([part.rect.topleft,part.rect.bottomright])
                    print "closed position ", part.rect.topleft, part.rect.bottomright

                # if under mouse is a part of player end of event 
                for squere in squeres:
                    if pos[0]>= squere[0][0] and pos[0]<= squere[1][0]:
                        print "s1"
                        if pos[1]>= squere[0][1] and pos[1]<= squere[1][1]:
                            ishere = True
                            print "s2"
                            
                # if under mouse isn't any parts             
                if ishere == False:         
                    print "good"
                    for part in parts:
                        if pos[0]>= part.rect.topleft[0]-zoom and pos[0]<= part.rect.bottomright[0]-zoom:
                            if pos[1]>= part.rect.topleft[1] and pos[1]<= part.rect.bottomright[1]:
                                x = part.rect.topleft[0]-zoom
                                y = part.rect.topleft[1]
                                pl = player.Player(part.rect.topleft[0]-ZOOM, part.rect.topleft[1], True, True, upispres)
                                pl.partposx = part.partposx - 1 
                                pl.partposy = part.partposy
                                print "cord", pl.partposx,  pl.partposy
                                upispres=0
                                return (p, upispres, pl)
                                
                        if pos[0]>= part.rect.topleft[0]+zoom and pos[0]<= part.rect.bottomright[0]+zoom:
                            if pos[1]>= part.rect.topleft[1] and pos[1]<= part.rect.bottomright[1]:
                                pl = player.Player(part.rect.topleft[0]+ZOOM, part.rect.topleft[1], True, True, upispres)
                                pl.partposx = part.partposx + 1 
                                pl.partposy = part.partposy
                                print "cord", pl.partposx,  pl.partposy
                                upispres=0
                                return (p, upispres, pl)
                        if pos[0]>= part.rect.topleft[0] and pos[0]<= part.rect.bottomright[0]:
                            if pos[1]>= part.rect.topleft[1]+zoom and pos[1]<= part.rect.bottomright[1]+zoom:
                                pl = player.Player(part.rect.topleft[0], part.rect.topleft[1]+ZOOM, True, True, upispres)
                                pl.partposx = part.partposx  
                                pl.partposy = part.partposy + 1
                                print "cord", pl.partposx,  pl.partposy
                                upispres=0
                                return (p, upispres, pl)
                        if pos[0]>= part.rect.topleft[0] and pos[0]<= part.rect.bottomright[0]:
                            if pos[1]>= part.rect.topleft[1]-zoom and pos[1]<= part.rect.bottomright[1]-zoom:
                                pl = player.Player(part.rect.topleft[0], part.rect.topleft[1]-zoom, True, True, upispres)
                                pl.partposx = part.partposx  
                                pl.partposy = part.partposy - 1
                                print "cord", pl.partposx,  pl.partposy
                                upispres=0
                                return (p, upispres, pl)    
            upispres=0
    return (p, upispres, 0)
    
# pause start 
def startpause(p, pausa, pos):
    if pausa.pressed(pos):
        print "paysa"
        p = True
    return p
