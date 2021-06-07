import sys
import serial, time
import pygame
import threading, queue
import time

global enemyLife
enemyLife = 5
global width
width = 5
global height
height = 5

black = 0, 0, 0
dt = 1
gamma = 0.05
q = queue.Queue()
q2 = queue.Queue()

class Read_Microbit(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self._running = True
      
    def terminate(self):
        self._running = False
        
    def run(self):
        #serial config
        port = "COM3"
        s = serial.Serial(port)
        s.baudrate = 115200
        while self._running:
            data = s.readline().decode()
            listaCom=data.split(",")
            fire = listaCom[0]
            acc = [float(x) for x in listaCom[1:3]]
            q.put(acc)
            q2.put(fire)
            print(f"Sparo: {fire}\nPosiz:{acc}")
            time.sleep(0.01)

class Game:
    screen = None
    enemyBullets = []
    yourBullets = []
    lost = False

    def __init__(self, width, height):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()
        done = False
    def MoveShuttle():
        screen = pygame.display.set_mode((width, height))
        clock = pygame.time.Clock()
        shuttle = pygame.image.load("C:\\Users\\obema\\Desktop\\scuola\\Sistemi\\MicroBit\\spaceShuttle.png")
        shutlleRect = shuttle.get_rect()
        shutlleRect.centerx = width//2
        shutlleRect.centery = height//2

        running = True
        rm = Read_Microbit()
        rm.start()
        pygame.init()
        speed = [0, 0]
        while running:
            acc = q.get()
            shoot = q2.get()
            #print(f"Sparo: {shoot}\nPosiz:{acc}")
            speed[0] = (1.-gamma)*speed[0] + (dt*acc[0]/1024)*2.
            speed[1] = (1.-gamma)*speed[1] + (dt*acc[1]/1024)*2.
            q.task_done()
            shrect = shrect.move(speed)
            if shrect.left < 0 or shrect.right > width:
                speed[0] = -speed[0]
            if shrect.top < 0 or shrect.bottom > height:
                speed[1] = -speed[1]
            screen.fill(black)
            screen.blit(shuttle, shrect)
            pygame.display.flip()
            clock.tick(10)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
            
            rm.terminate()
            rm.join()

        shuttle = Shuttle(self, width / 2, height - 20)
        enShootGen = EnemyShootGen(self)
        shoot = None

        while not done:
            if enemyLife == 0:
                self.displayText("VICTORY")
            MoveShuttle()
            
            

''' Da gestire con scoket-thread  
class EnemyShootGen:
    def __init__(self):
        
'''

def main():
    game = Game(width, height)
if __name__=="__main__":
    main()