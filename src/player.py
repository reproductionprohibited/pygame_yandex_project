import pygame

import dbmanager
from settings import PLAYER_SPRITE, PLAYER_VERTICAL_SPEED


class Player(pygame.sprite.Sprite):
    def __init__(
        self,
        db: dbmanager.DBManager,
        surface: pygame.Surface,
    ) -> None:
        super().__init__()

        self.image_anim1 = pygame.image.load(PLAYER_SPRITE[0]).convert_alpha()
        self.image_anim2 = pygame.image.load(PLAYER_SPRITE[1]).convert_alpha()
        self.image_anim3 = pygame.image.load(PLAYER_SPRITE[2]).convert_alpha()

        self.image_mask1 = pygame.mask.from_surface(self.image_anim1)
        self.image_mask2 = pygame.mask.from_surface(self.image_anim2)
        self.image_mask3 = pygame.mask.from_surface(self.image_anim3)

        self.rect = self.image_anim1.get_rect()
        self.image = self.image_anim1
        self.mask = self.image_mask1

        self.speed = PLAYER_VERTICAL_SPEED
        self.surface = surface
        self.db = db
        self.reset()

    def reset(self) -> None:
        self.coins = 0
        self.points = 0
        self.fruit = 0
        self.health_points = 3

    def set_image_and_mask(self, animstep: int) -> None:
        if animstep == 1:
            self.image = self.image_anim1
            self.mask = self.image_mask1
        elif animstep == 0 or animstep == 2:
            self.image = self.image_anim2
            self.mask = self.image_mask2
        elif animstep == 3:
            self.image = self.image_anim3
            self.mask = self.image_mask3

    def render_sprite(
        self,
        x: int,
        y: int,
        angle: int,
        animstep: int,
    ) -> None:
        self.set_image_and_mask(animstep=animstep)
        self.image = pygame.transform.rotate(self.image, angle)
        self.rect.topleft = (x, y)
        self.surface.blit(self.image, self.rect)

    def save_res(
        self,
    ) -> None:
        self.db.save_new_run_record(
            points=self.points,
            fruit=self.fruit,
            coins=self.coins,
        )

    def __str__(self) -> str:
        return f'Coins: {self.coins}; Fruit: {self.fruit}; Pts: {self.points}; Hp: {self.health_points}'