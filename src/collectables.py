import os
import random
import sys

import pygame

from settings import ROOT_PATH, WIDTH, HEIGHT, OFFSET_Y, FRUIT_NAMES, COIN_NAME, BOMB_NAME, UI_HEIGHT
from player import Player


def load_image(name: str, colorkey=None):
    fullname = os.path.join(ROOT_PATH, 'gfx', name)

    if not os.path.isfile(fullname):
        sys.exit()
    image = pygame.image.load(fullname)
    return image


class Collectable(pygame.sprite.Sprite):

    def __init__(self, *group: pygame.sprite.Group, tag: str, screen: pygame.Surface) -> None:
        super().__init__(*group)
        self.group = group
        self.image = self.select_image(tag=tag)
        self.rect = self.image.get_rect()
        self.tag = tag
        self.screen = screen
        self.cnt = 0
        
        self.picking_fruit_coin_sound = pygame.mixer.Sound(os.path.join(ROOT_PATH, 'sfx', 'picking_fruit_coin.wav'))
        self.picking_fruit_coin_sound.set_volume(0.15)
        
        self.respawn()

    def respawn(self) -> None:
        self.image = pygame.transform.rotate(self.image, random.randrange(-15, 15))
        self.x = WIDTH + random.randrange(50, 150)
        self.y = random.randrange(OFFSET_Y, HEIGHT - UI_HEIGHT - OFFSET_Y - 10)
        self.cnt += 1
        self.show()

    def on_collide(self, user: Player) -> None:
        if not pygame.sprite.collide_mask(self, user):
            return
        if self.tag == 'coin':
            pygame.mixer.Sound.play(self.picking_fruit_coin_sound)
            user.coins += 1
        elif self.tag == 'bomb':
            user.health_points -= 1
        elif self.tag == 'fruit':
            pygame.mixer.Sound.play(self.picking_fruit_coin_sound)
            user.fruit += 1
        
        self.respawn()

    def select_image(self, tag: str) -> pygame.Surface:
        if tag == 'fruit':
            return load_image(name=random.choice(FRUIT_NAMES))
        elif tag == 'coin':
            return load_image(name=COIN_NAME)
        return load_image(BOMB_NAME)
    
    def show(self) -> None:
        self.screen.blit(self.image, self.rect)

    def update(self, user: Player, speed: float) -> None:
        self.x -= speed
        if self.x < - speed * 30:
            self.respawn()
        self.rect.topleft = (self.x, self.y)
        self.on_collide(user=user)

        self.show()
