import telegram
import telebot #pyTelegramBotAPI-4.6.1
from dotenv import load_dotenv
import os
import time
from telegram import InlineQueryResultArticle, InputTextMessageContent, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, ConversationHandler
from telegram.ext import MessageHandler, Filters, InlineQueryHandler
from django.core.management.base import BaseCommand
from bot.models import Flow_group, Flow, Block

# функция обработки команды '/start'
def start(update, context):
    #global student_chat_id
    #student_chat_id = update.effective_chat.id
    
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Здравствуйте. Это официальный бот по поддержке участников")
    time.sleep(1)
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
    keyboard=[[InlineKeyboardButton('Главное меню', callback_data='Main_menu')]]
    flows = Flow.objects.all()
    for number, flow in enumerate(flows):
        button = [InlineKeyboardButton(f'{flow.title}', callback_data=f'Program_{number+1}')]
        keyboard.append(button)
    context.bot.send_message(update.effective_chat.id, 'Вот программа мероприятия', reply_markup=InlineKeyboardMarkup(keyboard))

# функция отрисовки меню всех блоков
def table_blocks(update, context, bases):
    keyboard = [[InlineKeyboardButton('Назад', callback_data='Back')]]
    for number, name in enumerate(bases):
        button = [InlineKeyboardButton(f'{name.start_time} {name.title}', callback_data=f'{name.flow_group.flow.title}_{number+1}')]
        keyboard.append(button)
    context.bot.send_message(update.effective_chat.id, 'В этом блоке будет следующее', reply_markup=InlineKeyboardMarkup(keyboard))

flows = Flow.objects.all()
block_entry = Block.objects.filter(flow_group__flow__title__contains='*Вступительные мероприятия')
block_everest = Block.objects.filter(flow_group__flow__title__contains='*Поток "Эверест"')
block_alps = Block.objects.filter(flow_group__flow__title__contains='*Поток "Альпы"')
block_finish = Block.objects.filter(flow_group__flow__title__contains='*Заключительные мероприятия')

# def info_blocks(update, context, bases, name):
#     print(bases.name.description_addition)
#     context.bot.send_message(chat_id=update.effective_chat.id,
#                              text="Здравствуйте. Это официальный бот по поддержке участников")



# функция отрисовки меню 'Задать вопрос спикеру'
def questions_keyboard(update, context):
    keyboard = [
        [InlineKeyboardButton('Вступительные мероприятия', callback_data='Questions_1')],
        [InlineKeyboardButton('Поток "Эверест"', callback_data='Questions_2'),
         InlineKeyboardButton('Поток "Альпы"', callback_data='Questions_3')],
        [InlineKeyboardButton('Главное меню', callback_data='Questions_4')]
    ]
    context.bot.send_message(update.effective_chat.id, 'Вот программа мероприятия', reply_markup=InlineKeyboardMarkup(keyboard))



# функция отрисовки меню-вопрос 'Вступительные мероприятия'
def entry_questuions_keyboard(update, context):
    keyboard = [
        [InlineKeyboardButton('Фёдор Федоров', callback_data='Entry_questuion_1'),
         InlineKeyboardButton('Денис Денисов', callback_data='Entry_questuion_2')],
        [InlineKeyboardButton('Борис Борисов', callback_data='Entry_questuion_3'),
         InlineKeyboardButton('Виталий Витальев', callback_data='Entry_questuion_4')],
        [InlineKeyboardButton('Сергей Сергеев', callback_data='Entry_questuion_5'),
         InlineKeyboardButton('Константин Константинов', callback_data='Entry_questuion_6')],
        [InlineKeyboardButton('Назад', callback_data='Entry_questuion_7')]
    ]
    context.bot.send_message(update.effective_chat.id, 'Спикеры "вступления"', reply_markup=InlineKeyboardMarkup(keyboard))

# функция отрисовки меню-вопрос 'Проект "Эверест"'
def everest_questuions_keyboard(update, context):
    keyboard = [
        [InlineKeyboardButton('12:00 – 13:30', callback_data='Everest_questuion_1'),
         InlineKeyboardButton('14:00 – 16:30', callback_data='Everest_questuion_2')],
        [InlineKeyboardButton('Назад', callback_data='Everest_questuion_3')]
    ]
    context.bot.send_message(update.effective_chat.id, 'Спикеры "Проект "Эверест"', reply_markup=InlineKeyboardMarkup(keyboard))

# функция отрисовки меню-вопрос 'Проект "Эверест" 12:00 - 13:30'
def everest_1_questuions_keyboard(update, context):
    keyboard = [
        [InlineKeyboardButton('Анна Аннова', callback_data='Everest_questuion_1.1'),
         InlineKeyboardButton('Сергей Володин', callback_data='Everest_questuion_1.2')],
        [InlineKeyboardButton('Михаил Михалов', callback_data='Everest_questuion_1.3'),
         InlineKeyboardButton('Максим Максимов,', callback_data='Everest_questuion_1.4')],
        [InlineKeyboardButton('Артем Артемов', callback_data='Everest_questuion_1.5')],
        [InlineKeyboardButton('Назад', callback_data='Everest_questuion_1.6')]
    ]
    context.bot.send_message(update.effective_chat.id, 'Спикеры "Проект "Эверест" c 12:00', reply_markup=InlineKeyboardMarkup(keyboard))

# функция отрисовки меню-вопрос 'Проект "Эверест" 14:00 - 16:30'
def everest_2_questuions_keyboard(update, context):
    keyboard = [
        [InlineKeyboardButton('Кирилл Кириенко', callback_data='Everest_questuion_2.1'),
         InlineKeyboardButton('Леся Самойлова', callback_data='Everest_questuion_2.2')],
        [InlineKeyboardButton('Надежда Бабкина', callback_data='Everest_questuion_2.3'),
         InlineKeyboardButton('Дмитрий Медведев', callback_data='Everest_questuion_2.4')],
        [InlineKeyboardButton('Евгений Евгеньев', callback_data='Everest_questuion_2.5'),
         InlineKeyboardButton('Екатерина Ворот', callback_data='Everest_questuion_2.6')],
        [InlineKeyboardButton('Татьяна Вилет', callback_data='Everest_questuion_2.7'),
         InlineKeyboardButton('Викторов Артем', callback_data='Everest_questuion_2.8')],
        [InlineKeyboardButton('Евгений Валуев', callback_data='Everest_questuion_2.9')],
        [InlineKeyboardButton('Назад', callback_data='Everest_questuion_2.10')]
    ]
    context.bot.send_message(update.effective_chat.id, 'Спикеры "Проект "Эверест" c 14:00', reply_markup=InlineKeyboardMarkup(keyboard))

# функция отрисовки меню-вопрос 'Проект "Альпы"'
def alps_questuions_keyboard(update, context):
    keyboard = [
        [InlineKeyboardButton('12:00 – 13:30', callback_data='Alps_questuion_1'),
         InlineKeyboardButton('14:00 – 16:30', callback_data='Alps_questuion_2')],
        [InlineKeyboardButton('Назад', callback_data='Alps_questuion_3')]
    ]
    context.bot.send_message(update.effective_chat.id, 'Спикеры "Проект "Альпы"', reply_markup=InlineKeyboardMarkup(keyboard))

# функция отрисовки меню-вопрос 'Проект "Альпы" 12:00 - 13:30'
def alps_1_questuions_keyboard(update, context):
    keyboard = [
        [InlineKeyboardButton('Сергей Кулькин', callback_data='Alps_questuion_1.1'),
         InlineKeyboardButton('Игорь Игорев', callback_data='Alps_questuion_1.2')],
        [InlineKeyboardButton('Дмитрий Бирюков', callback_data='Alps_questuion_1.3'),
         InlineKeyboardButton('Андрей Петров,', callback_data='Alps_questuion_1.4')],
        [InlineKeyboardButton('Назад', callback_data='Alps_questuion_1.5')]
    ]
    context.bot.send_message(update.effective_chat.id, 'Спикеры "Проект "Альпы" c 12:00', reply_markup=InlineKeyboardMarkup(keyboard))

# функция отрисовки меню-вопрос 'Проект "Альпы" 14:00 - 16:30'
def alps_2_questuions_keyboard(update, context):
    keyboard = [
        [InlineKeyboardButton('Алексей Петров', callback_data='Alps_questuion_2.1'),
         InlineKeyboardButton('Константин Константинопольский', callback_data='Alps_questuion_2.2')],
        [InlineKeyboardButton('Александр Бродский', callback_data='Alps_questuion_2.3'),
         InlineKeyboardButton('Алексей Жирков', callback_data='Alps_questuion_2.4')],
        [InlineKeyboardButton('Денис Глушаков', callback_data='Alps_questuion_2.5'),
         InlineKeyboardButton('Колбин Дмитрий', callback_data='Alps_questuion_2.6')],
        [InlineKeyboardButton('Алексей Пушилин', callback_data='Alps_questuion_2.7')],
        [InlineKeyboardButton('Назад', callback_data='Alps_questuion_2.8')]
        ]
    context.bot.send_message(update.effective_chat.id, 'Спикеры "Проект "Альпы" c 14:00', reply_markup=InlineKeyboardMarkup(keyboard))

# функция обработки кнопок ветка "Программа"
def button(update, context):
    global flag
    
    
    flag = False
    q = update.callback_query
    q.answer()
    if q.data == 'Start_1':
        return program_keyboard(update, context)
    elif q.data == 'Start_2':
        return questions_keyboard(update, context)
    elif q.data == 'Program_1':
        return table_blocks(update, context, bases=block_entry)
    elif q.data == 'Program_2':
        return table_blocks(update, context, bases=block_everest)
    elif q.data == 'Program_3':
        return table_blocks(update, context, bases=block_alps)
    elif q.data == 'Program_4':
        return table_blocks(update, context, bases=block_finish)
    elif q.data == 'Main_menu':
        return main_keyboard(update, context)
    elif q.data == '*Вступительные мероприятия_1':
        return info_blocks(update, context, bases=block_entry, name='*Регистрация')
    elif q.data == '*Вступительные мероприятия_2':
        pass
    elif q.data == '*Вступительные мероприятия_3':
        pass
    elif q.data == 'Back':
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
    elif q.data == 'Questions_1':
        return entry_questuions_keyboard(update, context)
    elif q.data == 'Questions_2':
        return everest_questuions_keyboard(update, context)
    elif q.data == 'Questions_3':
        return alps_questuions_keyboard(update, context)
    elif q.data == 'Questions_4':
        return main_keyboard(update, context)
    elif q.data == 'Entry_questuion_1':
        context.bot.send_message(update.effective_chat.id, 'Введите вопрос Федору')
        context.bot.send_message(update.effective_chat.id, 'Чтобы сменить спикера, нажмите кнопку "Назад"')
        conversation(update, context)
    
    elif q.data == 'Entry_questuion_2':
        context.bot.send_message(update.effective_chat.id, 'Введите вопрос Денису')
        context.bot.send_message(update.effective_chat.id, 'Чтобы сменить спикера, нажмите кнопку "Назад"')
        conversation(update, context)
    elif q.data == 'Entry_questuion_3':
        context.bot.send_message(update.effective_chat.id, 'Введите вопрос Борису')
        context.bot.send_message(update.effective_chat.id, 'Чтобы сменить спикера, нажмите кнопку "Назад"')
        conversation(update, context)        
    elif q.data == 'Entry_questuion_4':
        context.bot.send_message(update.effective_chat.id, 'Введите вопрос Виталию')
        context.bot.send_message(update.effective_chat.id, 'Чтобы сменить спикера, нажмите кнопку "Назад"')
        conversation(update, context)
    elif q.data == 'Entry_questuion_5':
        context.bot.send_message(update.effective_chat.id, 'Введите вопрос Сергею')
        context.bot.send_message(update.effective_chat.id, 'Чтобы сменить спикера, нажмите кнопку "Назад"')
        conversation(update, context)
    elif q.data == 'Entry_questuion_6':
        context.bot.send_message(update.effective_chat.id, 'Введите вопрос Константину')
        context.bot.send_message(update.effective_chat.id, 'Чтобы сменить спикера, нажмите кнопку "Назад"')
        conversation(update, context)
    elif q.data == 'Entry_questuion_7':
        flag = False
        return questions_keyboard(update, context)
    elif q.data == 'Everest_questuion_1':
        return everest_1_questuions_keyboard(update, context)
    elif q.data == 'Everest_questuion_2':
        return everest_2_questuions_keyboard(update, context)
    elif q.data == 'Everest_questuion_3':
        return questions_keyboard(update, context)
    elif q.data == 'Everest_questuion_1.1':
        context.bot.send_message(update.effective_chat.id, 'Введите вопрос Анне')
        context.bot.send_message(update.effective_chat.id, 'Чтобы сменить спикера, нажмите кнопку "Назад"')
        conversation(update, context)
    elif q.data == 'Everest_questuion_1.2':
        context.bot.send_message(update.effective_chat.id, 'Введите вопрос Сергею')
        context.bot.send_message(update.effective_chat.id, 'Чтобы сменить спикера, нажмите кнопку "Назад"')
        conversation(update, context)
    elif q.data == 'Everest_questuion_1.3':
        context.bot.send_message(update.effective_chat.id, 'Введите вопрос Михаилу')
        context.bot.send_message(update.effective_chat.id, 'Чтобы сменить спикера, нажмите кнопку "Назад"')
        conversation(update, context)
    elif q.data == 'Everest_questuion_1.4':
        context.bot.send_message(update.effective_chat.id, 'Введите вопрос Максиму')
        context.bot.send_message(update.effective_chat.id, 'Чтобы сменить спикера, нажмите кнопку "Назад"')
        conversation(update, context)
    elif q.data == 'Everest_questuion_1.5':
        context.bot.send_message(update.effective_chat.id, 'Введите вопрос Артему')
        context.bot.send_message(update.effective_chat.id, 'Чтобы сменить спикера, нажмите кнопку "Назад"')
        conversation(update, context)
    elif q.data == 'Everest_questuion_1.6':
        flag = False
        return everest_questuions_keyboard(update, context)
    elif q.data == 'Everest_questuion_2.1':
        context.bot.send_message(update.effective_chat.id, 'Введите вопрос Кириллу')
        context.bot.send_message(update.effective_chat.id, 'Чтобы сменить спикера, нажмите кнопку "Назад"')
        conversation(update, context)
    elif q.data == 'Everest_questuion_2.2':
        context.bot.send_message(update.effective_chat.id, 'Введите вопрос Леси')
        context.bot.send_message(update.effective_chat.id, 'Чтобы сменить спикера, нажмите кнопку "Назад"')
        conversation(update, context)
    elif q.data == 'Everest_questuion_2.3':
        context.bot.send_message(update.effective_chat.id, 'Введите вопрос Надежде')
        context.bot.send_message(update.effective_chat.id, 'Чтобы сменить спикера, нажмите кнопку "Назад"')
        conversation(update, context)
    elif q.data == 'Everest_questuion_2.4':
        context.bot.send_message(update.effective_chat.id, 'Введите вопрос Дмитрию')
        context.bot.send_message(update.effective_chat.id, 'Чтобы сменить спикера, нажмите кнопку "Назад"')
        conversation(update, context)
    elif q.data == 'Everest_questuion_2.5':
        context.bot.send_message(update.effective_chat.id, 'Введите вопрос Евгению')
        context.bot.send_message(update.effective_chat.id, 'Чтобы сменить спикера, нажмите кнопку "Назад"')
        conversation(update, context)
    elif q.data == 'Everest_questuion_2.6':
        context.bot.send_message(update.effective_chat.id, 'Введите вопрос Екатерине')
        context.bot.send_message(update.effective_chat.id, 'Чтобы сменить спикера, нажмите кнопку "Назад"')
        conversation(update, context)
    elif q.data == 'Everest_questuion_2.7':
        context.bot.send_message(update.effective_chat.id, 'Введите вопрос Татьяне')
        context.bot.send_message(update.effective_chat.id, 'Чтобы сменить спикера, нажмите кнопку "Назад"')
        conversation(update, context)
    elif q.data == 'Everest_questuion_2.8':
        context.bot.send_message(update.effective_chat.id, 'Введите вопрос Артему')
        context.bot.send_message(update.effective_chat.id, 'Чтобы сменить спикера, нажмите кнопку "Назад"')
        conversation(update, context)
    elif q.data == 'Everest_questuion_2.9':
        context.bot.send_message(update.effective_chat.id, 'Введите вопрос Евгению')
        context.bot.send_message(update.effective_chat.id, 'Чтобы сменить спикера, нажмите кнопку "Назад"')
        conversation(update, context)
    elif q.data == 'Everest_questuion_2.10':
        flag = False
        return everest_questuions_keyboard(update, context)
    elif q.data == 'Alps_questuion_1':
        return alps_1_questuions_keyboard(update, context)
    elif q.data == 'Alps_questuion_2':
        return alps_2_questuions_keyboard(update, context)
    elif q.data == 'Alps_questuion_3':
        return questions_keyboard(update, context)
    elif q.data == 'Alps_questuion_1.1':
        context.bot.send_message(update.effective_chat.id, 'Введите вопрос Сергею')
        context.bot.send_message(update.effective_chat.id, 'Чтобы сменить спикера, нажмите кнопку "Назад"')
        conversation(update, context)
    elif q.data == 'Alps_questuion_1.2':
        context.bot.send_message(update.effective_chat.id, 'Введите вопрос Игорю')
        context.bot.send_message(update.effective_chat.id, 'Чтобы сменить спикера, нажмите кнопку "Назад"')
        conversation(update, context)
    elif q.data == 'Alps_questuion_1.3':
        context.bot.send_message(update.effective_chat.id, 'Введите вопрос Дмитрию')
        context.bot.send_message(update.effective_chat.id, 'Чтобы сменить спикера, нажмите кнопку "Назад"')
        conversation(update, context)
    elif q.data == 'Alps_questuion_1.4':
        context.bot.send_message(update.effective_chat.id, 'Введите вопрос Андрею')
        context.bot.send_message(update.effective_chat.id, 'Чтобы сменить спикера, нажмите кнопку "Назад"')
        conversation(update, context)
    elif q.data == 'Alps_questuion_1.5':
        flag = False
        return alps_questuions_keyboard(update, context)
    elif q.data == 'Alps_questuion_2.1':
        context.bot.send_message(update.effective_chat.id, 'Введите вопрос Алексею')
        context.bot.send_message(update.effective_chat.id, 'Чтобы сменить спикера, нажмите кнопку "Назад"')
        conversation(update, context)
    elif q.data == 'Alps_questuion_2.2':
        context.bot.send_message(update.effective_chat.id, 'Введите вопрос Константину')
        context.bot.send_message(update.effective_chat.id, 'Чтобы сменить спикера, нажмите кнопку "Назад"')
        conversation(update, context)
    elif q.data == 'Alps_questuion_2.3':
        context.bot.send_message(update.effective_chat.id, 'Введите вопрос Александру')
        context.bot.send_message(update.effective_chat.id, 'Чтобы сменить спикера, нажмите кнопку "Назад"')
        conversation(update, context)
    elif q.data == 'Alps_questuion_2.4':
        context.bot.send_message(update.effective_chat.id, 'Введите вопрос Алексею')
        context.bot.send_message(update.effective_chat.id, 'Чтобы сменить спикера, нажмите кнопку "Назад"')
        conversation(update, context)
    elif q.data == 'Alps_questuion_2.5':
        context.bot.send_message(update.effective_chat.id, 'Введите вопрос Денису')
        context.bot.send_message(update.effective_chat.id, 'Чтобы сменить спикера, нажмите кнопку "Назад"')
        conversation(update, context)
    elif q.data == 'Alps_questuion_2.6':
        context.bot.send_message(update.effective_chat.id, 'Введите вопрос Дмитрию')
        context.bot.send_message(update.effective_chat.id, 'Чтобы сменить спикера, нажмите кнопку "Назад"')
        conversation(update, context)
    elif q.data == 'Alps_questuion_2.7':
        context.bot.send_message(update.effective_chat.id, 'Введите вопрос Алексею')
        context.bot.send_message(update.effective_chat.id, 'Чтобы сменить спикера, нажмите кнопку "Назад"')
        conversation(update, context)
    elif q.data == 'Alps_questuion_2.8':
        flag = False
        return alps_questuions_keyboard(update, context)


def conversation(update, context):
    flag = True
    context.bot.send_message(update.effective_chat.id, 'Введите вопрос Федору')
    context.bot.send_message(update.effective_chat.id, 'Чтобы сменить спикера, нажмите кнопку "Назад"')
    speaker_chat_id = '-1001758552115'#1774521104
    student_chat_id = update.effective_chat.id
    def forward_message(update, context):
        text = update.message.text
        nonlocal speaker_chat_id
        if flag:
            context.bot.send_message(chat_id=speaker_chat_id, text=text)
    def forward_message_student(update, context):
        text = update.message.text
        nonlocal student_chat_id 
        if flag:
            context.bot.send_message(chat_id=student_chat_id, text=text)        
    forward_message_handler_student = MessageHandler(Filters.reply, forward_message_student)
    dispatcher.add_handler(forward_message_handler_student)        
    forward_message_handler = MessageHandler(Filters.text & (~Filters.command), forward_message)
    dispatcher.add_handler(forward_message_handler)    

class Command(BaseCommand):

    load_dotenv()
    token = os.getenv("TG_BOT_TOKEN")
    global bot
    bot = telegram.Bot(token=token)
    global bot2
    bot2 = telebot.TeleBot(token)
    global dispatcher
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

    # запуск прослушивания сообщений
    updater.start_polling()
    # обработчик нажатия Ctrl+C
    updater.idle()