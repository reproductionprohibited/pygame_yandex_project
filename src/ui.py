from typing import List

import pygame

from collectables import load_image
from player import Player
from settings import UI_OFFSET_X, UI_HEIGHT, WIDTH, HEIGHT, UI_MARGIN_Y


class UI:

    red_heart_img = load_image('hearts/red_heart.png')
    black_heart_img = load_image('hearts/black_heart.png')
    coin_img = load_image('coin/coin_36x36.png')
    fruit_img = load_image('fruit/banana_48x48.png')
    finishline_img = load_image('finishline/finishline.png')
    gameover_img = load_image('gameover/gameover2.png')

    game_thumbnail_img = load_image('thumbnails/game_thumbnail1.png')
    topruns_coins_btn = load_image('buttons/topruns_coins_btn.png')
    topruns_fruit_btn = load_image('buttons/topruns_fruit_btn.png')
    topruns_points_btn = load_image('buttons/topruns_points_btn.png')
    topruns_overall_btn = load_image('buttons/topruns_overall_btn.png')

    bg_topruns_pts = load_image('thumbnails/background_best_runs_pts.png')
    bg_topruns_coins = load_image('thumbnails/background_best_runs_coins.png')
    bg_topruns_fruit = load_image('thumbnails/background_best_runs_fruit.png')
    bg_topruns_overall = load_image('thumbnails/background_best_runs_overall.png')

    def __init__(self, screen: pygame.Surface, player: Player) -> None:
        self.player = player
        self.screen = screen
        self.gameover_rect = UI.gameover_img.get_rect()
        self.gameover_rect.x = -WIDTH
        self.gameover_rect.y = 0
        self.gameover_slide_speed = 3

    def reset_game_over_plank(self) -> None:
        self.gameover_rect.x = -WIDTH
        self.gameover_rect.y = 0
        self.gameover_slide_speed = 3
    
    def render_top_runs(self, by: str) -> None:
        if by == 'pts':
            data = [it[0] for it in self.player.db.get_top_runs_points()]
        elif by == 'coins':
            data = [it[0] for it in self.player.db.get_top_runs_coins()]
        elif by == 'fruit':
            data = [it[0] for it in self.player.db.get_top_runs_fruit()]
        elif by == 'overall':
            data = [it[0] for it in self.player.db.get_top_runs_sum()]
        while len(data) < 3:
            data.append('No run data')

        bg = self.get_background_image_for_topruns(by=by)
        self.render_best_runs(bg=bg, data=data)

    def render_best_runs(self, bg: pygame.Surface, data: List[int]) -> None:
        text_x = 109 * 2 + 55
        text_y1 = 92 * 2 + 6
        text_y2 = 139 * 2 + 6
        text_y3 = 186 * 2 + 6

        self.screen.blit(
            bg,
            (0, 0),
        )
        run1, run2, run3 = data

        run1_text = pygame.font.Font(None, 40).render(
            str(run1),
            1,
            (255, 255, 255),
        )
        self.screen.blit(
            run1_text,
            (text_x, text_y1),
        )
        
        run2_text = pygame.font.Font(None, 40).render(
            str(run2),
            1,
            (255, 255, 255),
        )
        self.screen.blit(
            run2_text,
            (text_x, text_y2),
        )

        run3_text = pygame.font.Font(None, 40).render(
            str(run3),
            1,
            (255, 255, 255),
        )
        self.screen.blit(
            run3_text,
            (text_x, text_y3),
        )


    def get_background_image_for_topruns(self, by: str) -> pygame.Surface:
        if by == 'pts':
            return UI.bg_topruns_pts
        elif by == 'coins':
            return UI.bg_topruns_coins
        elif by == 'fruit':
            return UI.bg_topruns_fruit
        elif by == 'overall':
            return UI.bg_topruns_overall

    def render_game_over(self) -> None:
        self.gameover_rect = self.gameover_rect.move(self.gameover_slide_speed, 0)
        if self.gameover_rect.x >= 0:
            self.gameover_slide_speed = 0
            self.gameover_rect.x = 0
        self.screen.blit(
            UI.gameover_img,
            self.gameover_rect,
        )

    def render_game_thumbnail(self) -> None:
        # background
        self.screen.blit(
            UI.game_thumbnail_img,
            (0, 0),
        )

        # interactive buttons
        self.screen.blit(
            UI.topruns_points_btn,
            (29.5 * 2, 221.5 * 2)
        )
        
        self.screen.blit(
            UI.topruns_coins_btn,
            (156.5 * 2, 221.5 * 2)
        )

        self.screen.blit(
            UI.topruns_fruit_btn,
            (283.5 * 2, 221.5 * 2)
        )

        self.screen.blit(
            UI.topruns_overall_btn,
            (156.5 * 2, 257 * 2)
        )
        
    def render_ingame(self) -> None:
        # background
        pygame.draw.line(
            surface=self.screen,
            color=pygame.color.Color(87, 86, 82),
            start_pos=(0, HEIGHT - UI_HEIGHT),
            end_pos=(WIDTH, HEIGHT - UI_HEIGHT),
            width=2,
        )

        pygame.draw.rect(
            surface=self.screen,
            color=pygame.color.Color(31, 64, 52),
            rect=(
                0, HEIGHT - UI_HEIGHT + 2,
                WIDTH, HEIGHT - UI_HEIGHT + 2,
            )
        )

        # quit instructions
        quit_text = pygame.font.Font(None, 20).render(
            'To exit, press ESCAPE',
            1,
            (255, 255, 255),
        )
        self.screen.blit(
            quit_text,
            (10, HEIGHT - 16),
        )

        # health
        heart_xs = [UI_OFFSET_X, UI_OFFSET_X + 15 + UI.red_heart_img.get_width(), UI_OFFSET_X + 2 * (15 + UI.red_heart_img.get_width())]

        for i, heart_x in enumerate(heart_xs):
            if self.player.health_points > i:
                self.screen.blit(
                    UI.red_heart_img,
                    (heart_x, HEIGHT - UI_HEIGHT + UI_MARGIN_Y),
                )
            else:
                self.screen.blit(
                    UI.black_heart_img,
                    (heart_x, HEIGHT - UI_HEIGHT + UI_MARGIN_Y),
                )
        
        deltax = (WIDTH - heart_xs[-1] - 100) // 4
        
        # fruit
        fruit_x = heart_xs[-1] + deltax
        self.screen.blit(
            UI.fruit_img,
            (fruit_x, HEIGHT - UI_HEIGHT + UI_MARGIN_Y - 1),
        )
        fruit_text = pygame.font.Font(None, 48).render(
            str(self.player.fruit),
            1,
            (255, 255, 255),
        )
        self.screen.blit(fruit_text, (fruit_x + UI.fruit_img.get_width() + 10, HEIGHT - UI_HEIGHT + UI_MARGIN_Y + 8))
        
        # coin
        coin_x = fruit_x + deltax
        self.screen.blit(
            UI.coin_img,
            (coin_x, HEIGHT - UI_HEIGHT + UI_MARGIN_Y + 6),
        )
        coin_text = pygame.font.Font(None, 48).render(
            str(self.player.coins),
            1,
            (255, 255, 255),
        )
        self.screen.blit(coin_text, (coin_x + UI.coin_img.get_width() + 10, HEIGHT - UI_HEIGHT + UI_MARGIN_Y + 8))

        # points
        points_x = fruit_x + 2 * deltax
        self.screen.blit(
            UI.finishline_img,
            (points_x, HEIGHT - UI_HEIGHT + UI_MARGIN_Y),
        )
        points_text = pygame.font.Font(None, 48).render(
            str(self.player.points),
            1,
            (255, 255, 255),
        )
        self.screen.blit(points_text, (points_x + UI.coin_img.get_width() + 13, HEIGHT - UI_HEIGHT + UI_MARGIN_Y + 8))
