import telegram
from dotenv import load_dotenv
import os
import time
from telegram import InlineQueryResultArticle, InputTextMessageContent, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
from telegram.ext import MessageHandler, Filters, InlineQueryHandler
from django.core.management.base import BaseCommand


# функция обработки команды '/start'
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, 
                             text="Здравствуйте. Это официальный бот по поддержке участников")
    time.sleep(4)
    return main_keyboard(update, context)

# функция отрисовки начальной клавиатуры
def main_keyboard(update, context):
    keyboard = [
        [InlineKeyboardButton('Программа', callback_data='Start_1'),
         InlineKeyboardButton('Задать вопрос спикеру', callback_data='Start_2')]
    ]
    context.bot.send_message(update.effective_chat.id, 'Это основное меню мероприятия', reply_markup=InlineKeyboardMarkup(keyboard))

# функция отрисовки меню 'Программа'
def program_keyboard(update, context):
    keyboard = [
        [InlineKeyboardButton('Вступительные мероприятия', callback_data='Program_1')],
        [InlineKeyboardButton('Поток "Эверест"', callback_data='Program_2'),
         InlineKeyboardButton('Поток "Альпы"', callback_data='Program_3')],
        [InlineKeyboardButton('Заключительные мероприятия', callback_data='Program_4')],
        [InlineKeyboardButton('Главное меню', callback_data='Program_5')]
    ]
    context.bot.send_message(update.effective_chat.id, 'Вот программа мероприятия', reply_markup=InlineKeyboardMarkup(keyboard))

# функция отрисовки меню 'Вступительные мероприятия'
def entry_keyboard(update, context):
    keyboard = [
        [InlineKeyboardButton('09:00 Регистрация', callback_data='Entry_1')],
        [InlineKeyboardButton('10:00 Дискуссия – пути развития рынка разработки', callback_data='Entry_2'),
         InlineKeyboardButton('11:30 Нетворкинг', callback_data='Entry_3')],
        [InlineKeyboardButton('Назад', callback_data='Entry_4')],
        ]
    context.bot.send_message(update.effective_chat.id, 'Это будет во вступительной части', reply_markup=InlineKeyboardMarkup(keyboard))

# функция отрисовки меню Поток "Эверест"
def everest_keyboard(update, context):
    keyboard = [
        [InlineKeyboardButton('12:00 Блок «Коммуникационные инновации» ', callback_data='Everest_1')],
        [InlineKeyboardButton('13:30 Обед', callback_data='Everest_2')],
        [InlineKeyboardButton('14:00 Блок «Построение предективной аналитики» ', callback_data='Everest_3')],
        [InlineKeyboardButton('14:50  Блок  «Автоматизация рекламных коммуникаций»', callback_data='Everest_4')],
        [InlineKeyboardButton('15:40  Блок  «Системы управления коммуникациями компании с клиентами»', callback_data='Everest_5')],
        [InlineKeyboardButton('Назад', callback_data='Everest_6')]
        ]
    context.bot.send_message(update.effective_chat.id, 'Программа потока "Эверест"', reply_markup=InlineKeyboardMarkup(keyboard))

# функция отрисовки меню Поток "Альпы"
def alps_keyboard(update, context):
    keyboard = [
        [InlineKeyboardButton('12:00 Блок «Автоматизация продаж» ', callback_data='Alps_1')],
        [InlineKeyboardButton('13:30 Нетворкинг', callback_data='Alps_2')],
        [InlineKeyboardButton('14:20 Блок «Построение предективной аналитики»', callback_data='Alps_3')],
        [InlineKeyboardButton('15:20 Блок «Автоматизация рекламных коммуникаций»', callback_data='Alps_4')],
        [InlineKeyboardButton('Назад', callback_data='Alps_5')],
        ]
    context.bot.send_message(update.effective_chat.id, 'Программа потока "Альпы"', reply_markup=InlineKeyboardMarkup(keyboard))

# функция отрисовки меню 'Заключительные мероприятия'
def finish_keyboard(update, context):
    keyboard = [
        [InlineKeyboardButton('16:40 Нетворкинг', callback_data='Finish_1'),
         InlineKeyboardButton('17:00 Премия "BMA 2020"', callback_data='Finish_2')],
        [InlineKeyboardButton('Назад', callback_data='Finish_3')],
        ]
    context.bot.send_message(update.effective_chat.id, 'А это будет в заключении', reply_markup=InlineKeyboardMarkup(keyboard))

# функция обработки кнопок ветка "Программа"
def button(update, context):
    q = update.callback_query
    q.answer()
    if q.data == 'Start_1':
        return program_keyboard(update, context)
    elif q.data == 'Start_2':
        pass
    elif q.data == 'Program_1':
        return entry_keyboard(update, context)
    elif q.data == 'Program_2':
        return everest_keyboard(update, context)
    elif q.data == 'Program_3':
        return alps_keyboard
    elif q.data == 'Program_4':
        return finish_keyboard(update, context)
    elif q.data == 'Program_5':
        return main_keyboard(update, context)
    elif q.data == 'Entry_1':
        pass
    elif q.data == 'Entry_2':
        pass
    elif q.data == 'Entry_3':
        pass
    elif q.data == 'Entry_4':
        return program_keyboard(update, context)
    elif q.data == 'Everest_1':
        pass
    elif q.data == 'Everest_2':
        pass
    elif q.data == 'Everest_3':
        pass
    elif q.data == 'Everest_4':
        pass
    elif q.data == 'Everest_5':
        pass
    elif q.data == 'Everest_6':
        return program_keyboard(update, context)
    elif q.data == 'Alps_1':
        pass
    elif q.data == 'Alps_2':
        pass
    elif q.data == 'Alps_3':
        pass
    elif q.data == 'Alps_4':
        pass
    elif q.data == 'Alps_5':
        return program_keyboard(update, context)
    elif q.data == 'Finish_1':
        pass
    elif q.data == 'Finish_2':
        pass
    elif q.data == 'Finish_3':
        return program_keyboard(update, context)


# функция обработки текстовых сообщений
def echo(update, context):
    text = 'ECHO: ' + update.message.text 
    context.bot.send_message(chat_id=update.effective_chat.id, 
                             text=text)    

# функция обработки команды '/caps'
def caps(update, context):
    if context.args:
        text_caps = ' '.join(context.args).upper()
        context.bot.send_message(chat_id=update.effective_chat.id, 
                                text=text_caps)
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, 
                                text='No command argument')
        context.bot.send_message(chat_id=update.effective_chat.id, 
                                text='send: /caps argument')

# функция обработки встроенного запроса
def inline_caps(update, context):
    query = update.inline_query.query
    if not query:
        return
    results = list()
    results.append(
        InlineQueryResultArticle(
            id=query.upper(),
            title='Convert to UPPER TEXT',
            input_message_content=InputTextMessageContent(query.upper())
        )
    )
    context.bot.answer_inline_query(update.inline_query.id, results)

# функция обработки не распознных команд
def unknown(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, 
                             text="Такой команды нет, попробуйте еще раз")


class Command(BaseCommand):

    load_dotenv()
    token = os.getenv("TG_BOT_TOKEN")
    bot = telegram.Bot(token=token)
    updater = Updater(token=token)
    dispatcher = updater.dispatcher
    # обработчик команды '/start'
    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)

    # обработчик команды '/main' вызовет первую основную клавиатуру
    main_keyboard_handler = CommandHandler('main', main_keyboard)
    dispatcher.add_handler(main_keyboard_handler)

    # обработчик нажатия кнопок
    button_handler = CallbackQueryHandler(button)
    dispatcher.add_handler(button_handler)

    # обработчик текстовых сообщений
    echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
    dispatcher.add_handler(echo_handler)

    # обработчик команды '/caps'
    caps_handler = CommandHandler('caps', caps)
    dispatcher.add_handler(caps_handler)

    # обработчик встроенных запросов 
    inline_caps_handler = InlineQueryHandler(inline_caps)
    dispatcher.add_handler(inline_caps_handler)

    # обработчик не распознных команд
    unknown_handler = MessageHandler(Filters.command, unknown)
    dispatcher.add_handler(unknown_handler)

    # запуск прослушивания сообщений
    updater.start_polling()
    # обработчик нажатия Ctrl+C
    updater.idle()