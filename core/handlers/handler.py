# -*- coding: utf-8 -*-
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import MessageHandler, CommandHandler, CallbackQueryHandler, Filters, BaseFilter

from core.adv.controller import send_adv
from core.handlers.decorators import save_chanel_decorator, save_download_decorator
from core.handlers.finder import parse_result, normalize_download_url
from core.handlers.messages import Messages
from core.paging.page import Page

messages = Messages()

BOTONARIOUM = '::Ботонариум::'


# def _build_botonarioum_keyboard(bot, update):
#     area = Area.get(Area.token == bot.area.token)
#     if (area.language in ('RU')):
#         buttons = [[BOTONARIOUM]]
#         keyboard = ReplyKeyboardMarkup(buttons, resize_keyboard=True)
#         bot.send_message(update.message.chat.id, messages.get_massage('i_find'), reply_markup=keyboard)


def build_download_keyboard(songs_data):
    download_buttons = []
    for title, url in songs_data:
        inline_download_button = InlineKeyboardButton(title, callback_data=url)
        download_buttons.append([inline_download_button])
    return download_buttons


@save_chanel_decorator
def send_botonarioum_info(bot, update):
    print('ok1')
    message = 'Ботонариум - вселенная, где обитают боты.'
    print('ok2')
    button = [[InlineKeyboardButton('Присоединиться', url='https://t.me/botonarioum')]]
    print('ok3')
    return bot.send_message(update.message.chat.id, message, reply_markup=InlineKeyboardMarkup(button))


class BotonarioumFilter(BaseFilter):
    def filter(self, message):
        return bool(message.text == BOTONARIOUM)


def attach_pager_buttons(buttons, pager):
    limit, offset = pager.limit, pager.offset
    pagination_buttons = [[]]

    if pager.has_next:
        pagination_buttons[0].append(InlineKeyboardButton('>>>', callback_data='pager.next.limit.{}.offset.{}'.format(limit, offset)))

    if pager.has_prev:
        pagination_buttons[0].append(InlineKeyboardButton('<<<', callback_data='pager.prev.limit.{}.offset.{}'.format(limit, offset)))

    return pagination_buttons + buttons + pagination_buttons


@save_chanel_decorator
def search_audio(bot, update):
    limit, offset = 10, 0
    searching(bot, update, limit, offset)
    # messages.set_language(bot.area.language)
    #
    # try:
    #     bot.send_message(update.message.chat.id, messages.get_massage('searching'))
    #
    #     songs_data, songs_count = parse_result(update.message.text, limit, offset)
    #     songs_data = list(filter(None, songs_data))
    #
    #     pager = Page(songs_count, limit, offset)
    #
    #     print(len(songs_data))
    #
    #     songs_buttons = build_download_keyboard(songs_data)
    #
    #     if songs_buttons:
    #         buttons = attach_pager_buttons(songs_buttons, pager)
    #         keyboard = InlineKeyboardMarkup(buttons)
    #         bot.send_message(update.message.chat.id, messages.get_massage('i_find'), reply_markup=keyboard)
    #     else:
    #         bot.send_message(update.message.chat.id, messages.get_massage('i_try'))
    # except Exception as ex:
    #     print(ex)

def searching(bot, update, limit, offset):
    messages.set_language(bot.area.language)

    try:
        bot.send_message(update.message.chat.id, messages.get_massage('searching'))

        songs_data, songs_count = parse_result(update.message.text, limit, offset)
        songs_data = list(filter(None, songs_data))

        pager = Page(songs_count, limit, offset)

        print(len(songs_data))

        songs_buttons = build_download_keyboard(songs_data)

        if songs_buttons:
            buttons = attach_pager_buttons(songs_buttons, pager)
            keyboard = InlineKeyboardMarkup(buttons)
            bot.send_message(update.message.chat.id, messages.get_massage('i_find'), reply_markup=keyboard)
        else:
            bot.send_message(update.message.chat.id, messages.get_massage('i_try'))
    except Exception as ex:
        print(ex)


def next_page(bot, update, *args, **kwargs):
    query = update.callback_query
    print(query)
    limit = query.data.split('.')[3]
    offset = query.data.split('.')[5]
    print(limit)
    print(offset)
    print('next page')
    searching(bot, update, limit, offset)

def prev_page(bot, update, *args, **kwargs):
    print('next page')

@save_chanel_decorator
def send_info(bot, update):
    messages.set_language(bot.area.language)
    message = messages.get_massage('intro')
    # area = Area.get(Area.token == bot.area.token)
    # if (area.language in ('RU')):
    #     buttons = [[BOTONARIOUM]]
    #     keyboard = ReplyKeyboardMarkup(buttons, resize_keyboard=True)
    #     return bot.send_message(update.message.chat.id, message, reply_markup=keyboard)
    return bot.send_message(update.message.chat.id, message)


@save_chanel_decorator
# @save_download_decorator
def download_song(bot, update, *args, **kwargs):
    messages.set_language(bot.area.language)
    query = update.callback_query
    download_url = normalize_download_url(query.data)
    bot.send_audio(query.message.chat_id, download_url)
    # send_adv(bot, query.message.chat_id, messages)


def init_handlers(dispatcher):
    dispatcher.add_handler(CommandHandler('start', send_info))
    dispatcher.add_handler(MessageHandler(BotonarioumFilter(), send_botonarioum_info))
    dispatcher.add_handler(MessageHandler(Filters.text, search_audio))
    dispatcher.add_handler(CallbackQueryHandler(prev_page, True, False, 'pager.prev.*'))
    dispatcher.add_handler(CallbackQueryHandler(next_page, True, False, 'pager.next.*'))
    dispatcher.add_handler(CallbackQueryHandler(download_song, pass_update_queue=True))
    return dispatcher


if __name__ == '__main__':
    pass
