#!/usr/bin/env python3
"""A simple skiing game.

Day-iteration:
5-1: clean up
5-2: Sprite class
3-3: Sprite group and update() function
5-4: Collisions
5-5: Regeneration
5-6: Flags and points
5-7: Player class and image directions
"""
import random

import pygame


BOARD_SIZE = BOARD_WIDTH, BOARD_HEIGHT = 480, 640
FRAME_RATE = 30
BOARD_COLOR = (255, 255, 255)
PLAYER_SPEED = 5
DOWNHILL_SPEED = 4
TREES_MAX = 10
FLAGS_MAX = 10
POINTS = 10

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
        self.points = POINTS

    def update(self):
        """Update character position and paste on game board.

        Overrides the default update() method in the Sprite() class.
        """
        self.rect.x += self.x_inc
        self.rect.y += self.y_inc


class Player(Character):
    """Player class, which inherits from Character
    """
    def __init__(self, name):
        """Initialize the player object

        Args:
            name: Name of character (and image file)
        """
        super().__init__(name)
        self.image_straight = self.image
        self.image_left = pygame.image.load(f'images/{self.name}-sw.png')
        self.image_right = pygame.image.load(f'images/{self.name}-se.png')
        self.image_shadow = pygame.image.load(f'images/{self.name}-shadow.png')
        self.score = 0

    def draw(self, board):
        """Create a draw() method to be consistent with Sprite Groups.

        Args:
            board: A surface object (like BOARD)
        """
        if self.x_inc > 0:
            image = self.image_right
        elif self.x_inc < 0:
            image = self.image_left
        else:
            image = self.image_straight
        BOARD.blit(self.image_shadow, (player.rect.x, player.rect.y))
        BOARD.blit(image, (player.rect.x, player.rect.y))


player = Player('kiiro')
player.rect.x = (BOARD_WIDTH - player.width) // 2
player.rect.y = (BOARD_HEIGHT - player.height) // 2
player.speed = PLAYER_SPEED

trees = pygame.sprite.Group()
flags = pygame.sprite.Group()

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

    if player.rect.x < 0:
        player.rect.x = 0
    elif player.rect.x > BOARD_WIDTH - player.width:
        player.rect.x = BOARD_WIDTH - player.width
    if player.rect.y < 0:
        player.rect.y = 0
    elif player.rect.y > BOARD_HEIGHT - player.height:
        player.rect.y = BOARD_HEIGHT - player.height

    player.draw(BOARD)

    if len(trees) < TREES_MAX:
        tree = Character('tree')
        tree.rect.x = random.randint(0, BOARD_WIDTH - tree.width)
        tree.rect.y = random.randint(0, BOARD_HEIGHT) + BOARD_HEIGHT
        tree.y_inc = -tree.speed
        trees.add(tree)

    trees.update()

    for tree in trees:
        if tree.rect.y < -tree.height:
            tree.rect.x = random.randint(0, BOARD_WIDTH - tree.width)
            tree.rect.y = BOARD_HEIGHT

    hits = pygame.sprite.spritecollide(player, trees, dokill=True)
    for hit in hits:
        print('Ouch!')
        player.score -= hit.points

    trees.draw(BOARD)

    if len(flags) < FLAGS_MAX:
        flag = Character('flag')
        flag.rect.x = random.randint(0, BOARD_WIDTH - flag.width)
        flag.rect.y = random.randint(0, BOARD_HEIGHT) + BOARD_HEIGHT
        flag.y_inc = -flag.speed
        flags.add(flag)
    flags.update()

    for flag in flags:
        if flag.rect.y < -flag.height:
            flag.rect.x = random.randint(0, BOARD_WIDTH - flag.width)
            flag.rect.y = BOARD_HEIGHT

    hits = pygame.sprite.spritecollide(player, flags, dokill=True)
    for hit in hits:
        print('Yeah!')
        player.score += hit.points

    flags.draw(BOARD)

    pygame.display.flip()
    CLOCK.tick(FRAME_RATE)

pygame.quit()
