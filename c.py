#!/usr/bin/env python3
"""A simple skiing game.

Day-iteration:
5-1: clean up
5-2: Sprite class
3-3: Sprite group and update() function
5-4: Collisions
5-5: Regeneration of crashed trees
5-6: Flags and points
5-7: Player class and image directions
5-8: Sounds
5-9: Crash handling and game end
5-a: Score and messages
5-b: Image class
5-c: Jumping
"""
import os
import random

import pygame


BOARD_SIZE = BOARD_WIDTH, BOARD_HEIGHT = 480, 640
FRAME_RATE = 30
BOARD_COLOR = (255, 255, 255)
PLAYER_SPEED = 5
DOWNHILL_SPEED = 4
TREES_MAX = 10
FLAGS_MAX = 10
RAMPS_MAX = 3
POINTS = 10
IMAGE_FILES = (
    'kiiro',
    'kiiro-se',
    'kiiro-sw',
    'kiiro-shadow',
    'kiiro-stunned',
    'tree',
    'flag',
    'rainbow',
    )
IMAGE_PATH = 'images'
SOUND_FILES = (
    'bonus',
    'crash',
    'gameover',
    'jump',
    )
SOUND_PATH = 'sounds'
BG_MUSIC = 'music'
CRASH_MAX = 3  # How many crashes are allowed before the game ends
CRASH_TIME = FRAME_RATE * 2  # How many seconds each crash delays the game
JUMP_TIME = FRAME_RATE * 2  # How many seconds to get to maximum height
TEXT_SIZE = 40
TEXT_COLOR = (204, 0, 255)

pygame.init()

BOARD = pygame.display.set_mode(BOARD_SIZE)
CLOCK = pygame.time.Clock()


class ImageStore:
    """Storage for images.
    """
    def __init__(self, path='', ext='png'):
        """Initialize the image store with location and type of images.

        Args:
            path: Path to images folder
            ext: Extension for imagesfiles, with no dot.
        """
        self.store = {}
        self.path = path
        self.ext = ext.strip('.')

    def get(self, name):
        """Get an image in the image store.

        Not a great idea, but combines add() and get() in one function.

        Args:
            name: Name of image (also the file base name).

        Returns:
            image object added.
        """
        if name not in self.store:
            image_file = os.path.join(self.path, f'{name}.{self.ext}')
            try:
                image = pygame.image.load(image_file).convert_alpha()
            except:
                image = text2image(name, 20, (255, 0, 0))
            self.store[name] = image
        else:
            image = self.store[name]
        return image


class SoundStore:
    """Storage for sounds.
    """
    def __init__(self, path='', ext='wav'):
        """Initialize the sound store with location and type of sounds.

        Args:
            path: Path to sound folder
            ext: Extension for sound files, with no dot.
        """
        self.store = {}
        self.path = path
        self.ext = ext.strip('.')

    def add(self, name):
        """Add a sound to the store by name.

        Args:
            name: Name of sound to store (the base name of the file)

        Returns:
        """
        status = True
        if name not in self.store:
            sound_file = os.path.join(self.path, f'{name}.{self.ext}')
            try:
                sound = pygame.mixer.Sound(sound_file)
                self.store[name] = sound
            except:
                status = False
        else:
            print(f'NOTICE: Sound {name} is already in the sound store.')
        return status

    def play(self, name):
        """Play sound in the sound store.

        Args:
            name: Name of the sound to play.
        """
        if name in self.store:
            self.store[name].play()

    def bg_start(self, name):
        """Play background music.

        Args:
            name: Name of a file to use as background music.
        """
        sound_file = os.path.join(self.path, f'{name}.{self.ext}')
        pygame.mixer.music.load(sound_file)
        pygame.mixer.music.play(-1, 0.0)

    def bg_stop(self):
        """Stop background music.
        """
        pygame.mixer.music.stop()


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
        self.image = IMAGES.get(name)
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
        self.image_left = IMAGES.get(f'{self.name}-sw')
        self.image_right = IMAGES.get(f'{self.name}-se')
        self.image_shadow = IMAGES.get(f'{self.name}-shadow')
        self.image_crash = IMAGES.get(f'{self.name}-stunned')
        self.score = 0
        self.crashes = 0
        self.crash_time = 0
        self.jumping = False
        self.jump_time = 0

    def draw(self, board):
        """Create a draw() method to be consistent with Sprite Groups.

        Args:
            board: A surface object (like BOARD)
        """
        if self.crash_time > 0:
            image = self.image_crash
        elif self.x_inc > 0:
            image = self.image_right
        elif self.x_inc < 0:
            image = self.image_left
        else:
            image = self.image_straight
        BOARD.blit(self.image_shadow, (self.rect.x, self.rect.y))
        if self.jump_time > 0:
            y_pos = self.rect.y - self.jump_time
        else:
            y_pos = self.rect.y
        BOARD.blit(image, (self.rect.x, y_pos))


def text2image(text, size=TEXT_SIZE, color=TEXT_COLOR):
    """Create an image from a text string.

    Args:
        text: Text to convert to an image.
        size: Text size, in points.
        color: RGP tuple, in decimal; example: (255, 0, 255) is magenta.

    Returns:
        An image object of the specified text.
    """
    font = pygame.font.Font(None, size)
    image = font.render(text, 1, color)
    return image


def show_stats(score, crashes):
    """Show player score and crash statistics on the board.

    Args:
        score: Integer value.
        crashes: Integer number of crashes the player has had.
    """
    text = f'Score: {score}  Crashes: {crashes}/{CRASH_MAX}'
    text_image = text2image(text)
    text_width, text_height = text_image.get_size()
    text_x = 50
    text_y = BOARD_HEIGHT - text_height
    BOARD.blit(text_image, (text_x, text_y))


def end_game():
    """Show game over message.
    """
    text_image = text2image('Game Over')
    text_width, text_height = text_image.get_size()
    center_x = (BOARD_WIDTH - text_width) // 2
    center_y = (BOARD_HEIGHT - text_height) // 2
    BOARD.blit(text_image, (center_x, center_y))
    pygame.display.flip()
    SOUNDS.bg_stop()
    SOUNDS.play('gameover')
    pygame.time.wait(5 * 1000)


IMAGES = ImageStore(IMAGE_PATH)
for image_file in IMAGE_FILES:
    IMAGES.get(image_file)

SOUNDS = SoundStore(SOUND_PATH)
for sound_file in SOUND_FILES:
    SOUNDS.add(sound_file)
SOUNDS.bg_start(BG_MUSIC)

player = Player('kiiro')
player.rect.x = (BOARD_WIDTH - player.width) // 2
player.rect.y = (BOARD_HEIGHT - player.height) // 2
player.speed = PLAYER_SPEED

trees = pygame.sprite.Group()
flags = pygame.sprite.Group()
ramps = pygame.sprite.Group()

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

    if player.jumping:
        player.jump_time += 1
        if player.jump_time >= JUMP_TIME:
            player.jumping = False
    elif player.jump_time > 0:
        player.jump_time -= 1

    if player.crash_time > 0:
        player.crash_time -= 1
    else:
        player.update()
        trees.update()
        flags.update()
        ramps.update()

    if player.rect.x < 0:
        player.rect.x = 0
    elif player.rect.x > BOARD_WIDTH - player.width:
        player.rect.x = BOARD_WIDTH - player.width
    if player.rect.y < 0:
        player.rect.y = 0
    elif player.rect.y > BOARD_HEIGHT - player.height:
        player.rect.y = BOARD_HEIGHT - player.height

    if len(trees) < TREES_MAX:
        tree = Character('tree')
        tree.rect.x = random.randint(0, BOARD_WIDTH - tree.width)
        tree.rect.y = random.randint(0, BOARD_HEIGHT) + BOARD_HEIGHT
        tree.y_inc = -tree.speed
        trees.add(tree)

    if len(flags) < FLAGS_MAX:
        flag = Character('flag')
        flag.rect.x = random.randint(0, BOARD_WIDTH - flag.width)
        flag.rect.y = random.randint(0, BOARD_HEIGHT) + BOARD_HEIGHT
        flag.y_inc = -flag.speed
        flags.add(flag)

    if len(ramps) < RAMPS_MAX:
        ramp = Character('rainbow')
        ramp.rect.x = random.randint(0, BOARD_WIDTH - ramp.width)
        ramp.rect.y = random.randint(0, BOARD_HEIGHT) + BOARD_HEIGHT
        ramp.y_inc = -ramp.speed
        ramps.add(ramp)

    for tree in trees:
        if tree.rect.y < -tree.height:
            tree.rect.x = random.randint(0, BOARD_WIDTH - tree.width)
            tree.rect.y = BOARD_HEIGHT

    for flag in flags:
        if flag.rect.y < -flag.height:
            flag.rect.x = random.randint(0, BOARD_WIDTH - flag.width)
            flag.rect.y = BOARD_HEIGHT

    for ramp in ramps:
        if ramp.rect.y < -ramp.height:
            ramp.rect.x = random.randint(0, BOARD_WIDTH - ramp.width)
            ramp.rect.y = BOARD_HEIGHT

    if player.jump_time == 0:
        hits = pygame.sprite.spritecollide(player, trees, dokill=True)
        for hit in hits:
            SOUNDS.play('crash')
            player.score -= hit.points
            player.crashes += 1
            player.crash_time = CRASH_TIME

        hits = pygame.sprite.spritecollide(player, flags, dokill=True)
        for hit in hits:
            SOUNDS.play('bonus')
            player.score += hit.points

        hits = pygame.sprite.spritecollide(player, ramps, dokill=False)
        for hit in hits:
            SOUNDS.play('jump')
            player.score += hit.points
            player.jumping = True

    trees.draw(BOARD)
    flags.draw(BOARD)
    ramps.draw(BOARD)
    player.draw(BOARD)
    show_stats(player.score, player.crashes)

    if player.crashes >= CRASH_MAX:
        game_on = False

    pygame.display.flip()
    CLOCK.tick(FRAME_RATE)
end_game()

pygame.quit()
