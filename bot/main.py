import os
import logging
import socket

import requests
from dotenv import load_dotenv
from telegram import ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler

load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')
BOT_URL = os.getenv('BOT_URL')

backend_settings = {
    'protocol': os.getenv('BOT_BACKEND_PROTOCOL'),
    'host': os.getenv('BOT_BACKEND_HOST'),
    'port': os.getenv('BOT_BACKEND_PORT'),

}

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

URLS = {
    'job': '{protocol}://{host}:{port}/api/job'.format(**backend_settings),
    'proxy': '{protocol}://{host}:{port}/api/proxy'.format(**backend_settings),
}
CHOICE, ADD_PROXY, ADD_BEHANCE = range(3)


def start(bot, update):
    reply_keyboard = (['Behance'], ['Proxy'])
    update.message.reply_text(
        '''
        Hi! What would you like to do? Thumb up a project on BEHANCE? Or add a PROXY?
        ''',

        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard,
            resize_keyboard=True,
            one_time_keyboard=True),
    )
    return CHOICE


def choosing(bot, update):
    user_choice = update.message.text
    if user_choice == 'Behance':
        update.message.reply_text(
            '''
            Send me a link to site and an amount of likes you want in format: URL_ADDRESS AMOUNT.
            \n\rFor example: https://behance.net/gallery/72436411/Yelvy-Fashion-Website 10
            ''',
            disable_web_page_preview=True,
        )
        return ADD_BEHANCE
    elif user_choice == 'Proxy':
        update.message.reply_text(
            '''
            Send me a proxy server and a port for adding to database, in format: HOST PORT.
            \n\rFor example: 217.117.63.10 8080
            ''',
            disable_web_page_preview=True,
        )
        return ADD_PROXY
    return CHOICE


def adding_proxy(bot, update):
    user_proxy = update.message.text
    try:
        host, port = user_proxy.split()
        socket.inet_aton(host)
        port = int(port)
        if port < 0 or port > 65535:
            raise ValueError
    except (OSError, ValueError) as e:
        logger.error(e)
        return ConversationHandler.END

    data = {
        'host': host,
        'port': port,
    }
    with requests.post(url=URLS['proxy'], data=data) as response:
        if response.status_code == 201:
            update.message.reply_text(
                '''
                Success. I added a proxy in database.
                \n\rSee you later!
                ''',
            )
        else:
            update.message.reply_text(
                '''
                Failed. I can't add a proxy. Please, try later.
                ''',
            )

    return ConversationHandler.END


def adding_behance(bot, update):
    user_message = update.message.text

    try:
        url, likes = user_message.split(' ')
    except Exception as e:
        logger.error(e)
        return ConversationHandler.END
    else:
        logger.info("User ordered increasing of likes(+{}) for a project {}".format(likes, url))

    update.message.reply_text(
        '''
        I see! I understand your information.
        \n\rI try to increase count of likes(+{likes}) for a project: {url}.
        '''.format(likes=likes, url=url),
    )

    data = {
        'url': url,
        'likes': likes,
        'period': 60
    }
    with requests.post(url=URLS['job'], data=data) as response:
        if response.status_code == 201:
            update.message.reply_text(
                '''
                Success. I run tasks. Wait about one hour and check it.
                \n\rSee you later!
                ''',
            )
        else:
            update.message.reply_text(
                '''
                Failed. I can't run tasks. Please, try later.
                ''',
            )

    return ConversationHandler.END


def cancel(bot, update):
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text(
        'Bye! I hope we can talk again some day.',
    )

    return ConversationHandler.END


def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


def main():
    updater = Updater(BOT_TOKEN)  # Create the EventHandler and pass it your bot's token.
    dp = updater.dispatcher  # Get the dispatcher to register handlers

    conv_handler = ConversationHandler(
        entry_points=[
            CommandHandler('start', start)
        ],
        states={
            CHOICE: [
                MessageHandler(Filters.text, choosing)
            ],
            ADD_BEHANCE: [
                MessageHandler(Filters.text, adding_behance)
            ],
            ADD_PROXY: [
                MessageHandler(Filters.text, adding_proxy)
            ],

        },
        fallbacks=[
            CommandHandler('cancel', cancel)
        ]
    )

    dp.add_handler(conv_handler)
    dp.add_error_handler(error)  # log all errors

    updater.start_polling()  # Start the Bot
    updater.idle()


if __name__ == '__main__':
    main()
