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

START, SELECTING_ACTION, IAM_SPEAKER, IAM_MANAGER, HIDE_KEYBOARD = map(chr, range(5))
SELECTING_TRACK, TRACK_PROGRAMMING, TRACK_MANAGEMENT, TRACK_MARKETING = map(chr, range(5, 9))
START_OVER = 9
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


def start_hide_keyboard(update, context):
    # Hide keyboard
    update.callback_query.answer()
    update.callback_query.edit_message_reply_markup(InlineKeyboardMarkup([]))

    # Send general message
    context.bot.send_message(chat_id=update.callback_query.from_user.id,
                             text='⚙️ Настройки профиля\n\nВыберите сферу, зарплату и локацию.')

    # Send question about track
    buttons = [[
        InlineKeyboardButton(text='◻ Программирование ↵', callback_data=str(TRACK_PROGRAMMING)),
        InlineKeyboardButton(text='◻ Менеджмент ↵', callback_data=str(TRACK_MANAGEMENT)),
        InlineKeyboardButton(text='◻ Маркетинг ↵', callback_data=str(TRACK_MARKETING))
    ]]
    keyboard = InlineKeyboardMarkup(buttons)

    context.bot.send_message(chat_id=update.callback_query.from_user.id,
                             text='👨🏼‍💻 Сфера',
                             reply_markup=keyboard)

    return HIDE_KEYBOARD


def select_track(update, context):
    update.callback_query.answer()
    update.callback_query.edit_message_text('asdasdas')

    context.bot.send_message(chat_id=update.callback_query.from_user.id,
                             text='Настройки профиля\n\nВыберите сферу, зарплату и локацию.')
    context.bot.send_message(chat_id=update.callback_query.from_user.id, text='Сфера')

    buttons = [[
        InlineKeyboardButton(text='Программирование', callback_data=str(TRACK_PROGRAMMING)),
        InlineKeyboardButton(text='Менеджмент', callback_data=str(TRACK_MANAGEMENT)),
        InlineKeyboardButton(text='Маркетинг', callback_data=str(TRACK_MARKETING))
    ]]
    keyboard = InlineKeyboardMarkup(buttons)

    update.callback_query.answer()
    update.callback_query.edit_message_text(text='Сфера', reply_markup=keyboard)

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

    add_new_user_conv = ConversationHandler(
        # entry_points=[CallbackQueryHandler(select_track, pattern='^' + str(IAM_NEW_USER) + '$')],
        entry_points=[CallbackQueryHandler(start_hide_keyboard)],
        states={
            HIDE_KEYBOARD: [CallbackQueryHandler(select_track)]
        },

        fallbacks=[CommandHandler('stop', stop)],

        allow_reentry=True
    )

    selection_handlers = [
        add_new_user_conv
    ]

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            START: selection_handlers
        },

        fallbacks=[CommandHandler('stop', stop)],

        allow_reentry=True
    )

    dp.add_handler(conv_handler)

    # Start the webhook
    updater.start_webhook(listen="0.0.0.0",
                          port=int(PORT),
                          url_path=TOKEN)
    updater.bot.setWebhook("https://{}.herokuapp.com/{}".format(NAME, TOKEN))
    updater.idle()


if __name__ == "__main__":
    main()
