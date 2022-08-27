#!/usr/bin/env python3
"""A simple skiing game.

Day-iteration:
5-1: clean up
"""
import random

import pygame


BOARD_SIZE = BOARD_WIDTH, BOARD_HEIGHT = 480, 640
FRAME_RATE = 30
BOARD_COLOR = (255, 255, 255)
PLAYER_SPEED = 5
DOWNHILL_SPEED = 4

pygame.init()

BOARD = pygame.display.set_mode(BOARD_SIZE)
CLOCK = pygame.time.Clock()


player_image = pygame.image.load('images/kiiro.png')
player_width, player_height = player_image.get_size()
player_x = (BOARD_WIDTH - player_width) // 2
player_y = (BOARD_HEIGHT - player_height) // 2
player_x_inc = player_y_inc = 0

tree_image = pygame.image.load('images/tree.png')
tree_width, tree_height = tree_image.get_size()
tree_x = random.randint(0, BOARD_WIDTH - tree_width)
tree_y = random.randint(0, BOARD_HEIGHT)
tree_y_inc = -DOWNHILL_SPEED

game_on = True
while game_on:
    BOARD.fill(BOARD_COLOR)

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                game_on = False
            elif event.key == pygame.K_LEFT:
                player_x_inc = -PLAYER_SPEED
            elif event.key == pygame.K_RIGHT:
                player_x_inc = PLAYER_SPEED
            elif event.key == pygame.K_UP:
                player_y_inc = -PLAYER_SPEED
            elif event.key == pygame.K_DOWN:
                player_y_inc = PLAYER_SPEED
        elif event.type == pygame.KEYUP:
            if event.key in (pygame.K_LEFT, pygame.K_RIGHT):
                player_x_inc = 0
            elif event.key in (pygame.K_UP, pygame.K_DOWN):
                player_y_inc = 0

    player_x += player_x_inc
    player_y += player_y_inc

    if player_x < 0:
        player_x = 0
    elif player_x > BOARD_WIDTH - player_width:
        player_x = BOARD_WIDTH - player_width
    if player_y < 0:
        player_y = 0
    elif player_y > BOARD_HEIGHT - player_height:
        player_y = BOARD_HEIGHT - player_height

    BOARD.blit(player_image, (player_x, player_y))

    tree_y += tree_y_inc

    if tree_y < -tree_height:
        tree_y = BOARD_HEIGHT

    BOARD.blit(tree_image, (tree_x, tree_y))

    pygame.display.flip()
    CLOCK.tick(FRAME_RATE)

pygame.quit()
