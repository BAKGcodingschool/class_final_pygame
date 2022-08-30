#!/usr/bin/env python3
"""A simple skiing game.

Day-iteration:
5-1: clean up
5-2: Sprite class
3-3: Sprite group and update() function
5-4: Collisions
"""
import random

import pygame


BOARD_SIZE = BOARD_WIDTH, BOARD_HEIGHT = 480, 640
FRAME_RATE = 30
BOARD_COLOR = (255, 255, 255)
PLAYER_SPEED = 5
DOWNHILL_SPEED = 4
TREES_MAX = 10

pygame.init()

BOARD = pygame.display.set_mode(BOARD_SIZE)
CLOCK = pygame.time.Clock()


class Character(pygame.sprite.Sprite):
    """Sprite class for characters.
    """
    def __init__(self, name):
        """Initialize character

        Args:
            name: Name of character (and image file)
        """
        super().__init__()
        self.name = name
        self.image = pygame.image.load(f'images/{self.name}.png')
        self.width, self.height = self.image.get_size()
        self.rect = self.image.get_rect()
        self.rect.x = self.rect.y = 0
        self.x_inc = self.y_inc = 0
        self.speed = DOWNHILL_SPEED

    def update(self):
        """Update character position and paste on game board.

        Overrides the default update() method in the Sprite() class.
        """
        self.rect.x += self.x_inc
        self.rect.y += self.y_inc


player = Character('kiiro')
player.rect.x = (BOARD_WIDTH - player.width) // 2
player.rect.y = (BOARD_HEIGHT - player.height) // 2
player.speed = PLAYER_SPEED

trees = pygame.sprite.Group()

for _ in range(TREES_MAX):
    tree = Character('tree')
    tree.rect.x = random.randint(0, BOARD_WIDTH - tree.width)
    tree.rect.y = random.randint(0, BOARD_HEIGHT)
    tree.y_inc = -tree.speed
    trees.add(tree)

game_on = True
while game_on:
    BOARD.fill(BOARD_COLOR)

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                game_on = False
            elif event.key == pygame.K_LEFT:
                player.x_inc = -player.speed
            elif event.key == pygame.K_RIGHT:
                player.x_inc = player.speed
            elif event.key == pygame.K_UP:
                player.y_inc = -player.speed
            elif event.key == pygame.K_DOWN:
                player.y_inc = player.speed
        elif event.type == pygame.KEYUP:
            if event.key in (pygame.K_LEFT, pygame.K_RIGHT):
                player.x_inc = 0
            elif event.key in (pygame.K_UP, pygame.K_DOWN):
                player.y_inc = 0

    player.update()
    trees.update()

    if player.rect.x < 0:
        player.rect.x = 0
    elif player.rect.x > BOARD_WIDTH - player.width:
        player.rect.x = BOARD_WIDTH - player.width
    if player.rect.y < 0:
        player.rect.y = 0
    elif player.rect.y > BOARD_HEIGHT - player.height:
        player.rect.y = BOARD_HEIGHT - player.height

    for tree in trees:
        if tree.rect.y < -tree.height:
            tree.rect.y = BOARD_HEIGHT
            tree.rect.x = random.randint(0, BOARD_WIDTH - tree.width)

    hits = pygame.sprite.spritecollide(player, trees, dokill=True)

    BOARD.blit(player.image, (player.rect.x, player.rect.y))
    trees.draw(BOARD)

    pygame.display.flip()
    CLOCK.tick(FRAME_RATE)

pygame.quit()
