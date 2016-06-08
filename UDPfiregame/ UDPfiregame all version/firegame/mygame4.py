import random 
import pygame
from   pygame.locals import *
import psycopg2
import sys
import pickle
from time import sleep
import socket

import player
from player import* 
from settings import *
from pygame import *
from mapgenerator import generationmap
from menu import Menu, mennu
from minimap import Minimap
from MyButtons import createbuttons, update_display
from createmode import startpause, createmode
from shild import shild_dam, shild_rest


# !! NOT VERY GOOD !!
#find squere of enemy on the map 
def findsquere(encord):
    xmin = encord[0][0]
    xmax = encord[0][0]
    ymin = encord[0][1]
    ymax = encord[0][1]
    for i in range(3):
        if xmin > encord[i][0]:
            xmin = encord[i][0]
        if xmax < encord[i][0]:
            xmax = encord[i][0]
        if ymin > encord[i][1]:
            ymin = encord[i][1]
        if ymax < encord[i][1]:
            ymax = encord[i][1]
    return (xmin, xmax, ymin, ymax)


def drawscbull(screen, (x, y), scale):
    pygame.draw.circle(screen, (250,0,250), (x, y), int(BUL_SIZE*scale) , int(BUL_SIZE*scale))

def move(p, x, y):
    p[0][0] = p[0][0] - x
    p[0][1] = p[0][1] - y
    p[1][0] = p[1][0] - x
    p[1][1] = p[1][1] - y 
    p[2][0] = p[2][0] - x
    p[2][1] = p[2][1] - y
    return p


    
def drawpoligon(screen, pos):
    pygame.draw.polygon(screen, PL_COLOR, ((pos[0] - ZOOM/2, pos[1]),
                                           (pos[0] + ZOOM/2, pos[1] - ZOOM/2),
                                           (pos[0] + ZOOM/2, pos[1] + ZOOM/2)))

def drawrect(screen, pos):
    pygame.draw.polygon(screen, PL_COLOR, ((pos[0] - ZOOM/2, pos[1] - ZOOM/2),
                                           (pos[0] - ZOOM/2, pos[1] + ZOOM/2),
                                           (pos[0] + ZOOM/2, pos[1] + ZOOM/2),
                                           (pos[0] + ZOOM/2, pos[1] - ZOOM/2)))

# draw information and fps  
def drawtext(screen, timer):
    mytext = pygame.font.SysFont("monospace", 15)
    timer.tick(40)
    text = mytext.render("FPS "+str(timer.get_fps()), 1, (10, 10, 10))
    screen.blit(text, (5, 160))

#zooming recived players objects
def enzooming(obj, center, x, y, scale):
    dis = mypoints(obj, center, x, y, scale)
    return dis

def bzooming(obj, center, x, y, scale):
    dis = mypoint(obj, center, x, y, scale)
    return dis

def mypoints(points, center, x, y, scale):
    newp = []
    for p in points: 
        newp.append((int(center[0]+((p[0]-center[0])*scale)), int(center[1]+((p[1]-center[1])*scale))))
    return newp

def mypoint(p, center, x, y, scale):
    return (int(center[0]+((p[0]-center[0]-x)*scale)), int(center[1]+((p[1]-center[1]-y)*scale)))
    
# main function
def main():
    pygame.init()
    # menu check server or client
    mennu()
    #zoom    
    zoom = ZOOM
    kof = 0
    scale = 1
    #draw displey
    screen = pygame.display.set_mode(DISPLAY) 
    # minimap
    minimap = Surface((MINIMAPSIZE,MINIMAPSIZE))
    # generation first position    
    (maps, x, y) = generationmap(zoom)
    # get player start position
    midx = WIN_WIDTH/2
    midy = WIN_HEIGHT/2
    # minimap create
    minmap = Minimap()
    #create this user 
    myplayer = player.Player(midx, midy, True, False, CANNON)
    play_parts = pygame.sprite.Group()
    play_parts.add(myplayer)
    #this user bullets
    player_bul = pygame.sprite.Group()
    zoom1 = ZOOM + 0.0
    # clock for fps
    timer = pygame.time.Clock()
    
    # zoom press
    iszoomincres = False
    iszoomdecres = False
        
    # socket create
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.connect((HOST, PORT))

    #Buttons
    upispres = 0
    p = False
    pausa = createbuttons()
    cannon = createbuttons()
    shild = createbuttons()
    
    # lists for reciven and sending 
    recivepl = []
    reciveen = []
    reckilen = []
    mustdelete = []
    
    damagesend = []
    sendparts = []
    mybulsend = []
    
    # send list of this user bullets
    data = ""
    while True:
        #draw background on the screen 
        screen.fill(BACKGROUND_COLOR)
        
        # if zoom pressed zoom increes
        if iszoomincres == True:
            if scale<MAXSCALE:
                zoom1 += 2
                scale = zoom1/ZOOM
        # if zoom pressed zoom decrease        
        elif iszoomdecres == True:
            if scale>MINSCALE:
                zoom1 -= 2
                scale = zoom1/ZOOM

        #remove and zooming player
        for enemy in reciveen:
            for kilen in reckilen:
                if enemy[3] == kilen:
                    reciveen.remove(enemy)
            x = enzooming(enemy[:3], myplayer.rect.center,
                          myplayer.myposx, myplayer.myposy, scale)
            pldraw(screen, x, EN_COLOR)            
                
            #SHILD
        # check shilds
        #shild_dam((0,0), play_parts)
        # shild restore
        #shild_rest(play_parts)

             
        # SHOTTING and all for this player bullets
        # and killed enemies
        mybulsend = []
        damagesend = []
        #update and draw bullets   
        for bul in player_bul:
            bul.updat()
            x = bzooming((bul.rect.x, bul.rect.y), myplayer.rect.center, 0, 0, scale)
            drawscbull(screen, x, scale)
            # check if bullet find a target
            for encord in reciveen:
                (xmin, xmax, ymin, ymax) = findsquere(encord)
                #if bullet in the enemy squere kill bullet         
                if bul.rect.x >=  xmin+3 and bul.rect.x <= xmax-3:
                    if bul.rect.y >=  ymin+3 and bul.rect.y <= ymax-3:
                        damagesend.append(encord[3])
                        reciveen.remove(encord)
                        bul.kill()
                        
            #add bullet in send list    
            mybulsend.append((bul.rect.x+int(myplayer.myposx), bul.rect.y+int(myplayer.myposy), bul.id, bul.num))


            #CREATE PACKAGE FOR SEND
        #send thisplayer package
        data = "PL"
        myplayer.shiftmove()
        data += pickle.dumps(myplayer.sendp)
        #serialize thisplayer bullets    
        data += "BUL"
        data += pickle.dumps(mybulsend)
        #serialize damage of thisplayer bullets   
        data += "DAM"
        data += pickle.dumps(damagesend)
        data += "PAR"
        data += pickle.dumps(sendparts)
        
        #send and recive package
        sock.send(data)
        rec = sock.recv(BUFF)

        #DECODE PACKAGE
        if rec[:2] == "PL":
            rec = rec[2:]
            cords = rec.split("BUL")

            #players
            players = pickle.loads(cords[0])
            for pl in players:
                if pl[3]!= myplayer.id:
                    for myp in recivepl:
                        if pl[3]== myp[3]:
                            recivepl.remove(myp)
                    recivepl.append(pl)

            cor = cords[1].split("ENE")

            #take bullet other player and zoomed
            bullets = pickle.loads(cor[0])
            if bullets != []:
                for b in bullets:
                    temp = False
                    for pl in play_parts:
                        if pl.id == b[2]:
                            temp = True
                    if temp == False:        
                        x = bzooming(b[:2], myplayer.rect.center, myplayer.myposx, myplayer.myposy, scale)
                        drawscbull(screen, x, scale)

            co = cor[1].split("KIL")

            #take enemy cords
            enemies = pickle.loads(co[0])
            for enemy in enemies:
                for myenemy in reciveen:
                    if enemy[3] == myenemy[3]:
                        reciveen.remove(myenemy)
                reciveen.append(enemy)

            cor = co[1].split("ENB")
            
            # take id killen enemies
            reckilen = pickle.loads(cor[0])

            #take enemy bullets and zoomed
            enbul = pickle.loads(cor[1])
            for b in enbul:
                x = bzooming(b, myplayer.rect.center, myplayer.myposx, myplayer.myposy, scale)
                drawscbull(screen, x, scale)
            
        # move recived players
        for p in recivepl:
            if p[4] == False:
                move(p,myplayer.myposx, myplayer.myposy)
                p[4] = True
            x = enzooming(p[:3], myplayer.rect.center,
                          myplayer.myposx, myplayer.myposy, scale)
            pldraw(screen, x, PL_COLOR)  

        # draw recived enemies
        for myenemy in reciveen:
            if myenemy[4] == False:
                myenemy = move(myenemy,myplayer.myposx, myplayer.myposy)
                myenemy[4] = True

                
        #draw and update thisplayer object 
        pos = mouse.get_pos()
        for pl in play_parts:
            pl.update(0, 1, myplayer)
            if pl.id == myplayer.id:
                pl.draw(screen, pos, scale)
            else:
                x = enzooming(pl.points, myplayer.rect.center,
                          myplayer.myposx, myplayer.myposy, scale)
                pldraw(screen, x, PL_COLOR)

        # ALL EVENTS for gamemode
        for e in pygame.event.get():
            # check multipress 
            keystate = pygame.key.get_pressed()
        
            # exit
            if e.type == QUIT:
                sock.close()
                pygame.quit()
                sys.exit()
 
            # start moving and rotating
            elif e.type == KEYDOWN:
                if keystate[K_ESCAPE]:
                    pygame.quit()
                    sys.exit()
                if keystate[K_UP]:
                    for part in play_parts:
                        part.ismoveup = True
                if keystate[K_DOWN]:
                    for part in play_parts:
                        part.ismovedown = True
                if keystate[K_LEFT]:
                    for part in play_parts:
                        part.isrotateleft = True
                if keystate[K_RIGHT]:
                    for part in play_parts:
                        part.isrotateright = True
                if keystate[K_1]:
                    iszoomincres = True
                if keystate[K_2]:
                    iszoomdecres = True

            # stop moving and rotating        
            elif e.type == KEYUP:
                if e.key == K_UP:
                    for part in play_parts:
                        part.ismoveup = False
                if e.key == K_DOWN:
                    for part in play_parts:
                        part.ismovedown = False
                if e.key == K_LEFT:
                    for part in play_parts:
                        part.isrotateleft = False
                if e.key == K_RIGHT:
                    for part in play_parts:
                        part.isrotateright = False
                if e.key == K_1:
                    iszoomincres = False
                if e.key == K_2:
                    iszoomdecres = False

            #player shoot        
            elif e.type == pygame.MOUSEBUTTONDOWN:

                # if button press (CREATEMODE)        
                if e.type == pygame.MOUSEBUTTONDOWN:
                    # mouse position
                    pos = pygame.mouse.get_pos()
                    p = startpause(p, pausa, pos)
                    
                    # if pausa reset all player objects angle
                    if p == True:
                        print myplayer.points
                        alfa = myplayer.alfa
                        if alfa%360!=0:
                            alfa = alfa%360
                            for part in play_parts:
                                part.alfa = 0
                                part.rottoanhle(-alfa, myplayer)
                                part.update(0, 1 , myplayer)
                               
                    #pausa createmode begin
                    while p == True:
                        screen.fill((100,100,100))
                        #print myplayer.rect
                        update_display(screen, cannon, 100, 2, WIN_WIDTH/2)
                        update_display(screen, shild, 140, 2, WIN_WIDTH/2)
                        update_display(screen, pausa, 10, 2, 0)
                        
                        pos = pygame.mouse.get_pos()
                        (p,upispres, mypl) = createmode(screen, p, pausa, cannon, shild, pos, upispres, play_parts, ZOOM, kof, myplayer)
                        
                        if mypl != 0:
                            play_parts.add(mypl)
                        if upispres == CANNON:
                            drawpoligon(screen, pos)
                        elif upispres == SHILD:
                            drawrect(screen, pos)
                        for pl in play_parts:
                            pl.draw(screen, pos, 1)
                        
                        pygame.display.flip()
                
                # player shoot
                for pl in play_parts:
                    if pl.ptype == CANNON:
                        player_bul.add(pl.shoot(pos))
        #pausa button                
        update_display(screen, pausa, 10, 1,0)        

        drawtext(screen, timer)
        minmap.draw(screen, reciveen, myplayer, recivepl)
        pygame.display.flip()

# main fuction                
if __name__ == "__main__":
    main()
    
