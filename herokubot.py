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

(
    # Actions
    START, SELECTING_TRACK_ACTION, SELECTING_ENGINEERING, SELECTING_DATA_SCIENCE,

    # Different users
    IAM_NEW_USER, IAM_OLD_USER,

    # Different tracks
    TRACK_ENGINEERING, TRACK_DATA_SCIENCE, TRACK_MANAGEMENT, TRACK_HR, TRACK_MARKETING,
    TRACK_DESIGN, TRACK_QA, TRACK_DEVOPS, SELECT_TRACK_NEXT, RETURN_TO_SELECT_TRACK,

    # Track Engineering
    ENGIN_JAVA, ENGIN_PY, ENGIN_CSH, ENGIN_IOS, ENGIN_ANDROID, ENGIN_CPP, ENGIN_GO,
    ENGIN_RUBY, ENGIN_PHP, ENGIN_JS_FRONT, ENGIN_JS_BACK,

    # Track Data Science
    DATA_ANALYST, DATA_ENGINEER, DATA_SIMP_ANALYST, DATA_ML_ENGINEER, DATA_ML_RESEARCHER,

    SELECT_TRACK_FROM_START) = map(chr, range(33))


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
        InlineKeyboardButton(text='☐ Engineering ↵', callback_data=str(TRACK_ENGINEERING)),
        InlineKeyboardButton(text='☐ Data Science ↵', callback_data=str(TRACK_DATA_SCIENCE))
    ], [
        InlineKeyboardButton(text='☐ Management ↵', callback_data=str(TRACK_MANAGEMENT)),
        InlineKeyboardButton(text='☐ Tech HR', callback_data=str(TRACK_HR))
    ], [
        InlineKeyboardButton(text='☐ Marketing ↵', callback_data=str(TRACK_MARKETING)),
        InlineKeyboardButton(text='☐ Design & UX', callback_data=str(TRACK_DESIGN))
    ], [
        InlineKeyboardButton(text='☐ QA ↵', callback_data=str(TRACK_QA)),
        InlineKeyboardButton(text='☐ DevOps', callback_data=str(TRACK_DEVOPS))
    ], [
        InlineKeyboardButton(text='Далее »', callback_data=str(SELECT_TRACK_NEXT))
    ]]
    keyboard = InlineKeyboardMarkup(buttons)

    if context.user_data[SELECT_TRACK_FROM_START]:
        # Hide keyboard
        update.callback_query.answer()
        update.callback_query.edit_message_reply_markup(InlineKeyboardMarkup([]))

        context.bot.send_message(chat_id=update.callback_query.from_user.id,
                                 text='⚙️ Настройки профиля\n\nВыберите сферу, зарплату и локацию.')

        context.bot.send_message(chat_id=update.callback_query.from_user.id,
                                 text='👨🏼‍💻 Сфера', reply_markup=keyboard)
    else:
        update.callback_query.answer()
        update.callback_query.edit_message_text(text='👨🏼‍💻 Сфера', reply_markup=keyboard)

    context.user_data[SELECT_TRACK_FROM_START] = False

    return SELECTING_TRACK_ACTION


def button_type(btn_code, context):
    if btn_code in context.user_data:
        if context.user_data[btn_code] is True:
            return '▣ '
    return '☐ '


def select_track_engineering(update, context):
    buttons = [[
        InlineKeyboardButton(text=button_type(ENGIN_JAVA, context) + 'Java / Scala', callback_data=str(ENGIN_JAVA)),
        InlineKeyboardButton(text='☐ Python', callback_data=str(ENGIN_PY)),
        InlineKeyboardButton(text='☐ С#', callback_data=str(ENGIN_CSH))
    ], [
        InlineKeyboardButton(text='☐ iOS', callback_data=str(ENGIN_IOS)),
        InlineKeyboardButton(text='☐ Android', callback_data=str(ENGIN_ANDROID)),
        InlineKeyboardButton(text='☐ C/C++', callback_data=str(ENGIN_CPP))
    ], [
        InlineKeyboardButton(text='☐ Go', callback_data=str(ENGIN_GO)),
        InlineKeyboardButton(text='☐ Ruby', callback_data=str(ENGIN_RUBY)),
        InlineKeyboardButton(text='☐ PHP', callback_data=str(ENGIN_PHP))
    ], [
        InlineKeyboardButton(text='☐ JS / Front-end', callback_data=str(ENGIN_JS_FRONT)),
        InlineKeyboardButton(text='☐ JS / Back-end', callback_data=str(ENGIN_JS_BACK))
    ], [
        InlineKeyboardButton(text='« Назад', callback_data=str(RETURN_TO_SELECT_TRACK)),
        InlineKeyboardButton(text='Далее »', callback_data=str(SELECT_TRACK_NEXT))
    ]]
    keyboard = InlineKeyboardMarkup(buttons)

    update.callback_query.answer()
    update.callback_query.edit_message_text(text='👨🏼‍💻 Сфера → Engineering', reply_markup=keyboard)

    return SELECTING_ENGINEERING


def click_btn_track_engineering(update, context):
    query = update.callback_query
    logger.warning("Selected option: {}".format(query.data))


def select_track_data_science(update, context):
    buttons = [[
        InlineKeyboardButton(text='☐ Data Analyst', callback_data=str(DATA_ANALYST)),
        InlineKeyboardButton(text='☐ Data Engineer', callback_data=str(DATA_ENGINEER)),
        InlineKeyboardButton(text='☐ Analyst', callback_data=str(DATA_SIMP_ANALYST))
    ], [
        InlineKeyboardButton(text='☐ ML Engineer', callback_data=str(DATA_ML_ENGINEER)),
        InlineKeyboardButton(text='☐ ML Researcher', callback_data=str(DATA_ML_RESEARCHER))
    ], [
        InlineKeyboardButton(text='« Назад', callback_data=str(RETURN_TO_SELECT_TRACK)),
        InlineKeyboardButton(text='Далее »', callback_data=str(SELECT_TRACK_NEXT))
    ]]
    keyboard = InlineKeyboardMarkup(buttons)

    update.callback_query.answer()
    update.callback_query.edit_message_text(text='👨🏼‍💻 Сфера → Data Science', reply_markup=keyboard)


def check_selected_track(update, context):
    update.callback_query.answer(text='Пожалуйста, выберите сферу')


def stop(update, context):
    update.message.reply_text('Okay, bye.')

    return ConversationHandler.END


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
            SELECTING_TRACK_ACTION: [
                CallbackQueryHandler(select_track_engineering, pattern='^' + str(TRACK_ENGINEERING) + '$'),
                CallbackQueryHandler(select_track_data_science, pattern='^' + str(TRACK_DATA_SCIENCE) + '$'),

                CallbackQueryHandler(select_track, pattern='^' + str(RETURN_TO_SELECT_TRACK) + '$'),
                CallbackQueryHandler(check_selected_track, pattern='^' + str(SELECT_TRACK_NEXT) + '$')
            ],
            SELECTING_ENGINEERING: [
                CallbackQueryHandler(click_btn_track_engineering)
            ],
            SELECTING_DATA_SCIENCE: []

        },

        fallbacks=[
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

    updater.start_webhook(listen="0.0.0.0", port=int(PORT), url_path=TOKEN)
    updater.bot.setWebhook("https://{}.herokuapp.com/{}".format(NAME, TOKEN))
    updater.idle()


if __name__ == "__main__":
    main()
