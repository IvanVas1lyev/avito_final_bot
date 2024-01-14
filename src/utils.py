from copy import deepcopy
import random
from telegram import InlineKeyboardButton

from constants.vars import (
    DEFAULT_STATE,
    PLAYER_WIN_FLAG,
    BOT_WIN_FLAG,
    DRAW_FLAG,
    IN_GAME,
    ZERO,
    CROSS,
    FREE_SPACE
)


def get_default_state() -> list[list[str]]:
    """
    Returns a deep copy of the default state of the game.

    Returns:
        list[list[str]]: A copy of the default state of the game.
    """
    return deepcopy(DEFAULT_STATE)


def generate_keyboard(state: list[list[str]]) -> list[list[InlineKeyboardButton]]:
    """
    Generates a keyboard representation of the game state.

    Args:
        state (list[list[str]]): The current state of the game.

    Returns:
        list[list[InlineKeyboardButton]]: The keyboard representation of the game state.
    """
    return [
        [
            InlineKeyboardButton(state[r][c], callback_data=f'{r}{c}')
            for r in range(3)
        ]
        for c in range(3)
    ]


def bot_move(state: list[list[str]]) -> None:
    """
    Makes a random move for the bot player.

    Args:
        state (list[list[str]]): The current state of the game.

    Returns:
        None
    """
    picks = [(i, j) for i in range(3) for j in range(3) if state[i][j] == '.']
    pick = random.choice(picks)
    state[pick[0]][pick[1]] = ZERO


def game_status(state: list[list[str]]) -> bool:
    """
    Checks the status of the game.

    Args:
        state (list[list[str]]): The current state of the game.

    Returns:
        bool: The status of the game. Can be one of the following:
             - PLAYER_WIN_FLAG: Player has won the game.
             - BOT_WIN_FLAG: Bot has won the game.
             - DRAW_FLAG: The game is a draw.
             - IN_GAME: The game is still in progress.
    """
    for i in range(3):
        if state[i][0] == state[i][1] == state[i][2] == CROSS:
            return PLAYER_WIN_FLAG
        if state[0][i] == state[1][i] == state[2][i] == CROSS:
            return PLAYER_WIN_FLAG
        if state[i][0] == state[i][1] == state[i][2] == ZERO:
            return BOT_WIN_FLAG
        if state[0][i] == state[1][i] == state[2][i] == ZERO:
            return BOT_WIN_FLAG

    if state[0][2] == state[1][1] == state[2][0] == CROSS:
        return PLAYER_WIN_FLAG
    if state[0][0] == state[1][1] == state[2][2] == CROSS:
        return PLAYER_WIN_FLAG

    if state[0][2] == state[1][1] == state[2][0] == ZERO:
        return BOT_WIN_FLAG
    if state[0][0] == state[1][1] == state[2][2] == ZERO:
        return BOT_WIN_FLAG

    if all(state[i][j] != '.' for i in range(3) for j in range(3)):
        return DRAW_FLAG

    return IN_GAME


def is_pick_available(user_pick: list[int], state: list[list[str]]) -> bool:
    """
    Checks if the user's pick is available in the current state of the game.

    Args:
        user_pick (list[int]): The coordinates of the user's pick.
        state (list[list[str]]): The current state of the game.

    Returns:
        bool: True if the user's pick is available, False otherwise.
    """
    if state[user_pick[0]][user_pick[1]] == FREE_SPACE:
        return True

    return False
