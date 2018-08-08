from pygame.locals import *
from random import randint
from skimage import transform
from skimage.io import imread, imsave
import keras
import pygame
import time

class Apple:

    apple_list = []
    step = 100
 
    def __init__(self,x,y, step):
        self.apple_list = [[x*step, y*step]]
 
    def draw(self, surface, image):
        surface.blit(image,(self.apple_list[0][0], self.apple_list[0][1])) 
 
 
class Player:

    snake = []

    step = 100
    direction = 0
    length = 5
 
    updateCountMax = 2
    updateCount = 0
 
    def __init__(self, length, step):
       self.length = length
       self.step = step
       for i in range(length,0,-1):
            self.snake.append([i*step,0])


    def update(self):
 
        self.updateCount = self.updateCount + 1
        if self.updateCount > self.updateCountMax:
 
            # update previous positions
            
            self.snake = [[self.snake[0][0], self.snake[0][1]]] + self.snake[:]

            if len(self.snake) == self.length+1:
                self.snake.pop()
            
            # update position of head of snake
            if self.direction == 0:
                self.snake[0][0] = self.snake[0][0] + self.step
            if self.direction == 2:
                self.snake[0][0] = self.snake[0][0] - self.step
            if self.direction == 3:
                self.snake[0][1] = self.snake[0][1] - self.step
            if self.direction == 1:
                self.snake[0][1] = self.snake[0][1] + self.step

            #print(self.snake)
            self.updateCount = 0
 
 
    def moveRight(self):
        self.direction = (self.direction+1)%4 
 
    def moveLeft(self):
        self.direction = self.direction - 1
        if self.direction < 0:
            self.direction+=4
 
    def draw(self, surface, image):
        for i in self.snake:
            surface.blit(image,(i[0], i[1])) 
 
class Game:
    def isCollision(self, head, target, self_eat = 0):
        if head in target:
            return True

        width = pygame.display.Info().current_w
        height = pygame.display.Info().current_h

        if head[0] < 0 or head[0]>width:
            return True

        if head[1]<0 or head[1]>height:
            return True
            
        return False
 
class App:
 
    windowWidth = 800
    windowHeight = 800
    player = 0
    apple = 0
    step_size = 100
    network = 0
    score = 0
 
    def __init__(self, network, step_size):
        self._running = True
        self.network = network
        self._display_surf = None
        self._image_surf = None
        self._apple_surf = None
        self.step_size = step_size
        self.game = Game()
        self.player = Player(5, self.step_size) 
        self.apple = Apple(5,5, self.step_size)
        self.score=0
 
    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode((0,0), pygame.HWSURFACE)
        pygame.display.toggle_fullscreen()
 
        pygame.display.set_caption('Pygame pythonspot.com example')
        self._running = True
        adam_block = imread('block_adam_base.jpg')
        adam_block = transform.resize(adam_block, (self.step_size, self.step_size))
        imsave('block_adam.jpg', adam_block)
        julia_block = imread('Block_julia_base.jpg')
        julia_block = transform.resize(julia_block, (self.step_size, self.step_size))
        imsave('block_julia.jpg', julia_block)
        self._image_surf = pygame.image.load('block_adam.jpg').convert()
        self._apple_surf = pygame.image.load("block_julia.jpg").convert()
 
    def on_event(self, event):
        if event.type == QUIT:
            self._running = False
 
    def on_loop(self):
        self.player.update()
 
        # does snake eat apple?

        if self.game.isCollision(self.player.snake[0], self.apple.apple_list):
            screen_width, screen_height = pygame.display.Info().current_w, pygame.display.Info().current_h
            self.apple.apple_list[0][0] = randint(0,(int(screen_width/100)-1)) * self.step_size
            self.apple.apple_list[0][1] = randint(0,(int(screen_height/100)-1)) * self.step_size
            while self.game.isCollision(self.apple.apple_list[0], self.player.snake):
                self.apple.apple_list[0][0] = randint(0,(int(screen_width/100)-1)) * self.step_size
                self.apple.apple_list[0][1] = randint(0,(int(screen_height/100)-1)) * self.step_size
            self.player.length = self.player.length + 1
            self.score+=1
 
 
        # does snake collide with itself?
        if self.game.isCollision(self.player.snake[0], self.player.snake[1:], self_eat=1):
            print("You lose! Collision")
            self._running=False
 
        pass
 
    def on_render(self):
        screen_width, screen_height = pygame.display.Info().current_w, pygame.display.Info().current_h
        self._display_surf.fill((0,0,0))
        self.player.draw(self._display_surf, self._image_surf)
        self.apple.draw(self._display_surf, self._apple_surf)

        font=pygame.font.Font(None,60)
        scoretext=font.render("Score: " + str(self.score), 1,(255,255,255))
        self._display_surf.blit(scoretext, (10, screen_height-70))

        pygame.display.flip()
 
    def on_cleanup(self):
        pygame.quit()

    def get_input(self):
        out = [0, 0, 0, 0, 0, 0]
        sh = self.player.snake[0]
        dire = self.player.direction
        appl=self.apple.apple_list[0]
        mod = [[sh[0]+100, sh[1]], [sh[0], sh[1]+100], [sh[0]-100, sh[1]], [sh[0], sh[1]-100]]
        
        if self.game.isCollision(mod[(dire-1)%4], self.player.snake[:-1]):
            out[0]=1
        else:
            out[0]=0
        
        if self.game.isCollision(mod[dire], self.player.snake[:-1]):
            out[1]=1
        else:
            out[1]=0
        
        if self.game.isCollision(mod[(dire+1)%4], self.player.snake[:-1]):
            out[2]=1
        else:
            out[2]=0

        if dire == 3:
            if sh[0]==appl[0] and appl[1]<sh[1]:
                out[4]=1
            else:
                out[4]=0
            
            if sh[1]==appl[1]:
                if sh[0]>appl[0]:
                    out[3]=1
                    out[5]=0
                else:
                    out[3]=0
                    out[5]=1

        if dire == 1:
            if sh[0]==appl[0] and appl[1]>sh[1]:
                out[4]=1
            else:
                out[4]=0
            
            if sh[1]==appl[1]:
                if sh[0]>appl[0]:
                    out[3]=0
                    out[5]=1
                else:
                    out[3]=1
                    out[5]=0

        if dire == 0:
            if sh[1]==appl[1] and appl[0]>sh[0]:
                out[4]=1
            else:
                out[4]=0
            
            if sh[0]==appl[0]:
                if sh[1]>appl[1]:
                    out[3]=1
                    out[5]=0
                else:
                    out[3]=0
                    out[5]=1

        if dire == 2:
            if sh[1]==appl[1] and appl[0]<sh[0]:
                out[4]=1
            else:
                out[4]=0
            
            if sh[0]==appl[0]:
                if sh[1]>appl[1]:
                    out[3]=0
                    out[5]=1
                else:
                    out[3]=1
                    out[5]=0
        

        return out    

    def on_execute(self):
        if self.on_init() == False:
            self._running = False
 
        while( self._running ):
            pygame.event.pump()
            keys = pygame.key.get_pressed() 

            input_data = self.get_input()
            result = self.network.predict(input_data)
            
            if result==1:
                self.player.moveRight()
 
            if result == 2:
                self.player.moveLeft()
 
            if (keys[K_ESCAPE]):
                self._running = False
 
            self.on_loop()
            self.on_render()
 
            time.sleep (50.0 / 1000.0)

        self.on_cleanup()
        return self.score

def playing_game(network, step):
    theApp = App(network, step)
    result = theApp.on_execute()
    return result
 
'''
if __name__ == "__main__" :
    theApp = App(100)
    theApp.on_execute()
'''
