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

START, SELECTING_TRACK_ACTION, IAM_SPEAKER, IAM_MANAGER, HIDE_KEYBOARD = map(chr, range(5))
SELECTING_TRACK, TRACK_PROGRAMMING, TRACK_MANAGEMENT, TRACK_MARKETING = map(chr, range(5, 9))
START_OVER = 9
GO_TO_SELECT_TRACK = 10
SELECT_TRACK_FROM_START = 11
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

        context.user_data[SELECT_TRACK_FROM_START] = True
    else:
        pass

    return START


def select_track(update, context):

    buttons = [[
        InlineKeyboardButton(text='☐ Engineering ↵', callback_data=str(TRACK_PROGRAMMING)),
        InlineKeyboardButton(text='☐ Data Science ↵', callback_data=str(1))
    ], [
        InlineKeyboardButton(text='☐ Management ↵', callback_data=str(TRACK_MANAGEMENT)),
        InlineKeyboardButton(text='☐ Tech Recruitment', callback_data=str(TRACK_MARKETING))
    ], [
        InlineKeyboardButton(text='☐ Marketing ↵', callback_data=str(TRACK_MANAGEMENT)),
        InlineKeyboardButton(text='▣ Design & UX', callback_data=str(TRACK_MANAGEMENT))
    ], [
        InlineKeyboardButton(text='☐ QA ↵', callback_data=str(TRACK_MARKETING)),
        InlineKeyboardButton(text='☐ DevOps', callback_data=str(TRACK_MARKETING))
    ], [
        InlineKeyboardButton(text='Далее ▶', callback_data=str(123))
    ]]
    keyboard = InlineKeyboardMarkup(buttons)

    if context.user_data[SELECT_TRACK_FROM_START]:
        # Hide keyboard
        update.callback_query.answer()
        update.callback_query.edit_message_reply_markup(InlineKeyboardMarkup([]))

        # Send general message
        context.bot.send_message(chat_id=update.callback_query.from_user.id,
                                 text='⚙️ Настройки профиля\n\nВыберите сферу, зарплату и локацию.')

        context.bot.send_message(chat_id=update.callback_query.from_user.id,
                                 text='👨🏼‍💻 Сфера',
                                 reply_markup=keyboard)
    else:
        update.callback_query.answer()
        update.callback_query.edit_message_text(text='👨🏼‍💻 Сфера',
                                                reply_markup=keyboard)

    return SELECTING_TRACK_ACTION


def select_track_programming(update, context):
    # Send question about track
    buttons = [[
        InlineKeyboardButton(text='☐ Java / Scala', callback_data=str(TRACK_PROGRAMMING)),
        InlineKeyboardButton(text='☐ Python', callback_data=str(TRACK_MANAGEMENT)),
        InlineKeyboardButton(text='☐ С#', callback_data=str(TRACK_MARKETING))
    ], [
        InlineKeyboardButton(text='☐ iOS', callback_data=str(TRACK_PROGRAMMING)),
        InlineKeyboardButton(text='☐ Android', callback_data=str(TRACK_MANAGEMENT)),
        InlineKeyboardButton(text='☐ C/C++', callback_data=str(TRACK_MARKETING))
    ], [
        InlineKeyboardButton(text='☐ Go', callback_data=str(TRACK_PROGRAMMING)),
        InlineKeyboardButton(text='☐ Ruby', callback_data=str(TRACK_MANAGEMENT)),
        InlineKeyboardButton(text='☐ PHP', callback_data=str(TRACK_MARKETING))
    ], [
        InlineKeyboardButton(text='☐ JS/Front-end', callback_data=str(TRACK_PROGRAMMING)),
        InlineKeyboardButton(text='☐ JS/Back-end', callback_data=str(TRACK_MANAGEMENT))
    ], [
        InlineKeyboardButton(text='◀ Назад', callback_data=str(GO_TO_SELECT_TRACK)),
        InlineKeyboardButton(text='Далее ▶', callback_data=str(123))
    ]]
    keyboard = InlineKeyboardMarkup(buttons)

    update.callback_query.answer()
    update.callback_query.edit_message_text(text='👨🏼‍💻 Сфера', reply_markup=keyboard)

    context.user_data[SELECT_TRACK_FROM_START] = False

    return 1001


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
        entry_points=[CallbackQueryHandler(select_track,
                                           pattern='^' + str(IAM_NEW_USER) + '$')],
        states={
            SELECTING_TRACK_ACTION: [CallbackQueryHandler(select_track_programming,
                                                          pattern='^' + str(TRACK_PROGRAMMING) + '$')]
        },

        fallbacks=[
            CallbackQueryHandler(select_track, pattern='^' + str(GO_TO_SELECT_TRACK) + '$'),
            CommandHandler('stop', stop)
        ],

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
