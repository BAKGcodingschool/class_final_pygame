#!/usr/bin/env python3
"""A simple skiing game.
"""
import pygame

BOARD_SIZE = BOARD_WIDTH, BOARD_HEIGHT = 600, 800
FRAME_RATE = 20

pygame.init()

BOARD = pygame.display.set_mode(BOARD_SIZE)
CLOCK = pygame.time.Clock()

player_x = 50
player_y = 50
player_x_inc = 0
player_y_inc = 0
player_image_center = pygame.image.load('images/kiiro.png')
player_image_left = pygame.image.load('images/kiiro-sw.png')
player_image_right = pygame.image.load('images/kiiro-se.png')
PLAYER_SPEED = 5

BOARD_WIDTH, BOARD_HEIGHT = 600, 800
import random
tree_image = pygame.image.load('images/tree.png')
tree_width, tree_height = tree_image.get_size()
tree_x = random.randint(0, BOARD_WIDTH - tree_width)
tree_y = random.randint(0, BOARD_HEIGHT)
DOWNHILL_SPEED = 4
tree_y_inc = -DOWNHILL_SPEED

tree_x2 = random.randint(0, BOARD_WIDTH - tree_width)
tree_y2 = random.randint(0, BOARD_HEIGHT)
tree_x3 = random.randint(0, BOARD_WIDTH - tree_width)
tree_y3 = random.randint(0, BOARD_HEIGHT)

game_on = True
speed_cheat_key_count = 0
direction = 0   # 6: 0 for center, 1 for left, 2 for right
while game_on:
    BOARD.fill((255, 255, 255))
    # 6: show different play icons for direction
    if direction == 0:
        BOARD.blit(player_image_center, (player_x, player_y))
    elif direction == 1:
        BOARD.blit(player_image_left, (player_x, player_y))
    elif direction == 2:
        BOARD.blit(player_image_right, (player_x, player_y))
    
    BOARD.blit(tree_image, (tree_x, tree_y))
    BOARD.blit(tree_image, (tree_x2, tree_y2))
    BOARD.blit(tree_image, (tree_x3, tree_y3))

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                game_on = False
            elif event.key == pygame.K_LEFT:
                player_x_inc = -PLAYER_SPEED
                direction = 1   # 6: left direction
            elif event.key == pygame.K_RIGHT:
                player_x_inc = PLAYER_SPEED
                direction = 2   # 6: right direction
            elif event.key == pygame.K_UP:
                player_y_inc = -PLAYER_SPEED
            elif event.key == pygame.K_DOWN:
                player_y_inc = PLAYER_SPEED
            elif event.key == pygame.K_s:
                speed_cheat_key_count = 1
            elif event.key == pygame.K_p and speed_cheat_key_count == 1:
                speed_cheat_key_count = 2
            elif event.key == pygame.K_e and speed_cheat_key_count == 2:
                speed_cheat_key_count = 3
            elif event.key == pygame.K_e and speed_cheat_key_count == 3:
                speed_cheat_key_count = 4
            elif event.key == pygame.K_d and speed_cheat_key_count == 4:
                speed_cheat_key_count = 5
                PLAYER_SPEED = 20
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                player_x_inc = 0
                direction = 0   # 6: center
            elif event.key == pygame.K_RIGHT:
                player_x_inc = 0
                direction = 0   # 6: center
            elif event.key == pygame.K_UP:
                player_y_inc = 0
            elif event.key == pygame.K_DOWN:
                player_y_inc = 0
    player_x = player_x + player_x_inc
    player_y = player_y + player_y_inc

    if player_x < 0:
        player_x = 0
    elif player_x > BOARD_WIDTH - 30:
        player_x = BOARD_WIDTH - 30
    if player_y < 0:
        player_y = 0
    elif player_y > BOARD_HEIGHT - 40:
        player_y = BOARD_HEIGHT - 40
                
    tree_y = tree_y + tree_y_inc
    if tree_y < -tree_height:
        tree_y = BOARD_HEIGHT
    tree_y2 = tree_y2 + tree_y_inc
    if tree_y2 < -tree_height:
        tree_y2 = BOARD_HEIGHT
    tree_y3 = tree_y3 + tree_y_inc
    if tree_y3 < -tree_height:
        tree_y3 = BOARD_HEIGHT

    pygame.display.flip()
    CLOCK.tick(FRAME_RATE)

pygame.quit()
