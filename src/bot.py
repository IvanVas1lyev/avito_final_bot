import logging
from constants.vars import (
    CONTINUE_GAME,
    FINISH_GAME,
    CROSS,
    IN_GAME
)
from constants.msgs import (
    YOUR_TURN_MSG,
    MSGS_DICT,
    RESTART_MSG,
    NOT_AVAILABLE_MSG
)
from src.utils import (
    get_default_state,
    generate_keyboard,
    bot_move,
    game_status,
    is_pick_available
)
from telegram import InlineKeyboardMarkup, Update
from telegram.ext import (
    ContextTypes,
    ConversationHandler,
)


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Start the game and initialize the state and keyboard for the user.

    Args:
        update (telegram.Update): The update object for the incoming message.
        context (telegram.ext.Context): The context object for handling the conversation flow.

    Returns:
        int: The next state in the conversation flow.
    """
    context.user_data["keyboard_state"] = get_default_state()
    keyboard = generate_keyboard(context.user_data["keyboard_state"])
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(YOUR_TURN_MSG, reply_markup=reply_markup)

    return CONTINUE_GAME


async def game(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Handle the user's move and bot's move in the game.

    Args:
        update (telegram.Update): The update object for the incoming callback query.
        context (telegram.ext.Context): The context object for handling the conversation flow.

    Returns:
        int: The next state in the conversation flow.
    """
    user_pick = [
        int(update.callback_query.data[0]),
        int(update.callback_query.data[1])
    ]
    state = context.user_data["keyboard_state"]

    if not is_pick_available(user_pick, state):
        keyboard = generate_keyboard(state)
        reply_markup = InlineKeyboardMarkup(keyboard)
        logger.info(f"Player's move is not available : {user_pick}")

        await update.callback_query.edit_message_text(
            NOT_AVAILABLE_MSG, reply_markup=reply_markup
        )

        return CONTINUE_GAME

    state[user_pick[0]][user_pick[1]] = CROSS
    logger.info(f"Player's move : {state}")
    status = game_status(state)

    if status != IN_GAME:
        logger.info(status)
        keyboard = generate_keyboard(state)
        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.callback_query.edit_message_text(
            MSGS_DICT[status] + RESTART_MSG, reply_markup=reply_markup
        )

        return FINISH_GAME

    bot_move(state)
    logger.info(f"Bot's move: {state}")
    status = game_status(state)

    if status != IN_GAME:
        logger.info(status)
        keyboard = generate_keyboard(state)
        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.callback_query.edit_message_text(
            MSGS_DICT[status] + RESTART_MSG, reply_markup=reply_markup
        )

        return FINISH_GAME

    keyboard = generate_keyboard(state)
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.callback_query.edit_message_text(
        YOUR_TURN_MSG, reply_markup=reply_markup
    )

    return CONTINUE_GAME


async def end(context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    End the game and reset the state.

    Args:
        context (telegram.ext.Context): The context object for handling the conversation flow.

    Returns:
        int: The next state in the conversation flow.
    """
    context.user_data['keyboard_state'] = get_default_state()
    return ConversationHandler.END
