import pathlib

ROOT_PATH = pathlib.Path(__file__).parent.parent
PLAYER_SPRITE = [
    f'{ROOT_PATH}/gfx/player/anim1.png',
    f'{ROOT_PATH}/gfx/player/anim2.png',
    f'{ROOT_PATH}/gfx/player/anim3.png',
]
PLAYER_VERTICAL_SPEED = 5
COLLECTABLE_SPEED = 3
WIDTH = 800
HEIGHT = 600
OFFSET_Y = 30
UI_HEIGHT = 100
UI_MARGIN_Y = 30
UI_OFFSET_X = 30
TITLE = 'Side bird'
__COLLECTABLE_SPRITE_SIZE = '36x36'
FRUIT_NAMES = [f'fruit/banana_{__COLLECTABLE_SPRITE_SIZE}.png', f'fruit/berries_{__COLLECTABLE_SPRITE_SIZE}.png']
BOMB_NAME = f'bomb/bomb_{__COLLECTABLE_SPRITE_SIZE}.png'
COIN_NAME = f'coin/coin_{__COLLECTABLE_SPRITE_SIZE}.png'
FRAMERATE = 60