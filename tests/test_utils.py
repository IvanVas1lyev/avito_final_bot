from src.utils import (
    bot_move,
    game_status,
    is_pick_available
)
from constants.vars import (
    PLAYER_WIN_FLAG,
    BOT_WIN_FLAG,
    DRAW_FLAG,
)
from copy import deepcopy


def test_player_win_diagonal():
    state = [['X', 'O', '.'], ['.', 'X', 'O'], ['.', '.', 'X']]

    assert game_status(state) == PLAYER_WIN_FLAG


def test_player_win_horizontal():
    state = [['.', 'O', '.'], ['X', 'X', 'X'], ['.', '.', 'O']]

    assert game_status(state) == PLAYER_WIN_FLAG


def test_player_win_vertical():
    state = [['X', '.', '.'], ['X', 'O', '.'], ['X', 'O', '.']]

    assert game_status(state) == PLAYER_WIN_FLAG


def test_bot_win_diagonal():
    state = [['O', 'X', '.'], ['.', 'O', 'X'], ['X', '.', 'O']]

    assert game_status(state) == BOT_WIN_FLAG


def test_bot_win_horizontal():
    state = [['X', 'X', '.'], ['O', 'O', 'O'], ['.', '.', 'X']]

    assert game_status(state) == BOT_WIN_FLAG


def test_bot_win_vertical():
    state = [['O', '.', '.'], ['O', 'X', '.'], ['O', 'X', 'X']]

    assert game_status(state) == BOT_WIN_FLAG


def test_draw():
    state = [['O', 'X', 'X'], ['X', 'O', 'O'], ['X', 'O', 'X']]

    assert game_status(state) == DRAW_FLAG


def test_available_pick():
    state = [['O', '.', 'X'], ['X', 'O', 'O'], ['X', 'O', 'X']]
    pick = [0, 1]

    assert is_pick_available(pick, state)


def test_not_available_pick():
    state = [['O', '.', 'X'], ['X', 'O', 'O'], ['X', 'O', 'X']]
    pick = [0, 2]

    assert not is_pick_available(pick, state)


def test_bot_move():
    state = [['.', '.', 'X'], ['.', '.', '.'], ['.', '.', '.']]
    start_state = deepcopy(state)

    bot_move(start_state)

    assert state != start_state
