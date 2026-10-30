import pygame
from sys import exit
import random
import time 
import os
import sys

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Physics
GRAVITY = 0.8
JUMP_STRENGTH = -16
PLAYER_SPEED = 5

MARIO = pygame.transform.scale(pygame.image.load(resource_path("images/mario.png")), (50, 50))

