import telegram
from dotenv import load_dotenv
import os
import time
from telegram import InlineQueryResultArticle, InputTextMessageContent, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, ConversationHandler
from telegram.ext import MessageHandler, Filters, InlineQueryHandler
from django.core.management.base import BaseCommand
from bot.models import Flow_group, Flow, Block, Presentation, Speaker


# функция обработки команды '/start'
def start(update, context):
        
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
    for number, flow in enumerate(flows, start=1):
        button = [InlineKeyboardButton(f'{flow.title}', callback_data=f'Program_{number}')]
        keyboard.append(button)
    context.bot.send_message(update.effective_chat.id, 'Вот программа мероприятия', reply_markup=InlineKeyboardMarkup(keyboard))

# функция отрисовки меню всех блоков
def table_blocks(update, context, bases):
    keyboard = [[InlineKeyboardButton('Назад', callback_data='Back')]]
    for number, name in enumerate(bases, start=1):
        button = [InlineKeyboardButton(f'{name.start_time} {name.title}', callback_data=f'{name.flow_group.flow.title}_{number}')]
        keyboard.append(button)
    context.bot.send_message(update.effective_chat.id, 'В этом блоке будет следующее', reply_markup=InlineKeyboardMarkup(keyboard))

flows = Flow.objects.all()
block_entry = Block.objects.filter(flow_group__flow__title__contains='*Вступительные мероприятия')
block_everest = Block.objects.filter(flow_group__flow__title__contains='*Поток "Эверест"')
block_alps = Block.objects.filter(flow_group__flow__title__contains='*Поток "Альпы"')
block_finish = Block.objects.filter(flow_group__flow__title__contains='*Заключительные мероприятия')


# функция открытия файла нужна для info_blocks
def open_file(name):
    a = open(name, 'r')
    data = a.read()
    a.close()
    return data

# функция расшифровки любого блока
def info_blocks(update, context, bases):
    with open('инфо_блок.txt', 'a') as info:
        info.write(f'{bases[0].block.start_time} - {bases[0].block.end_time} \n')
        info.write(bases[0].block.title + '\n' + '\n')
        for presentation in bases:
            info.write(presentation.title +'\n')
            speakers = Speaker.objects.filter(presentations__title=presentation)
            for speaker in speakers:
                info.write(speaker.full_name +'\n')
                info.write(speaker.job_title +'\n' + '\n')
    context.bot.send_message(update.effective_chat.id, open_file('инфо_блок.txt'))
    os.remove('инфо_блок.txt')


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

# flows = Flow.objects.all()
# это для отрисовки клавиатур по потокам
block_entry = Block.objects.filter(flow_group__flow__title__contains='*Вступительные мероприятия')
block_everest = Block.objects.filter(flow_group__flow__title__contains='*Поток "Эверест"')
block_alps = Block.objects.filter(flow_group__flow__title__contains='*Поток "Альпы"')
block_finish = Block.objects.filter(flow_group__flow__title__contains='*Заключительные мероприятия')

# это для расшифровки каждого блока
presentations_entry_1 = Presentation.objects.filter(block__title__contains='Дискуссия - пути развития рынка разработки.')

presentations_everest_1 = Presentation.objects.filter(block__title__contains='Коммуникационные инновации')
presentations_everest_2 = Presentation.objects.filter(block__title__contains='Построение предективной аналитики')
presentations_everest_3 = Presentation.objects.filter(block__title__contains='Автоматизация рекламных коммуникаций')
presentations_everest_4 = Presentation.objects.filter(block__title__contains='Системы управления коммуникациями')

presentations_alps_1 = Presentation.objects.filter(block__title__contains='Автоматизация продаж')
presentations_alps_2 = Presentation.objects.filter(block__title__contains='Построение предективной аналитики')
presentations_alps_3 = Presentation.objects.filter(block__title__contains='Автоматизация рекламных коммуникаций')

# функция обработки кнопок ветка "Программа"
def button(update, context):
    global flag
    global speaker_chat_id
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
        pass
    elif q.data == '*Вступительные мероприятия_2':
        return info_blocks(update, context, bases=presentations_entry_1)
    elif q.data == '*Вступительные мероприятия_3':
        pass
    elif q.data == 'Back':
        return program_keyboard(update, context)
    elif q.data == '*Поток "Эверест"_1':
        return info_blocks(update, context, bases=presentations_everest_1)
    elif q.data == '*Поток "Эверест"_2':
        pass
    elif q.data == '*Поток "Эверест"_3':
        return info_blocks(update, context, bases=presentations_everest_2)
    elif q.data == '*Поток "Эверест"_4':
        return info_blocks(update, context, bases=presentations_everest_3)
    elif q.data == '*Поток "Эверест"_5':
        return info_blocks(update, context, bases=presentations_everest_4)
    elif q.data == 'Back':
        return program_keyboard(update, context)
    elif q.data == '*Поток "Альпы"_1':
        return info_blocks(update, context, bases=presentations_alps_1)
    elif q.data == '*Поток "Альпы"_2':
        pass
    elif q.data == '*Поток "Альпы"_3':
        return info_blocks(update, context, bases=presentations_alps_2)
    elif q.data == '*Поток "Альпы"_4':
        return info_blocks(update, context, bases=presentations_alps_3)
    elif q.data == 'Back':
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
        speaker_chat_id = '1774521104'
        conversation(update, context, speaker_chat_id)
    
    elif q.data == 'Entry_questuion_2':
        context.bot.send_message(update.effective_chat.id, 'Введите вопрос Денису')
        context.bot.send_message(update.effective_chat.id, 'Чтобы сменить спикера, нажмите кнопку "Назад"')
        speaker_chat_id = '-1001758552115'
        conversation(update, context, speaker_chat_id)
    elif q.data == 'Entry_questuion_3':
        context.bot.send_message(update.effective_chat.id, 'Введите вопрос Борису')
        context.bot.send_message(update.effective_chat.id, 'Чтобы сменить спикера, нажмите кнопку "Назад"')
        speaker_chat_id = '-1001758552115'
        conversation(update, context, speaker_chat_id)        
    elif q.data == 'Entry_questuion_4':
        context.bot.send_message(update.effective_chat.id, 'Введите вопрос Виталию')
        context.bot.send_message(update.effective_chat.id, 'Чтобы сменить спикера, нажмите кнопку "Назад"')
        speaker_chat_id = '-1001758552115'
        conversation(update, context, speaker_chat_id)
    elif q.data == 'Entry_questuion_5':
        context.bot.send_message(update.effective_chat.id, 'Введите вопрос Сергею')
        context.bot.send_message(update.effective_chat.id, 'Чтобы сменить спикера, нажмите кнопку "Назад"')
        speaker_chat_id = '-1001758552115'
        conversation(update, context, speaker_chat_id)
    elif q.data == 'Entry_questuion_6':
        context.bot.send_message(update.effective_chat.id, 'Введите вопрос Константину')
        context.bot.send_message(update.effective_chat.id, 'Чтобы сменить спикера, нажмите кнопку "Назад"')
        speaker_chat_id = '-1001758552115'
        conversation(update, context, speaker_chat_id)
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
        speaker_chat_id = '-1001758552115'
        conversation(update, context, speaker_chat_id)
    elif q.data == 'Everest_questuion_1.2':
        context.bot.send_message(update.effective_chat.id, 'Введите вопрос Сергею')
        context.bot.send_message(update.effective_chat.id, 'Чтобы сменить спикера, нажмите кнопку "Назад"')
        speaker_chat_id = '-1001758552115'
        conversation(update, context, speaker_chat_id)
    elif q.data == 'Everest_questuion_1.3':
        context.bot.send_message(update.effective_chat.id, 'Введите вопрос Михаилу')
        context.bot.send_message(update.effective_chat.id, 'Чтобы сменить спикера, нажмите кнопку "Назад"')
        speaker_chat_id = '-1001758552115'
        conversation(update, context, speaker_chat_id)
    elif q.data == 'Everest_questuion_1.4':
        context.bot.send_message(update.effective_chat.id, 'Введите вопрос Максиму')
        context.bot.send_message(update.effective_chat.id, 'Чтобы сменить спикера, нажмите кнопку "Назад"')
        speaker_chat_id = '-1001758552115'
        conversation(update, context, speaker_chat_id)
    elif q.data == 'Everest_questuion_1.5':
        context.bot.send_message(update.effective_chat.id, 'Введите вопрос Артему')
        context.bot.send_message(update.effective_chat.id, 'Чтобы сменить спикера, нажмите кнопку "Назад"')
        speaker_chat_id = '-1001758552115'
        conversation(update, context, speaker_chat_id)
    elif q.data == 'Everest_questuion_1.6':
        flag = False
        return everest_questuions_keyboard(update, context)
    elif q.data == 'Everest_questuion_2.1':
        context.bot.send_message(update.effective_chat.id, 'Введите вопрос Кириллу')
        context.bot.send_message(update.effective_chat.id, 'Чтобы сменить спикера, нажмите кнопку "Назад"')
        speaker_chat_id = '-1001758552115'
        conversation(update, context, speaker_chat_id)
    elif q.data == 'Everest_questuion_2.2':
        context.bot.send_message(update.effective_chat.id, 'Введите вопрос Леси')
        context.bot.send_message(update.effective_chat.id, 'Чтобы сменить спикера, нажмите кнопку "Назад"')
        speaker_chat_id = '-1001758552115'
        conversation(update, context, speaker_chat_id)
    elif q.data == 'Everest_questuion_2.3':
        context.bot.send_message(update.effective_chat.id, 'Введите вопрос Надежде')
        context.bot.send_message(update.effective_chat.id, 'Чтобы сменить спикера, нажмите кнопку "Назад"')
        speaker_chat_id = '-1001758552115'
        conversation(update, context, speaker_chat_id)
    elif q.data == 'Everest_questuion_2.4':
        context.bot.send_message(update.effective_chat.id, 'Введите вопрос Дмитрию')
        context.bot.send_message(update.effective_chat.id, 'Чтобы сменить спикера, нажмите кнопку "Назад"')
        speaker_chat_id = '-1001758552115'
        conversation(update, context, speaker_chat_id)
    elif q.data == 'Everest_questuion_2.5':
        context.bot.send_message(update.effective_chat.id, 'Введите вопрос Евгению')
        context.bot.send_message(update.effective_chat.id, 'Чтобы сменить спикера, нажмите кнопку "Назад"')
        speaker_chat_id = '-1001758552115'
        conversation(update, context, speaker_chat_id)
    elif q.data == 'Everest_questuion_2.6':
        context.bot.send_message(update.effective_chat.id, 'Введите вопрос Екатерине')
        context.bot.send_message(update.effective_chat.id, 'Чтобы сменить спикера, нажмите кнопку "Назад"')
        speaker_chat_id = '-1001758552115'
        conversation(update, context, speaker_chat_id)
    elif q.data == 'Everest_questuion_2.7':
        context.bot.send_message(update.effective_chat.id, 'Введите вопрос Татьяне')
        context.bot.send_message(update.effective_chat.id, 'Чтобы сменить спикера, нажмите кнопку "Назад"')
        speaker_chat_id = '-1001758552115'
        conversation(update, context, speaker_chat_id)
    elif q.data == 'Everest_questuion_2.8':
        context.bot.send_message(update.effective_chat.id, 'Введите вопрос Артему')
        context.bot.send_message(update.effective_chat.id, 'Чтобы сменить спикера, нажмите кнопку "Назад"')
        speaker_chat_id = '-1001758552115'
        conversation(update, context, speaker_chat_id)
    elif q.data == 'Everest_questuion_2.9':
        context.bot.send_message(update.effective_chat.id, 'Введите вопрос Евгению')
        context.bot.send_message(update.effective_chat.id, 'Чтобы сменить спикера, нажмите кнопку "Назад"')
        speaker_chat_id = '-1001758552115'
        conversation(update, context, speaker_chat_id)
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
        speaker_chat_id = '-1001758552115'
        conversation(update, context, speaker_chat_id)
    elif q.data == 'Alps_questuion_1.2':
        context.bot.send_message(update.effective_chat.id, 'Введите вопрос Игорю')
        context.bot.send_message(update.effective_chat.id, 'Чтобы сменить спикера, нажмите кнопку "Назад"')
        speaker_chat_id = '-1001758552115'
        conversation(update, context, speaker_chat_id)
    elif q.data == 'Alps_questuion_1.3':
        context.bot.send_message(update.effective_chat.id, 'Введите вопрос Дмитрию')
        context.bot.send_message(update.effective_chat.id, 'Чтобы сменить спикера, нажмите кнопку "Назад"')
        speaker_chat_id = '-1001758552115'
        conversation(update, context, speaker_chat_id)
    elif q.data == 'Alps_questuion_1.4':
        context.bot.send_message(update.effective_chat.id, 'Введите вопрос Андрею')
        context.bot.send_message(update.effective_chat.id, 'Чтобы сменить спикера, нажмите кнопку "Назад"')
        speaker_chat_id = '-1001758552115'
        conversation(update, context, speaker_chat_id)
    elif q.data == 'Alps_questuion_1.5':
        flag = False
        return alps_questuions_keyboard(update, context)
    elif q.data == 'Alps_questuion_2.1':
        context.bot.send_message(update.effective_chat.id, 'Введите вопрос Алексею')
        context.bot.send_message(update.effective_chat.id, 'Чтобы сменить спикера, нажмите кнопку "Назад"')
        speaker_chat_id = '-1001758552115'
        conversation(update, context, speaker_chat_id)
    elif q.data == 'Alps_questuion_2.2':
        context.bot.send_message(update.effective_chat.id, 'Введите вопрос Константину')
        context.bot.send_message(update.effective_chat.id, 'Чтобы сменить спикера, нажмите кнопку "Назад"')
        speaker_chat_id = '-1001758552115'
        conversation(update, context, speaker_chat_id)
    elif q.data == 'Alps_questuion_2.3':
        context.bot.send_message(update.effective_chat.id, 'Введите вопрос Александру')
        context.bot.send_message(update.effective_chat.id, 'Чтобы сменить спикера, нажмите кнопку "Назад"')
        speaker_chat_id = '-1001758552115'
        conversation(update, context, speaker_chat_id)
    elif q.data == 'Alps_questuion_2.4':
        context.bot.send_message(update.effective_chat.id, 'Введите вопрос Алексею')
        context.bot.send_message(update.effective_chat.id, 'Чтобы сменить спикера, нажмите кнопку "Назад"')
        speaker_chat_id = '-1001758552115'
        conversation(update, context, speaker_chat_id)
    elif q.data == 'Alps_questuion_2.5':
        context.bot.send_message(update.effective_chat.id, 'Введите вопрос Денису')
        context.bot.send_message(update.effective_chat.id, 'Чтобы сменить спикера, нажмите кнопку "Назад"')
        speaker_chat_id = '-1001758552115'
        conversation(update, context, speaker_chat_id)
    elif q.data == 'Alps_questuion_2.6':
        context.bot.send_message(update.effective_chat.id, 'Введите вопрос Дмитрию')
        context.bot.send_message(update.effective_chat.id, 'Чтобы сменить спикера, нажмите кнопку "Назад"')
        speaker_chat_id = '-1001758552115'
        conversation(update, context, speaker_chat_id)
    elif q.data == 'Alps_questuion_2.7':
        context.bot.send_message(update.effective_chat.id, 'Введите вопрос Алексею')
        context.bot.send_message(update.effective_chat.id, 'Чтобы сменить спикера, нажмите кнопку "Назад"')
        speaker_chat_id = '-1001758552115'
        conversation(update, context, speaker_chat_id)
    elif q.data == 'Alps_questuion_2.8':
        flag = False
        return alps_questuions_keyboard(update, context)


def conversation(update, context, speaker_chat_id):
    global flag
    flag = True
    speaker_chat_id = speaker_chat_id
    def forward_message(update, context):
        global speaker_chat_id
        if flag:
            forwarded = update.message.forward(chat_id=speaker_chat_id)
            if not forwarded.forward_from:
                context.bot.send_message(
                        chat_id=speaker_chat_id,
                        reply_to_message_id=forwarded.message_id,
                        text=update.message.from_user.id
                    )
    def forward_message_student(update, context):
        user_id = None
        if update.message.reply_to_message.forward_from:
            user_id = update.message.reply_to_message.forward_from.id
        elif update.message.reply_to_message.text:
            try:
                user_id = int(update.message.reply_to_message.text.split('\n')[0])
            except ValueError:
                user_id = None
        if user_id:
            context.bot.copy_message(
            message_id=update.message.message_id,
            chat_id=user_id,
            from_chat_id=update.message.chat_id
        )        
    forward_message_handler_student = MessageHandler(Filters.reply, forward_message_student)
    dispatcher.add_handler(forward_message_handler_student)        
    forward_message_handler = MessageHandler(Filters.text & (~Filters.command), forward_message)
    dispatcher.add_handler(forward_message_handler)
    

class Command(BaseCommand):

    load_dotenv()
    token = os.getenv("TG_BOT_TOKEN")
    global bot
    bot = telegram.Bot(token=token)
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
