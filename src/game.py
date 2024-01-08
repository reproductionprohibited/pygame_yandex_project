import os
import sys

import pygame

from dbmanager import DBManager
from player import Player
from settings import TITLE, WIDTH, HEIGHT, UI_HEIGHT, COLLECTABLE_SPEED, FRAMERATE, ROOT_PATH
from collectables import Collectable
from ui import UI


class Game:

    BG_COLOR = pygame.color.Color((149, 205, 246, 75))

    def __init__(self) -> None:
        pygame.init()
        pygame.font.init()
        pygame.mixer.init()

        pygame.display.set_caption(TITLE)

        self.width, self.height = WIDTH, HEIGHT
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.gameover_sound = pygame.mixer.Sound(os.path.join(ROOT_PATH, 'sfx', 'game_over.wav'))
        self.gameover_sound.set_volume(0.15)

        self.bg_music = pygame.mixer.music.load(os.path.join(ROOT_PATH, 'sfx', 'bg_music.mp3'))
        pygame.mixer.music.set_volume(0.05)

        self.init_coin_group()
        self.init_fruit_group()
        self.init_bomb_group()

        self.player = Player(db=DBManager(db_filepath='database.db'), surface=self.screen)
        self.x, self.y = 75, self.height // 2

        self.clock = pygame.time.Clock()
        self.ticks = 0
        self.points = 0
        self.is_game_in_process = False
        self.started_playing = False
        self.is_game_over = False
        self.is_displaying_run_data = False
        self.collectable_speed = COLLECTABLE_SPEED
        self.delta_speed = 0.3
        self.player_angle = 0
        self.anim_step = 0

        pygame.mixer.music.play(-1)
        self.ui = UI(
            screen=self.screen,
            player=self.player,
        )
        self.ui.render_ingame()


    def init_coin_group(self) -> None:
        self.coin_group = pygame.sprite.Group()
        for _ in range(5):
            coin = Collectable(
                self.coin_group,
                tag='coin',
                screen=self.screen,
            )
            coin.image = coin.image.convert_alpha()
    
    def init_fruit_group(self) -> None:
        self.fruit_group = pygame.sprite.Group()
        for _ in range(4):
            fruit = Collectable(
                self.fruit_group,
                tag='fruit',
                screen=self.screen,
            )
            fruit.image = fruit.image.convert_alpha()
    
    def init_bomb_group(self) -> None:
        self.bomb_group = pygame.sprite.Group()
        for _ in range(6):
            bomb = Collectable(
                self.bomb_group,
                tag='bomb',
                screen=self.screen,
            )
            bomb.image = bomb.image.convert_alpha()

    def game_over(self) -> None:
        if not self.played_sound:
            pygame.mixer.Sound.play(self.gameover_sound)
            self.played_sound = True
        self.ui.render_game_over()

    def game_process_run(self) -> None:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.y -= self.player.speed
            self.player_angle = 20
        elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.y += self.player.speed
            self.player_angle = -20
        else:
            self.player_angle = 0
        if self.y < 0:
            self.y = 0
        elif self.y > self.height - UI_HEIGHT - self.player.rect.height:
            self.y = self.height - UI_HEIGHT - self.player.rect.height

        self.screen.fill(Game.BG_COLOR)
        self.player.render_sprite(x=self.x, y=self.y, angle=self.player_angle, animstep = self.anim_step)

        self.coin_group.update(user=self.player, speed=self.collectable_speed)
        self.fruit_group.update(user=self.player, speed=self.collectable_speed)
        self.bomb_group.update(user=self.player, speed=self.collectable_speed)

        self.ui.render_ingame()

        self.ticks += 0.5
        if self.ticks % 10 == 0:
            self.anim_step= (self.anim_step + 1) % 4
        if self.ticks >= 60:
            self.ticks = 0
            self.player.points += 1
            self.collectable_speed = round(self.collectable_speed + self.delta_speed, 1)
        if self.collectable_speed >= 5:
            self.collectable_speed = 5
            self.delta_speed = 0
        if self.player.health_points <= 0:
            self.is_game_in_process = False
            self.player.save_res()
            
            return

    def setup(self) -> None:
        self.played_sound = False
        self.screen.fill('black')
        self.init_coin_group()
        self.init_fruit_group()
        self.init_bomb_group()
        self.player.reset()
        self.delta_speed = 0.3
        
        self.x, self.y = 75, self.height // 2

        self.ticks = 0
        self.points = 0
        self.is_game_over = False
        self.collectable_speed = COLLECTABLE_SPEED

        self.ui.render_ingame()


    def launch(self) -> None:
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                keys = pygame.key.get_pressed()

                # Game thumbnail
                if not self.started_playing and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    button_width = 86.5
                    button_height = 23.5
                    mousex, mousey = pygame.mouse.get_pos()
                    self.is_displaying_run_data = True
                    if 29.5 * 2 <= mousex <= (29.5 + button_width) * 2 and 221.5 * 2 <= mousey <= (221.5 + button_height) * 2:
                        self.ui.render_top_runs(by='pts')
                    elif 156.5 * 2 <= mousex <= (156.5 + button_width) * 2 and 221.5 * 2 <= mousey <= (221.5 + button_height) * 2:
                        self.ui.render_top_runs(by='coins')
                    elif 283.5 * 2 <= mousex <= (283.5 + button_width) * 2 and 221.5 * 2 <= mousey <= (221.5 + button_height) * 2:
                        self.ui.render_top_runs(by='fruit')
                    elif 156.5 * 2 <= mousex <= (156.5 + button_width) * 2 and 257 * 2 <= mousey <= (257 + button_height) * 2:
                        self.ui.render_top_runs(by='overall')

                    continue
                
                if self.is_displaying_run_data and keys[pygame.K_ESCAPE]:
                    self.is_displaying_run_data = False

                # First launch of the game
                if keys[pygame.K_SPACE] and not self.started_playing:
                    # self.player.reset()
                    self.setup()
                    self.is_game_in_process = True
                    self.started_playing = True

                # After game over
                elif keys[pygame.K_SPACE] and self.is_game_over and self.started_playing:
                    # self.player.reset()
                    self.setup()
                    self.ui.reset_game_over_plank()
                    self.is_game_in_process = True
                    self.is_game_over = False

            if not self.started_playing and not self.is_displaying_run_data:
                self.ui.render_game_thumbnail()
            if self.is_game_in_process:
                self.game_process_run() 
            elif self.started_playing and not self.is_game_in_process:
                self.game_over()
            if self.ui.gameover_slide_speed == 0:
                self.is_game_over = True

            if self.is_game_in_process and keys[pygame.K_ESCAPE]:
                self.started_playing = False
                self.is_game_in_process = False

            if self.is_game_over and keys[pygame.K_ESCAPE]:
                self.started_playing = False
                self.is_game_in_process = False
                self.is_game_over = False

            pygame.display.flip()
            self.clock.tick(FRAMERATE)

        pygame.quit()

        sys.exit()
