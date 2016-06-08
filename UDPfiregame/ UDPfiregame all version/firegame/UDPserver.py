import threading
import socket
import logging
import pickle
import pygame
import random
import math


from settings import*
import player

clients_lock = threading.Lock()

class Server():
    def __init__(self):
        logging.info('Initializing Broker')
        pygame.init()
        self.recpl = []
        self.recbull = []
        self.senden = []
        self.sendkilen = []
        self.sendenbul = []
        self.plid = []
        self.en = pygame.sprite.Group()
        self.en_bul = pygame.sprite.Group()
        
        pygame.time.set_timer(ENEMYRATE, 3000)
        pygame.time.set_timer(EN_FIRE, 500)
    
    def enmove(self):
        # enemy updates
        for e in self.en:
            x = 6
            x = int(x*random.random())
            if x == 0:
                e.update(-1,1, 0)
                self.senden.remove(e.sendp)
                e.shiftmove()
                self.senden.append(e.sendp)
            if x == 1:
                e.rotate(1, 0)
                self.senden.remove(e.sendp)
                e.shiftmove()
                self.senden.append(e.sendp)
            if x >= 2 and x <=5:
                e.update(1,1, 0)
                self.senden.remove(e.sendp)
                e.shiftmove()
                self.senden.append(e.sendp)
            if x == 6:
                e.rotate(1, 0)
                self.senden.remove(e.sendp)
                e.shiftmove()
                self.senden.append(e.sendp)

    def EnemyandShot(self):
            for e in pygame.event.get():
                if e.type ==  ENEMYRATE:
                    myenemy = player.Player(
                        int(WIN_WIDTH/ZOOM*random.random()),
                        int(WIN_HEIGHT/ZOOM*random.random()),
                        False, False, CANNON)
                    
                    self.senden.append(myenemy.sendp)
                    self.en.add(myenemy)

                # enemy shoot
                if e.type == EN_FIRE:
                    for myen in self.en:
                        for pl in self.recpl:
                            x = myen.points[0][0]-pl[0][0]
                            y = myen.points[0][1]-pl[0][1]
                            if math.sqrt(pow(x,2)+pow(y,2)) < myen.radius:
                                bullet = myen.shoot(pl[0])
                                if bullet != [] and bullet != 0:
                                    self.en_bul.add(bullet)
                                    break
                                    


    def bulupdate(self):
        self.sendenbul = []
        for bul in self.en_bul:
            for pl in self.recpl:
                #find squere of player on the map 
                xmin = pl[0][0]
                xmax = pl[0][0]
                ymin = pl[0][1]
                ymax = pl[0][1]
                for i in range(3):
                    if xmin > pl[i][0]:
                        xmin = pl[i][0]
                    if xmax < pl[i][0]:
                        xmax = pl[i][0]

                    if ymin > pl[i][1]:
                        ymin = pl[i][1]
                    if ymax < pl[i][1]:
                        ymax = pl[i][1]

                #if bullet in the enemy squere kill bullet         
                if bul.rect.x >=  xmin+3 and bul.rect.x <= xmax-3:
                    if bul.rect.y >=  ymin+3 and bul.rect.y <= ymax-3:
                        bul.kill()
            bul.updat()
            self.sendenbul.append((bul.rect.x, bul.rect.y, bul.id, bul.num))


    # recive data and run send thread
    def listen_clients(self, sock):
        while True:

            #recive daata    
            msg, client = sock.recvfrom(1024)

            # decode data
            self.decode(msg)

            #start thread send to client
            data = "PL"
            data += pickle.dumps(self.recpl)
            data += "BUL"
            data += pickle.dumps(self.recbull)
            data += "ENE"
            data += pickle.dumps(self.senden)   
            data += "KIL"
            data += pickle.dumps(self.sendkilen)
            data += "ENB"
            data += pickle.dumps(self.sendenbul)

            #send data
            sock.sendto(data, client)
            
    # take data from message(package)
    def decode(self, msg):

        # if this is player cords
        if msg[0:2] == "PL":
            msg = msg[2:]
            cords = msg.split("BUL")

            #players
            player = pickle.loads(cords[0])
            ishere = False
            print "-------------------------"
            print self.plid
            
            for p in self.plid:
                if player[3] == p:
                    ishere = True
            if ishere == False:
                self.plid.append(player[3])

            for pl in self.recpl:
                if player[3] == pl[3]:
                    self.recpl.remove(pl)
            self.recpl.append(player)
                                       
            if player[3] == self.plid[0]:
                self.EnemyandShot()
                self.enmove()
                self.bulupdate()
            tcords = cords[1].split("DAM")
            
            #bullets
            bullets = pickle.loads(tcords[0])
            for cor in bullets:
                for b in self.recbull:
                    if cor[3] == b[3]:
                        if cor[2] == b[2]:
                            self.recbull.remove(b)
                self.recbull.append(cor)

            #damage
            damage = pickle.loads(tcords[1])
            for e in self.en:
                for dam in damage:
                    if e.id == dam:
                        if len(self.sendkilen) < 3:
                            self.sendkilen.append(e.id)
                        else:
                            self.sendkilen.remove(self.sendkilen[0])
                            self.sendkilen.append(e.id)
                        self.senden.remove(e.sendp)
                        e.kill()
                        
                             
if __name__ == '__main__':
    
    print "start", HOST, PORT
    Ser = Server()

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((HOST, PORT))
    
    t = threading.Thread(target=Ser.listen_clients(sock).start())
    print "ss"
    








    
