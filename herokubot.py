#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import logging

from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardButton,
                      InlineKeyboardMarkup)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          ConversationHandler, CallbackQueryHandler)

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

IAM_NEW_USER, IAM_OLD_USER = 101, 102

START, SELECTING_ACTION, IAM_SPEAKER, IAM_MANAGER = map(chr, range(4))
SELECTING_TRACK, TRACK_PROGRAMMING, TRACK_MANAGEMENT, TRACK_MARKETING = map(chr, range(4, 8))
START_OVER = 8
END = ConversationHandler.END


def start(update, context):
    is_new_user = True

    if is_new_user:
        buttons = [[
            InlineKeyboardButton('Я первый раз', callback_data=str(IAM_NEW_USER))
        ], [
            InlineKeyboardButton('У меня есть аккаунт', callback_data=str(IAM_OLD_USER))
        ]]
        keyboard = InlineKeyboardMarkup(buttons)
        update.message.reply_text('👋 Hey! Давайте активируем SpeakersTeam — это займет меньше минуты.',
                                  reply_markup=keyboard)
    else:
        pass

    return START


def start2(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")
    
    buttons = [[
        InlineKeyboardButton('Я спикер', callback_data=str(IAM_SPEAKER))
    ], [
        InlineKeyboardButton('Я организатор', callback_data=str(IAM_MANAGER))
    ]]
    keyboard = InlineKeyboardMarkup(buttons)

    if context.user_data.get(START_OVER):
        update.callback_query.answer()
        update.callback_query.edit_message_text('Нужно понять что здесь написать', reply_markup=keyboard)
    else:
        update.message.reply_text('Нужно выбрать кто ты:', reply_markup=keyboard)

    context.user_data[START_OVER] = False

    return SELECTING_ACTION


def select_track(update, context):
    text = 'Пока какой-то текст'
    buttons = [[
        InlineKeyboardButton(text='Программирование', callback_data=str(TRACK_PROGRAMMING)),
        InlineKeyboardButton(text='Менеджмент', callback_data=str(TRACK_MANAGEMENT)),
        InlineKeyboardButton(text='Маркетинг', callback_data=str(TRACK_MARKETING))
    ]]
    keyboard = InlineKeyboardMarkup(buttons)

    update.callback_query.answer()
    update.callback_query.edit_message_text(text='Нужно выбрать кто ты:\nЯ спикер', reply_markup=keyboard)

    context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")

    return SELECTING_TRACK


def stop(update, context):
    update.message.reply_text('Okay, bye.')

    return END

def main():
    TOKEN = os.environ.get('TOKEN')
    NAME = os.environ.get('NAME')
    PORT = os.environ.get('PORT')

    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    add_speaker_conv = ConversationHandler(
        entry_points=[CallbackQueryHandler(select_track, pattern='^' + str(IAM_SPEAKER) + '$')],

        states={

        },

        fallbacks=[CommandHandler('stop', stop)]
    )

    selection_handlers = [
        add_speaker_conv
    ]

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start2', start2)],

        states={
            SELECTING_ACTION: selection_handlers
        },

        fallbacks=[CommandHandler('stop', stop)]
    )

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(conv_handler)

    # Start the webhook
    updater.start_webhook(listen="0.0.0.0",
                          port=int(PORT),
                          url_path=TOKEN)
    updater.bot.setWebhook("https://{}.herokuapp.com/{}".format(NAME, TOKEN))
    updater.idle()


if __name__ == "__main__":
    main()
