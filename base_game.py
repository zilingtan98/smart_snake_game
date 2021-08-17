import pygame
import random
from enum import Enum
from collections import namedtuple

pygame.init()
font = pygame.font.SysFont('arial', 25)

class Moving(Enum):
    """
    direction of the snake moving

    Args:
        Enum ([type]): [description]
    """
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4

Point = namedtuple('Point', 'x , y')
BLOCK_SIZE = 20
SPEED = 40
WHITE = (255, 255, 255)
RED = (200,0,0)
GREEN = (0,128,0)
LIGHT_GREEN = (173,255,47)
BLACK = (0,0,0)

class SnakeGame():
    """
    Class for snake game
    """
    def __init__(self, w= 640, h= 480):
        # set window size for game and display
        self.w = w
        self.h = h
        self.display = pygame.display.set_mode((self.w, self.h))
        # title
        pygame.display.set_caption('Yeet Snake')
        # get time
        self.clock = pygame.time.Clock()
        # default direction
        self.direction = Moving.RIGHT
        # snake head and snake body, 3 blocks long
        self.head = Point(self.w/2, self.h/2)
        self.snake = [self.head, Point(self.head.x-BLOCK_SIZE, self.head.y), Point(self.head.x-(2*BLOCK_SIZE), self.head.y)]
        self.score = 0
        self.food = None
        self._place_food()
    
    def _place_food(self):
        """
        place food for my cutie snakes to eat
        """
        # randomly put the food
        x = random.randint(0,(self.w - BLOCK_SIZE)//BLOCK_SIZE) * BLOCK_SIZE
        y = random.randint(0,(self.h - BLOCK_SIZE)//BLOCK_SIZE) * BLOCK_SIZE
        self.food = Point(x,y)

        # recursive function to check if the coords with the snake and food overlap
        # overlap = bad, generate new food to makan
        if self.food in self.snake:
            self._place_food()

    def play_step(self):
        # get user input
        for input in pygame.event.get():
            if input.type == pygame.QUIT:
                pygame.quit()
                quit()
            if input.type == pygame.KEYDOWN:
                if input.key == pygame.K_LEFT:
                    self.direction = Moving.LEFT
                elif input.key == pygame.K_RIGHT:
                    self.direction = Moving.RIGHT
                elif input.key == pygame.K_UP:
                    self.direction = Moving.UP
                elif input.key == pygame.K_DOWN:
                    self.direction = Moving.DOWN
        
        # update the head
        self._move(self.direction)
        self.snake.insert(0,self.head)

        # check if snake runs into border
        self.update_ui()
        self.clock.tick(SPEED)
        # game over
        gg = False
        return gg, self.score


    def update_ui(self):
        # background
        self.display.fill(BLACK)

        for i in self.snake:
            pygame.draw.rect(self.display, GREEN, pygame.Rect(i.x,i.y, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(self.display, LIGHT_GREEN, pygame.Rect(i.x+4,i.y+5, 12,12))
        pygame.draw.rect(self.display,RED,pygame.Rect(self.food.x, self.food.y, BLOCK_SIZE, BLOCK_SIZE))

        text = font.render("Score: " + str(self.score), True, WHITE)
        self.display.blit(text, [0,0])
        pygame.display.flip()

    def _move(self, direction):
        # get the current snake coords
        x = self.head.x
        y = self.head.y

        if direction == Moving.RIGHT:
            x += BLOCK_SIZE
        elif direction == Moving.LEFT:
            x -= BLOCK_SIZE
        elif direction == Moving.UP:
            y -= BLOCK_SIZE
        elif direction == Moving.DOWN:
            y += BLOCK_SIZE
        
        # update coords
        self.head = Point(x,y)


# driver code
if __name__ == '__main__':
    start_game = SnakeGame()

    while True:
        gg, score = start_game.play_step()
        
        if gg == True:
            break
    print('Final Score', score)
    pygame.quit()