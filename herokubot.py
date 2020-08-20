#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import os

from telegram import (InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          ConversationHandler, CallbackQueryHandler)

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


def start(update, context):
    keyboard = [[InlineKeyboardButton('Я спикер', callback_data='SPEAKER')],
                [InlineKeyboardButton('Я организатор', callback_data='MANAGER')]]

    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text('Расскажи о себе', reply_markup=reply_markup)


def button(update, context):
    query = update.callback_query
    query.answer()
    query.edit_message_text(query.data)


def help_command(update, context):
    update.message.reply_text('Help!')


def echo(update, context):
    update.message.reply_text(update.message.text)


def error(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    TOKEN = os.environ.get('TOKEN')
    NAME = os.environ.get('NAME')
    PORT = os.environ.get('PORT')

    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    # Add handlers
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('help', help_command))
    updater.dispatcher.add_handler(CallbackQueryHandler(button))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))
    dp.add_error_handler(error)

    # Start the webhook
    updater.start_webhook(listen="0.0.0.0",
                          port=int(PORT),
                          url_path=TOKEN)
    updater.bot.setWebhook("https://{}.herokuapp.com/{}".format(NAME, TOKEN))
    updater.idle()


if __name__ == "__main__":
    main()
