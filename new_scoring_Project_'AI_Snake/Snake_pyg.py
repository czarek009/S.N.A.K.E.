from pygame.locals import *
from random import randint
from skimage import transform
from skimage.io import imread, imsave
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

    def false_update(self,false_dire):
        # update previous positions
        
        false_snake = [[self.snake[0][0], self.snake[0][1]]] + self.snake[:]

        if len(false_snake) == self.length+1:
            false_snake.pop()
        
        # update position of head of snake
        if false_dire == 0:
            false_snake[0][0] = false_snake[0][0] + self.step
        if false_dire == 2:
            false_snake[0][0] = false_snake[0][0] - self.step
        if false_dire == 3:
            false_snake[0][1] = false_snake[0][1] - self.step
        if false_dire == 1:
            false_snake[0][1] = false_snake[0][1] + self.step

        print(false_snake[0])
        print(false_snake[1:-1])

        return Game.isCollision(self,false_snake[0],false_snake[1:-1])

 
 
    def moveRight(self):
        self.direction = 0
 
    def moveLeft(self):
        self.direction = 2
 
    def moveUp(self):
        self.direction = 3
 
    def moveDown(self):
        self.direction = 1
 
    def draw(self, surface, image):
        for i in self.snake:
            surface.blit(image,(i[0], i[1])) 
 
class Game:
    def isCollision(self, head, target):
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
    
    score = 0
    windowWidth = 800
    windowHeight = 800
    player = 0
    apple = 0
    step_size = 100
    apple_distance = 0
 
    def __init__(self, step_size):
        self._running = True
        self.input = 0
        self._display_surf = None
        self._image_surf = None
        self._apple_surf = None
        self.step_size = step_size
        self.game = Game()
        self.player = Player(10, self.step_size) 
        self.apple = Apple(5,5, self.step_size)
        self.apple_distance = (abs(self.player.snake[0][0]//100 - self.apple.apple_list[0][0]//100) + abs(self.player.snake[0][1]//100 - self.apple.apple_list[0][1]//100))
 
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
            self.score = self.score + 20
 
 
        # does snake collide with itself?
        if self.game.isCollision(self.player.snake[0], self.player.snake[1:]):
            print("You lose! Collision")
            #print(self.player.snake[0])
            #print(self.get_input())
            exit(0)
 
        pass
 
    def on_render(self):
        screen_width, screen_height = pygame.display.Info().current_w, pygame.display.Info().current_h
        self._display_surf.fill((0,0,0))
        self.player.draw(self._display_surf, self._image_surf)
        self.apple.draw(self._display_surf, self._apple_surf)

        font=pygame.font.Font(None,60)
        scoretext=font.render("Score: " + str(self.score)+'    '+str(self.input[:3]), 1,(255,255,255))
        self._display_surf.blit(scoretext, (10, screen_height-70))

        #input_text=font.render(str(self.get_input()), 1, (255,255,255))
        #self._display_surf.blit(input_text, (400, screen_height-70))

        pygame.display.flip()
 
    def on_cleanup(self):
        pygame.quit()
 
    def updateScore(self):
        current_distance = (abs(self.player.snake[0][0]//100 - self.apple.apple_list[0][0]//100) + abs(self.player.snake[0][1]//100 - self.apple.apple_list[0][1]//100))

        if current_distance<self.apple_distance:
            self.score+=2
        elif current_distance>self.apple_distance:
            self.score-=3

        self.apple_distance = current_distance

    def on_execute(self):
        if self.on_init() == False:
            self._running = False

        #dire = 0

        while( self._running ):
            pygame.event.pump()
            keys = pygame.key.get_pressed() 

            self.input = self.get_input()
            print (self.input[:3])
            print('____________')
            '''
            done = 0

            if (dire == 0) and done == 0:
                self.player.moveRight()
                dire += 1
                done = 1
 

            if (dire == 1) and done == 0:
                self.player.moveDown()
                dire += 1
                done = 1


            if (dire == 2) and done == 0:
                self.player.moveLeft()
                dire += 1
                done = 1


            if (dire == 3) and done == 0:
                self.player.moveUp()
                dire += 1
                done = 1
            
            '''
            if (keys[K_RIGHT]) and self.player.direction!=2:
                self.player.moveRight()
 
            if (keys[K_LEFT]) and self.player.direction!=0:
                self.player.moveLeft()
 
            if (keys[K_UP]) and self.player.direction!=1:
                self.player.moveUp()
 
            if (keys[K_DOWN]) and self.player.direction!=3:
                self.player.moveDown()
            
            
 
            if (keys[K_ESCAPE]):
                self._running = False
 
            self.on_loop()
            self.on_render()
            self.updateScore()
            time.sleep (150.0 / 1000.0)
        self.on_cleanup()

    def get_input(self):
        out = [0, 0, 0, 0, 0, 0]
        sh = self.player.snake[0]
        dire = self.player.direction
        appl=self.apple.apple_list[0]
        #mod = [[sh[0]+100, sh[1]], [sh[0], sh[1]+100], [sh[0]-100, sh[1]], [sh[0], sh[1]-100]]
        
        if self.player.false_update((dire-1)%4):
            out[0]=1
        else:
            out[0]=0
        
        if self.player.false_update(dire):
            out[1]=1
        else:
            out[1]=0
        
        if self.player.false_update((dire+1)%4):
            out[2]=1
        else:
            out[2]=0

        if dire == 3:
            if appl[1]<sh[1]:
                out[4]=1
            else:
                out[4]=0

            if sh[0]>appl[0]:
                out[3]=1
                out[5]=0
            elif sh[0]<appl[0]:
                out[3]=0
                out[5]=1

        if dire == 1:
            if appl[1]>sh[1]:
                out[4]=1
            else:
                out[4]=0
            
            if sh[0]>appl[0]:
                out[3]=0
                out[5]=1
            elif sh[0]<appl[0]:
                out[3]=1
                out[5]=0

        if dire == 0:
            if appl[0]>sh[0]:
                out[4]=1
            else:
                out[4]=0
            

            if sh[1]>appl[1]:
                out[3]=1
                out[5]=0
            elif sh[1]<appl[1]:
                out[3]=0
                out[5]=1

        if dire == 2:
            if appl[0]<sh[0]:
                out[4]=1
            else:
                out[4]=0
            

            if sh[1]>appl[1]:
                out[3]=0
                out[5]=1
            elif sh[1]<appl[1]:
                out[3]=1
                out[5]=0
        

        return out   
        
 
if __name__ == "__main__" :
    theApp = App(100)
    theApp.on_execute()
