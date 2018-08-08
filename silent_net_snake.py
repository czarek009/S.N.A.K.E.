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
 
    def on_init(self):
        pygame.init()

        Player.length = Player.length - 5 # Bo tak.
 
        self._running = True
 
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
            Player.length = Player.length + 1
 
 
        # does snake collide with itself?
        if self.game.isCollision(self.player.snake[0], self.player.snake[1:], self_eat=1):
            self._running=False
 
        pass

 
    def on_cleanup(self):
        pygame.quit()
 
    def on_execute(self):
        if self.on_init() == False:
            self._running = False
 
        while( self._running ):

            input_data = get_input()
            result = self.network.predict(input_data)
            
            if result==1:
                self.player.moveRight()
 
            if result == 2:
                self.player.moveLeft()
 
            self.on_loop()
 
            time.sleep (50.0 / 1000.0)

        self.on_cleanup()
        return self.score

def playing_game(network, step):
    theApp = App(network, step)
    result = theApp.on_execute()
    return result