import os


TOKEN = os.getenv('TG_TOKEN')

CONTINUE_GAME, FINISH_GAME = range(2)

FREE_SPACE = '.'
CROSS = 'X'
ZERO = 'O'

DEFAULT_STATE = [[FREE_SPACE for _ in range(3)] for _ in range(3)]

PLAYER_WIN_FLAG = 0
BOT_WIN_FLAG = 1
DRAW_FLAG = 2
IN_GAME = 3
