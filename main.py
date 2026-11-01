import pygame
from sys import exit
import random
import time 
import os
import sys
from os.path import join
pygame.init()

pygame.display.set_caption("Halloween Mario") 

GAME_WIDTH = 800
GAME_HEIGHT = 600
FPS = 60
PLAYER_VEL = 5

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)

class Block(pygame.Rect):
    def __init__(self, coordinates, size, image):
        self.x = coordinates[0]
        self.y = coordinates[1]
        self.width = size[0]
        self.height = size[1]
        self.image = image
        self.velocity_x = 0
        self.velocity_y = 0

MARIO = pygame.transform.scale(pygame.image.load(resource_path("images/mario.png")), (50, 50))

window = pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT))

class Player(pygame.sprite.Sprite):
    pass

def draw(window):
    window.fill("cadetblue3")
    pygame.display.update()

def main(window):
    clock = pygame.time.Clock()
    
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
        draw(window)
        clock.tick(FPS)
    pygame.quit()
    quit()

if __name__ == "__main__" :
    main(window)