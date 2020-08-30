#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import logging
import constants as const


from telegram import (InlineKeyboardButton, InlineKeyboardMarkup)
from telegram.ext import (Updater, CommandHandler, ConversationHandler, CallbackQueryHandler)

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)


def start(update, context):
    is_new_user = True

    if is_new_user:
        buttons = [[
            InlineKeyboardButton('Я первый раз', callback_data=str(const.IAM_NEW_USER))
        ], [
            InlineKeyboardButton('У меня есть аккаунт', callback_data=str(const.IAM_OLD_USER))
        ]]
        keyboard = InlineKeyboardMarkup(buttons)
        update.message.reply_text('👋 Hey! Давайте активируем SpeakersTeam — это займет меньше минуты.',
                                  reply_markup=keyboard)

        context.user_data[const.SELECT_TRACK_FROM_START] = True
    else:
        pass

    return const.START


def select_track(update, context):
    query = update.callback_query
    btn_code = query.data

    if btn_code in const.TRACK_SIMPLE_SET:
        change_button_type(btn_code, context)

    buttons = [[
        InlineKeyboardButton(text=track_type(const.TRACK_ENGINEERING, context) + 'Engineering ↵',
                             callback_data=str(const.TRACK_ENGINEERING)),
        InlineKeyboardButton(text=track_type(const.TRACK_DS, context) + 'Data Science ↵',
                             callback_data=str(const.TRACK_DS))
    ], [
        InlineKeyboardButton(text=track_type(const.TRACK_MANAGEMENT, context) + 'Management ↵',
                             callback_data=str(const.TRACK_MANAGEMENT)),
        InlineKeyboardButton(text=track_type(const.TRACK_MARKETING, context) + 'Marketing ↵',
                             callback_data=str(const.TRACK_MARKETING))
    ], [
        InlineKeyboardButton(text=button_type(const.TRACK_DESIGN, context) + 'Design & UX',
                             callback_data=str(const.TRACK_DESIGN)),
        InlineKeyboardButton(text=track_type(const.TRACK_QA, context) + 'QA ↵', callback_data=str(const.TRACK_QA))
    ], [
        InlineKeyboardButton(text='Далее »', callback_data=str(const.SELECT_TRACK_NEXT))
    ]]
    keyboard = InlineKeyboardMarkup(buttons)

    if context.user_data[const.SELECT_TRACK_FROM_START]:
        # Hide keyboard
        update.callback_query.answer()
        update.callback_query.edit_message_reply_markup(InlineKeyboardMarkup([]))

        context.bot.send_message(chat_id=update.callback_query.from_user.id,
                                 text='⚙️ Настройки профиля\n\nВыберите специализацию и сферу, в которой вы '
                                      'разбираетесь, расскажите о своем опыте выступлений.')

        context.bot.send_message(chat_id=update.callback_query.from_user.id,
                                 text='👨🏼‍💻 Специализация', reply_markup=keyboard)
    else:
        update.callback_query.answer()
        update.callback_query.edit_message_text(text='👨🏼‍💻 Специализация', reply_markup=keyboard)

    context.user_data[const.SELECT_TRACK_FROM_START] = False

    return const.SELECTING_TRACK_ACTION


def button_type(btn_code, context):
    if btn_code in context.user_data:
        if context.user_data[btn_code] is True:
            return '▣ '
    return '☐ '


def change_button_type(btn_code, context):
    if btn_code not in context.user_data:
        context.user_data[btn_code] = False
    context.user_data[btn_code] = not context.user_data[btn_code]


def track_type(t_type, context):
    if check_track_for_selected(t_type, context):
        return '▣ '
    return '☐ '


def check_track_for_selected(t_type, context):
    if t_type == const.TRACK_ENGINEERING:
        for val in const.TRACK_ENGINEERING_SET:
            if val in context.user_data:
                if context.user_data[val] is True:
                    return True
    elif t_type == const.TRACK_DS:
        for val in const.TRACK_DS_SET:
            if val in context.user_data:
                if context.user_data[val] is True:
                    return True
    elif t_type == const.TRACK_MANAGEMENT:
        for val in const.TRACK_MANAGEMENT_SET:
            if val in context.user_data:
                if context.user_data[val] is True:
                    return True
    elif t_type == const.TRACK_DESIGN:
        for val in const.TRACK_SIMPLE_SET:
            if val in context.user_data:
                if context.user_data[val] is True:
                    return True
    elif t_type == const.TRACK_MARKETING:
        for val in const.TRACK_MARKETING_SET:
            if val in context.user_data:
                if context.user_data[val] is True:
                    return True
    elif t_type == const.TRACK_QA:
        for val in const.TRACK_QA_SET:
            if val in context.user_data:
                if context.user_data[val] is True:
                    return True
    return False


def is_track_selected(context):
    if check_track_for_selected(const.TRACK_ENGINEERING, context) or \
            check_track_for_selected(const.TRACK_DS, context) or \
            check_track_for_selected(const.TRACK_MANAGEMENT, context) or \
            check_track_for_selected(const.TRACK_DESIGN, context) or \
            check_track_for_selected(const.TRACK_MARKETING, context) or \
            check_track_for_selected(const.TRACK_QA, context):
        return True
    return False


def select_track_engineering(update, context):
    query = update.callback_query
    btn_code = query.data

    if btn_code in const.TRACK_ENGINEERING_SET:
        change_button_type(btn_code, context)

    buttons = [[
        InlineKeyboardButton(text=button_type(const.ENGIN_JAVA, context) + 'Java / Scala',
                             callback_data=str(const.ENGIN_JAVA)),
        InlineKeyboardButton(text=button_type(const.ENGIN_PY, context) + 'Python',
                             callback_data=str(const.ENGIN_PY)),
        InlineKeyboardButton(text=button_type(const.ENGIN_CSH, context) + 'С#',
                             callback_data=str(const.ENGIN_CSH))
    ], [
        InlineKeyboardButton(text=button_type(const.ENGIN_IOS, context) + 'iOS',
                             callback_data=str(const.ENGIN_IOS)),
        InlineKeyboardButton(text=button_type(const.ENGIN_ANDROID, context) + 'Android',
                             callback_data=str(const.ENGIN_ANDROID)),
        InlineKeyboardButton(text=button_type(const.ENGIN_CPP, context) + 'C/C++',
                             callback_data=str(const.ENGIN_CPP))
    ], [
        InlineKeyboardButton(text=button_type(const.ENGIN_GO, context) + 'Go',
                             callback_data=str(const.ENGIN_GO)),
        InlineKeyboardButton(text=button_type(const.ENGIN_RUBY, context) + 'Ruby',
                             callback_data=str(const.ENGIN_RUBY)),
        InlineKeyboardButton(text=button_type(const.ENGIN_PHP, context) + 'PHP',
                             callback_data=str(const.ENGIN_PHP))
    ], [
        InlineKeyboardButton(text=button_type(const.ENGIN_JS_FRONT, context) + 'JS / Front-end',
                             callback_data=str(const.ENGIN_JS_FRONT)),
        InlineKeyboardButton(text=button_type(const.ENGIN_JS_BACK, context) + 'JS / Back-end',
                             callback_data=str(const.ENGIN_JS_BACK)),
        InlineKeyboardButton(text=button_type(const.ENGIN_DEVOPS, context) + 'DevOps',
                             callback_data=str(const.ENGIN_DEVOPS))
    ], [
        InlineKeyboardButton(text='« Назад', callback_data=str(const.RETURN_TO_SELECT_TRACK)),
        InlineKeyboardButton(text='Далее »', callback_data=str(const.SELECT_TRACK_NEXT))
    ]]
    keyboard = InlineKeyboardMarkup(buttons)

    update.callback_query.answer()
    update.callback_query.edit_message_text(text='👨🏼‍💻 Engineering', reply_markup=keyboard)

    return const.SELECTING_ENGINEERING


def select_track_data_science(update, context):
    query = update.callback_query
    btn_code = query.data

    if btn_code in const.TRACK_DS_SET:
        change_button_type(btn_code, context)

    buttons = [[
        InlineKeyboardButton(text=button_type(const.DS_ANALYST, context) + 'Data Analyst',
                             callback_data=str(const.DS_ANALYST)),
        InlineKeyboardButton(text=button_type(const.DS_ENGINEER, context) + 'Data Engineer',
                             callback_data=str(const.DS_ENGINEER)),
        InlineKeyboardButton(text=button_type(const.DS_SIMP_ANALYST, context) + 'Analyst',
                             callback_data=str(const.DS_SIMP_ANALYST))
    ], [
        InlineKeyboardButton(text=button_type(const.DS_ML_ENGINEER, context) + 'ML Engineer',
                             callback_data=str(const.DS_ML_ENGINEER)),
        InlineKeyboardButton(text=button_type(const.DS_ML_RESEARCHER, context) + 'ML Researcher',
                             callback_data=str(const.DS_ML_RESEARCHER))
    ], [
        InlineKeyboardButton(text='« Назад', callback_data=str(const.RETURN_TO_SELECT_TRACK)),
        InlineKeyboardButton(text='Далее »', callback_data=str(const.SELECT_TRACK_NEXT))
    ]]
    keyboard = InlineKeyboardMarkup(buttons)

    update.callback_query.answer()
    update.callback_query.edit_message_text(text='👨🏼‍💻 Data Science', reply_markup=keyboard)

    return const.SELECTING_DATA_SCIENCE


def select_track_management(update, context):
    query = update.callback_query
    btn_code = query.data

    if btn_code in const.TRACK_MANAGEMENT_SET:
        change_button_type(btn_code, context)

    buttons = [[
        InlineKeyboardButton(text=button_type(const.MANAGEMENT_PRODUCT, context) + 'Product management',
                             callback_data=str(const.MANAGEMENT_PRODUCT)),
        InlineKeyboardButton(text=button_type(const.MANAGEMENT_PROJECT, context) + 'Project management',
                             callback_data=str(const.MANAGEMENT_PROJECT))
    ], [
        InlineKeyboardButton(text=button_type(const.MANAGEMENT_TECH, context) + 'Tech management',
                             callback_data=str(const.MANAGEMENT_TECH)),
        InlineKeyboardButton(text=button_type(const.MANAGEMENT_AGILE, context) + 'Agile',
                             callback_data=str(const.MANAGEMENT_AGILE)),
        InlineKeyboardButton(text=button_type(const.MANAGEMENT_HR, context) + 'HR',
                             callback_data=str(const.MANAGEMENT_HR))
    ], [
        InlineKeyboardButton(text='« Назад', callback_data=str(const.RETURN_TO_SELECT_TRACK)),
        InlineKeyboardButton(text='Далее »', callback_data=str(const.SELECT_TRACK_NEXT))
    ]]
    keyboard = InlineKeyboardMarkup(buttons)

    update.callback_query.answer()
    update.callback_query.edit_message_text(text='👨🏼‍💻 Management', reply_markup=keyboard)

    return const.SELECTING_MANAGEMENT


def select_track_marketing(update, context):
    query = update.callback_query
    btn_code = query.data

    if btn_code in const.TRACK_MARKETING_SET:
        change_button_type(btn_code, context)

    buttons = [[
        InlineKeyboardButton(text=button_type(const.MARKETING_INTERNET, context) + 'Internet marketing',
                             callback_data=str(const.MARKETING_INTERNET)),
        InlineKeyboardButton(text=button_type(const.MARKETING_EVENT, context) + 'Event marketing',
                             callback_data=str(const.MARKETING_EVENT))
    ], [
        InlineKeyboardButton(text=button_type(const.MARKETING_PR, context) + 'PR',
                             callback_data=str(const.MARKETING_PR)),
        InlineKeyboardButton(text=button_type(const.MARKETING_BRANDING, context) + 'Branding',
                             callback_data=str(const.MARKETING_BRANDING))
    ], [
        InlineKeyboardButton(text=button_type(const.MARKETING_COMMUNITY, context) + 'Community marketing',
                             callback_data=str(const.MARKETING_COMMUNITY)),
        InlineKeyboardButton(text=button_type(const.MARKETING_SMM, context) + 'SMM',
                             callback_data=str(const.MARKETING_SMM))
    ], [
        InlineKeyboardButton(text=button_type(const.MARKETING_CONTENT, context) + 'Content marketing',
                             callback_data=str(const.MARKETING_CONTENT)),
        InlineKeyboardButton(text=button_type(const.MARKETING_ADV, context) + 'Advertising',
                             callback_data=str(const.MARKETING_ADV))
    ], [
        InlineKeyboardButton(text='« Назад', callback_data=str(const.RETURN_TO_SELECT_TRACK)),
        InlineKeyboardButton(text='Далее »', callback_data=str(const.SELECT_TRACK_NEXT))
    ]]
    keyboard = InlineKeyboardMarkup(buttons)

    update.callback_query.answer()
    update.callback_query.edit_message_text(text='👨🏼‍💻 Marketing', reply_markup=keyboard)

    return const.SELECTING_MARKETING


def select_track_qa(update, context):
    query = update.callback_query
    btn_code = query.data

    if btn_code in const.TRACK_QA_SET:
        change_button_type(btn_code, context)

    buttons = [[
        InlineKeyboardButton(text=button_type(const.QA_AUTO, context) + 'QA / Auto',
                             callback_data=str(const.QA_AUTO)),
        InlineKeyboardButton(text=button_type(const.QA_MANUAL, context) + 'QA / Manual',
                             callback_data=str(const.QA_MANUAL))
    ], [
        InlineKeyboardButton(text='« Назад', callback_data=str(const.RETURN_TO_SELECT_TRACK)),
        InlineKeyboardButton(text='Далее »', callback_data=str(const.SELECT_TRACK_NEXT))
    ]]
    keyboard = InlineKeyboardMarkup(buttons)

    update.callback_query.answer()
    update.callback_query.edit_message_text(text='👨🏼‍💻 QA', reply_markup=keyboard)

    return const.SELECTING_QA


def check_selected_track(update, context):
    if not is_track_selected(context):
        update.callback_query.answer(text='Пожалуйста, выберите хотя бы одну сферу')
        return

    update.callback_query.answer(text='Продолжение скоро будет')
    

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
                                           pattern='^' + str(const.IAM_NEW_USER) + '$')],
        states={
            const.SELECTING_TRACK_ACTION: [
                CallbackQueryHandler(select_track_engineering, pattern='^' + str(const.TRACK_ENGINEERING) + '$'),
                CallbackQueryHandler(select_track_data_science, pattern='^' + str(const.TRACK_DS) + '$'),
                CallbackQueryHandler(select_track_management, pattern='^' + str(const.TRACK_MANAGEMENT) + '$'),
                CallbackQueryHandler(select_track_marketing, pattern='^' + str(const.TRACK_MARKETING) + '$'),
                CallbackQueryHandler(select_track_qa, pattern='^' + str(const.TRACK_QA) + '$'),

                CallbackQueryHandler(check_selected_track, pattern='^' + str(const.SELECT_TRACK_NEXT) + '$'),
                CallbackQueryHandler(select_track)
            ],
            const.SELECTING_ENGINEERING: [
                CallbackQueryHandler(select_track, pattern='^' + str(const.RETURN_TO_SELECT_TRACK) + '$'),
                CallbackQueryHandler(check_selected_track, pattern='^' + str(const.SELECT_TRACK_NEXT) + '$'),
                CallbackQueryHandler(select_track_engineering)
            ],
            const.SELECTING_DATA_SCIENCE: [
                CallbackQueryHandler(select_track, pattern='^' + str(const.RETURN_TO_SELECT_TRACK) + '$'),
                CallbackQueryHandler(check_selected_track, pattern='^' + str(const.SELECT_TRACK_NEXT) + '$'),
                CallbackQueryHandler(select_track_data_science)
            ],
            const.SELECTING_MANAGEMENT: [
                CallbackQueryHandler(select_track, pattern='^' + str(const.RETURN_TO_SELECT_TRACK) + '$'),
                CallbackQueryHandler(check_selected_track, pattern='^' + str(const.SELECT_TRACK_NEXT) + '$'),
                CallbackQueryHandler(select_track_management)
            ],
            const.SELECTING_MARKETING: [
                CallbackQueryHandler(select_track, pattern='^' + str(const.RETURN_TO_SELECT_TRACK) + '$'),
                CallbackQueryHandler(check_selected_track, pattern='^' + str(const.SELECT_TRACK_NEXT) + '$'),
                CallbackQueryHandler(select_track_marketing)
            ],
            const.SELECTING_QA: [
                CallbackQueryHandler(select_track, pattern='^' + str(const.RETURN_TO_SELECT_TRACK) + '$'),
                CallbackQueryHandler(check_selected_track, pattern='^' + str(const.SELECT_TRACK_NEXT) + '$'),
                CallbackQueryHandler(select_track_qa)
            ]
        },
        fallbacks={
            CallbackQueryHandler('stop', stop)
        },
        allow_reentry=True
    )

    selection_handlers = [
        add_new_user_conv
    ]

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            const.START: selection_handlers
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
