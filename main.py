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
COIN_IMAGE = pygame.transform.scale(pygame.image.load(resource_path("images/coin.png")), (32, 32))

window = pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT))

class Player(pygame.sprite.Sprite):
    COLOR = (255, 0, 0)
    GRAVITY = 0.7
    JUMP_STRENGTH = 14
    MAX_FALL_SPEED = 15
    
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
            self.y_vel = -self.JUMP_STRENGTH
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
        if self.y_vel > self.MAX_FALL_SPEED:
            self.y_vel = self.MAX_FALL_SPEED
        
    
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

class Coin(Object):
    def __init__(self, x, y):
        super().__init__(x, y, 32, 32)
        self.image = COIN_IMAGE

class Flag(Object):
    def __init__(self, x, y):
        super().__init__(x, y, 40, 60)
        self.image.fill((0, 200, 0))

def draw(window, player, objects, coins, score, flag, won):
    window.fill("orange")
    player.draw(window)
    for obj in objects:
        obj.draw(window)
    for coin in coins:
        coin.draw(window)
    flag.draw(window)
    
    font = pygame.font.SysFont("arial", 28)
    score_text = font.render(f"Score: {score}", True, "black")
    window.blit(score_text, (10, 10))
    
    if won:
        win_text = font.render("You Win!", True, "green")
        window.blit(win_text, (GAME_WIDTH // 2 -60, GAME_HEIGHT // 2))

        restart_text = font.render("Press R to play again", True, "black")
        window.blit(restart_text, (GAME_WIDTH // 2 - 130, GAME_HEIGHT // 2 + 40))
    
    pygame.display.update()

def handle_physics_and_collision(player, objects):
    player.rect.x += player.x_vel
    
    for obj in objects:
        if player.rect.colliderect(obj.rect):
            if player.x_vel > 0:
                player.rect.right = obj.rect.left
            elif player.x_vel < 0:
                player.rect.left = obj.rect.right
    
    previous_bottom = player.rect.bottom
    player.rect.y += round(player.y_vel)
    player.on_ground = False
    
    for obj in objects:
        if (player.y_vel >= 0 and previous_bottom <= obj.rect.top and player.rect.bottom >= obj.rect.top and player.rect.right > obj.rect.left and player.rect.left < obj.rect.right):
                player.rect.bottom = obj.rect.top
                player.landed()
        elif (player.y_vel < 0 and player.rect.colliderect(obj.rect)):
            player.rect.top = obj.rect.bottom
            player.hit_head()



def handle_move(player):
    player.x_vel = 0
    
    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_LEFT]:
        player.move_left(PLAYER_VEL)
    if keys[pygame.K_RIGHT]:
        player.move_right(PLAYER_VEL)

def main(window):
    clock = pygame.time.Clock()
    block_size = 64
    
    player = Player(10, GAME_HEIGHT - block_size - 50, 50, 50, MARIO_IMAGE)
    
    blocks = []
    def make_platform(x, y, count):
        for i in range(count):
            blocks.append(Block(x+ i * block_size, y, block_size))
    make_platform(250, 450, 3)
    make_platform(700, 450, 2)
    make_platform(0, 350, 2)
    make_platform(200, 220, 1)
    make_platform(425, 100, 2)
    make_platform(0, GAME_HEIGHT - block_size, 4)
    coins = [Coin(285, 400), Coin(65, 300), Coin(215, 170), Coin(465, 50),]
    score = 0
    flag = Flag(700, 400)
    won = False
    
    def reset_level():
        nonlocal player, coins, score, won
        player = Player (10, GAME_HEIGHT - block_size - 50, 50, 50, MARIO_IMAGE)
        coins = [Coin(285, 400), Coin(65, 300), Coin(215, 170), Coin(465, 50),]
    
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    player.jump()
                if event.key == pygame.K_r and won:
                    reset_level()
            
        handle_move(player)
        player.loop(FPS)
        handle_physics_and_collision(player, blocks)
        for coin in coins[:]:
            if player.rect.colliderect(coin.rect):
                coins.remove(coin)
                score += 1
                
        if player.rect.colliderect(flag.rect):
            won= True
        if won:
            player.x_vel = 0
        clock.tick(FPS)
        draw(window, player, blocks, coins, score, flag, won)

    pygame.quit()
    quit()

if __name__ == "__main__" :
    main(window)