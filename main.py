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

MARIO_IMAGE = pygame.transform.scale(pygame.image.load(resource_path("images/mario.png")), (50, 50))
BLOCK1_IMAGE = pygame.transform.scale(pygame.image.load(resource_path("images/block1.png")), (50, 50))
BLOCK2_IMAGE = pygame.transform.scale(pygame.image.load(resource_path("images/block2.png")), (50, 50))
BLOCK3_IMAGE = pygame.transform.scale(pygame.image.load(resource_path("images/block3.png")), (50, 50))
DIRT_BLOCK_IMAGE = pygame.image.load(resource_path("images/dirt_block.png"))
MYSTERY_BLOCK_IMAGE = pygame.transform.scale(pygame.image.load(resource_path("images/mystery_block.png")), (50, 50))
PIPE_IMAGE = pygame.transform.scale(pygame.image.load(resource_path("images/pipe.png")), (50, 50))

window = pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT))

class Player(pygame.sprite.Sprite):
    COLOR = (255, 0, 0)
    GRAVITY = 0.8
    
    def __init__(self, x, y, width, height, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.x_vel = 0
        self.y_vel = 0
        self.mask = pygame.mask.from_surface(self.image)
        self.direction = "left"
        self.animation_count = 0
        self.fall_count = 0
        self.jump_count = 0
        self.on_ground = False
        
    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

    def move_left(self, vel):
        self.x_vel = -vel
        if self.direction != "left":
            self.direction = "left"
            self.animation_count = 0

    def move_right(self, vel):
        self.x_vel = vel
        if self.direction != "right":
            self.direction = "right"
            self.animation_count = 0

    def jump(self):
        if self.on_ground:
            self.y_vel = -14
            self.fall_count = 0
            self.on_ground = False

    def landed(self):
        self.fall_count = 0
        self.y_vel = 0
        self.on_ground = True

    def hit_head(self):
        self.fall_count = 0
        self.y_vel = 0

    def loop(self, fps):
        self.y_vel += self.GRAVITY
        if self.y_vel > 15:
            self.y_vel = 15
        
        self.move(self.x_vel, 0)
        self.fall_count += 1
    
    def draw(self, win):
        win.blit(self.image, self.rect)

def get_block(size):
    return pygame.transform.scale(DIRT_BLOCK_IMAGE, (size, size))

class Object(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, name=None):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        self.width = width
        self.height = height
        self.name = name
        
    def draw(self, win):
        win.blit(self.image, (self.rect.x, self.rect.y))

class Block(Object):
    def __init__(self, x, y, size):
        super().__init__(x, y, size, size)
        block_image = get_block(size)
        self.image = block_image
        self.mask = pygame.mask.from_surface(self.image)

def draw(window, player, objects):
    window.fill("cadetblue3")
    player.draw(window)
    for obj in objects:
        obj.draw(window)
    
    pygame.display.update()

def handle_physics_and_collision(player, objects):
    player.rect.x += player.x_vel
    
    for obj in objects:
        if player.rect.colliderect(obj.rect):
            if player.x_vel > 0:
                player.rect.right = obj.rect.left
            elif player.x_vel < 0:
                player.rect.left = obj.rect.right
    
    player.rect.y += player.y_vel
    player.on_ground = False
    
    for obj in objects:
        if player.rect.colliderect(obj.rect):
            if player.y_vel >= 0:
                player.rect.bottom = obj.rect.top
                player.landed()
            elif player.y_vel < 0:
                player.rect.top = obj.rect.bottom
                player.hit_head

def handle_move(player):
    player.x_vel = 0
    
    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_LEFT]:
        player.move_left(PLAYER_VEL)
    if keys[pygame.K_RIGHT]:
        player.move_right(PLAYER_VEL)

def main(window):
    clock = pygame.time.Clock()
    block_size = 96
    
    player = Player(100, 100, 50, 50, MARIO_IMAGE)
    
    blocks = []
    for i in range(8):
        blocks.append(Block((i + 1)* block_size, GAME_HEIGHT - block_size, block_size))
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                    player.jump()
            
        handle_move(player)
        player.loop(FPS)
        handle_physics_and_collision(player, blocks)
        clock.tick(FPS)
        draw(window, player, blocks)

    pygame.quit()
    quit()

if __name__ == "__main__" :
    main(window)