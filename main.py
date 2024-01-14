from telegram import Update
from telegram.ext import (
    Application, CallbackQueryHandler, CommandHandler, ConversationHandler
)
from constants.vars import TOKEN, CONTINUE_GAME, FINISH_GAME
from src.bot import start, game, end, logger


def main() -> None:
    """
    Run the bot.
    """
    logger.info('Start the bot.')
    application = Application.builder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            CONTINUE_GAME: [
                CallbackQueryHandler(game, pattern='^' + f'{r}{c}' + '$')
                for r in range(3)
                for c in range(3)
            ],
            FINISH_GAME: [
                CallbackQueryHandler(end, pattern='^' + f'{r}{c}' + '$')
                for r in range(3)
                for c in range(3)
            ],
        },
        fallbacks=[CommandHandler('start', start)],
    )

    # Add ConversationHandler to application that will be used for handling updates
    application.add_handler(conv_handler)

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()
