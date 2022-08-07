import os
import time
import telegram
from telegram import InlineQueryResultArticle, InputTextMessageContent, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import MessageHandler, Filters, InlineQueryHandler,Updater, CommandHandler, CallbackQueryHandler, ConversationHandler

from bot.models import Flow, Block, Presentation, Speaker, Flow_group
from django.core.management.base import BaseCommand
from dotenv import load_dotenv


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
    context.bot.send_message(update.effective_chat.id, 'Это основное меню мероприятия',
                             reply_markup=InlineKeyboardMarkup(keyboard))


# Программа
# функция отрисовки меню 'Программа', 'Задать вопрос спикеру'
def program_keyboard(update, context, title):
    keyboard = [[InlineKeyboardButton('Главное меню', callback_data='Main_menu')]]
    flows = Flow.objects.all()
    for number, flow in enumerate(flows, start=1):
        button = [InlineKeyboardButton(f'{flow.title}', callback_data=f'{title}_{number}')]
        keyboard.append(button)
    context.bot.send_message(update.effective_chat.id, 'Вот программа мероприятия',
                             reply_markup=InlineKeyboardMarkup(keyboard))


# это функция для получения названия кнопок для клавиатур по потокам
def buttons_flow_names(structure):
    buttons = {}
    for number, element in enumerate(structure, start=1):
        block = Block.objects.filter(flow_group__flow__title__contains=element.title)
        buttons[f'block_{number}'] = block
    return buttons



# это функция для получения названия кнопок для блоков без презентаций
def buttons_additional_block_names(structure):
    buttons = {}
    for number, element in enumerate(structure, start=1):
        block = element.title
        buttons[f'block_{number}'] = block
    return buttons


# это функция для получения названия кнопок для блоков с презентациями
def buttons_block_names(structure):
    buttons = {}
    for number, element in enumerate(structure, start=1):
        block = Presentation.objects.filter(block__title__contains=element.title)
        buttons[f'block_{number}'] = block
    return buttons


# функция отрисовки меню всех блоков в ветке "Программа"
def table_blocks(update, context, bases, button_name):
    keyboard = [[InlineKeyboardButton('Назад', callback_data='Back')]]
    for number, name in enumerate(bases, start=1):
        button = [InlineKeyboardButton(f'{name.start_time} {name.title}', callback_data=f'{button_name}_{number}')]
        keyboard.append(button)
    context.bot.send_message(update.effective_chat.id, 'В этом блоке будет следующее',
                             reply_markup=InlineKeyboardMarkup(keyboard))


# функция открытия файла нужна для info_blocks, add_description_addition
def open_file(name):
    a = open(name, 'r')
    data = a.read()
    a.close()
    return data


# функция расшифровки любого блока c презентациями
def info_blocks(update, context, bases):
    with open('инфо_блок.txt', 'a') as info:
        info.write(f'{bases[0].block.start_time} - {bases[0].block.end_time} \n')
        info.write(bases[0].block.title + '\n' + '\n')
        for presentation in bases:
            info.write(presentation.title + '\n')
            speakers = Speaker.objects.filter(presentations__title=presentation)
            for speaker in speakers:
                info.write(speaker.full_name + '\n')
                info.write(speaker.job_title + '\n' + '\n')
    context.bot.send_message(update.effective_chat.id, open_file('инфо_блок.txt'))
    os.remove('инфо_блок.txt')
    return program_keyboard(update, context, title='Program')


# функция расшифровки любого блока без презентаций
def add_description_addition(update, context, title, number=1):
    blocks = Block.objects.filter(title__contains=title)
    with open('инфо_блок.txt', 'a') as info:
        info.write(f'{blocks[number - 1].start_time} - {blocks[number - 1].end_time} \n')
        info.write(blocks[number - 1].title + '\n')
        info.write(blocks[number - 1].description_addition + '\n')
    context.bot.send_message(update.effective_chat.id, open_file('инфо_блок.txt'))
    os.remove('инфо_блок.txt')

# Вопросы спикеру

# функция отрисовки меню всех блоков в ветке "Задать вопрос спикеру"
def table_speakers_blocks(update, context, bases, button_name):
    keyboard = [[InlineKeyboardButton('Назад', callback_data='Back_speakers')]]
    for number, name in enumerate(bases, start=1):
        button = [InlineKeyboardButton(f'{name.full_name} {name.job_title}', callback_data=f'{button_name}_{number}')]
        keyboard.append(button)
    context.bot.send_message(update.effective_chat.id, 'Спикеры этого блока',
                             reply_markup=InlineKeyboardMarkup(keyboard))

# это функция для получения названия кнопок c именами спикеров
def buttons_speakers_names(structure):
    buttons = {}
    for number, element in enumerate(structure, start=1):
        block = Speaker.objects.filter(presentations__block__flow_group__title__contains=element.title)
        buttons[f'seaction_{number}'] = block
    return buttons


# функция отрисовки меню-вопрос 'Проект "Эверест"'
def everest_questuions_keyboard(update, context):
    keyboard = [
        [InlineKeyboardButton('12:00 – 13:30', callback_data='Everest_questuion_1'),
         InlineKeyboardButton('14:00 – 16:30', callback_data='Everest_questuion_2')],
        [InlineKeyboardButton('Назад', callback_data='Back_speakers')]
    ]
    context.bot.send_message(update.effective_chat.id, 'Спикеры "Проект "Эверест"',
                             reply_markup=InlineKeyboardMarkup(keyboard))


# функция отрисовки меню-вопрос 'Проект "Альпы"'
def alps_questuions_keyboard(update, context):
    keyboard = [
        [InlineKeyboardButton('12:00 – 13:30', callback_data='Alps_questuion_1'),
         InlineKeyboardButton('14:00 – 16:30', callback_data='Alps_questuion_2')],
        [InlineKeyboardButton('Назад', callback_data='Back_speakers')]
    ]
    context.bot.send_message(update.effective_chat.id, 'Спикеры "Проект "Альпы"',
                             reply_markup=InlineKeyboardMarkup(keyboard))

blokcs = Block.objects.all()
flows = Flow.objects.all()
flows_group = Flow_group.objects.all()
speakers = buttons_speakers_names(structure=flows_group)
flow_names = buttons_flow_names(structure=flows)
aditional_block_names = buttons_additional_block_names(structure=blokcs)
block_names = buttons_block_names(structure=blokcs)


def button(update, context):
    global flag
    flag = False
    q = update.callback_query
    q.answer()
    if q.data == 'Start_1':
        return program_keyboard(update, context, title='Program')
    elif q.data == 'Start_2':
        return program_keyboard(update, context, title='Questions')
    elif q.data == 'Program_1':
        return table_blocks(update, context, bases=flow_names['block_1'],
                            button_name='Вступительные мероприятия')
    elif q.data == 'Program_2':
        return table_blocks(update, context, bases=flow_names['block_2'],
                            button_name='Поток "Эверест"')
    elif q.data == 'Program_3':
        return table_blocks(update, context, bases=flow_names['block_3'],
                            button_name='Поток "Альпы"')
    elif q.data == 'Program_4':
        return table_blocks(update, context, bases=flow_names['block_4'],
                            button_name='Заключительные мероприятия')
    elif q.data == 'Main_menu':
        return main_keyboard(update, context)
    elif q.data == 'Вступительные мероприятия_1':
        return add_description_addition(update, context,
                                        title=aditional_block_names['block_1'])
    elif q.data == 'Вступительные мероприятия_2':
        return info_blocks(update, context, bases=block_names['block_2'])
    elif q.data == 'Вступительные мероприятия_3':
        return add_description_addition(update, context,
                                        title=aditional_block_names['block_3'])
    elif q.data == 'Back':
        return program_keyboard(update, context,title='Program')
    elif q.data == 'Поток "Эверест"_1':
        return info_blocks(update, context, bases=block_names['block_4'])
    elif q.data == 'Поток "Эверест"_2':
        return add_description_addition(update, context,
                                        title=aditional_block_names['block_5'])
    elif q.data == 'Поток "Эверест"_3':
        return info_blocks(update, context, bases=block_names['block_6'])
    elif q.data == 'Поток "Эверест"_4':
        return info_blocks(update, context, bases=block_names['block_7'])
    elif q.data == 'Поток "Эверест"_5':
        return info_blocks(update, context, bases=block_names['block_8'])
    elif q.data == 'Back':
        return program_keyboard(update, context, title='Program')
    elif q.data == 'Поток "Альпы"_1':
        return info_blocks(update, context, bases=block_names['block_9'])
    elif q.data == 'Поток "Альпы"_2':
        return add_description_addition(update, context,
                                        title=aditional_block_names['block_10'], number=2)
    elif q.data == 'Поток "Альпы"_3':
        return info_blocks(update, context, bases=block_names['block_11'])
    elif q.data == 'Поток "Альпы"_4':
        return info_blocks(update, context, bases=block_names['block_12'])
    elif q.data == 'Back':
        return program_keyboard(update, context, title='Program')
    elif q.data == 'Заключительные мероприятия_1':
        return add_description_addition(update, context,
                                        title=aditional_block_names['block_13'], number=3)
    elif q.data == 'Заключительные мероприятия_2':
        return add_description_addition(update, context,
                                        title=aditional_block_names['block_14'])
    elif q.data == 'Back':
        return program_keyboard(update, context, title='Program')
    elif q.data == 'Questions_1':
        return table_speakers_blocks(update, context,
                                     bases=speakers['seaction_1'],
                                     button_name='Entry_questuion')
    elif q.data == 'Questions_2':
        return everest_questuions_keyboard(update, context)
    elif q.data == 'Questions_3':
        return alps_questuions_keyboard(update, context)
    elif q.data == 'Main_menu':
        return main_keyboard(update, context)
    elif q.data == 'Entry_questuion_1':
        speaker = speakers['seaction_1'][0]
        context.bot.send_message(update.effective_chat.id, f"Введите вопрос {speaker}")
        context.bot.send_message(update.effective_chat.id, 'Чтобы сменить спикера, нажмите кнопку "Назад"')
        conversation(update, context, speaker_chat_id=speaker.id_telegram)
    elif q.data == 'Entry_questuion_2':
        speaker = speakers['seaction_1'][1]
        context.bot.send_message(update.effective_chat.id, f"Введите вопрос {speaker}")
        context.bot.send_message(update.effective_chat.id, 'Чтобы сменить спикера, нажмите кнопку "Назад"')
        conversation(update, context, speaker_chat_id=speaker.id_telegram)
    elif q.data == 'Entry_questuion_3':
        speaker = speakers['seaction_1'][2]
        context.bot.send_message(update.effective_chat.id, f"Введите вопрос {speaker}")
        context.bot.send_message(update.effective_chat.id, 'Чтобы сменить спикера, нажмите кнопку "Назад"')
        conversation(update, context, speaker_chat_id=speaker.id_telegram)
    elif q.data == 'Entry_questuion_4':
        speaker = speakers['seaction_1'][3]
        context.bot.send_message(update.effective_chat.id, f"Введите вопрос {speaker}")
        context.bot.send_message(update.effective_chat.id, 'Чтобы сменить спикера, нажмите кнопку "Назад"')
        conversation(update, context, speaker_chat_id=speaker.id_telegram)
    elif q.data == 'Entry_questuion_5':
        speaker = speakers['seaction_1'][4]
        context.bot.send_message(update.effective_chat.id, f"Введите вопрос {speaker}")
        context.bot.send_message(update.effective_chat.id, 'Чтобы сменить спикера, нажмите кнопку "Назад"')
        conversation(update, context, speaker_chat_id=speaker.id_telegram)
    elif q.data == 'Entry_questuion_6':
        speaker = speakers['seaction_1'][5]
        context.bot.send_message(update.effective_chat.id, f"Введите вопрос {speaker}")
        context.bot.send_message(update.effective_chat.id, 'Чтобы сменить спикера, нажмите кнопку "Назад"')
        conversation(update, context, speaker_chat_id=speaker.id_telegram)
    elif q.data == 'Back_speakers':
        return program_keyboard(update, context, title='Questions')
    elif q.data == 'Everest_questuion_1':
        return table_speakers_blocks(update, context,
                                     bases=speakers['seaction_2'],
                                     button_name='Everest_questuion_1')
    elif q.data == 'Everest_questuion_2':
        return table_speakers_blocks(update, context,
                                     bases=speakers['seaction_3'],
                                     button_name='Everest_questuion_2')
    elif q.data == 'Back_speakers':
        return program_keyboard(update, context, title='Questions')
    elif q.data == 'Everest_questuion_1_1':
        speaker = speakers['seaction_2'][0]
        context.bot.send_message(update.effective_chat.id, f"Введите вопрос {speaker}")
        context.bot.send_message(update.effective_chat.id, 'Чтобы сменить спикера, нажмите кнопку "Назад"')
        conversation(update, context, speaker_chat_id=speaker.id_telegram)
    elif q.data == 'Everest_questuion_1_2':
        speaker = speakers['seaction_2'][1]
        context.bot.send_message(update.effective_chat.id, f"Введите вопрос {speaker}")
        context.bot.send_message(update.effective_chat.id, 'Чтобы сменить спикера, нажмите кнопку "Назад"')
        conversation(update, context, speaker_chat_id=speaker.id_telegram)
    elif q.data == 'Everest_questuion_1_3':
        speaker = speakers['seaction_2'][2]
        context.bot.send_message(update.effective_chat.id, f"Введите вопрос {speaker}")
        context.bot.send_message(update.effective_chat.id, 'Чтобы сменить спикера, нажмите кнопку "Назад"')
        conversation(update, context, speaker_chat_id=speaker.id_telegram)
    elif q.data == 'Everest_questuion_1_4':
        speaker = speakers['seaction_2'][3]
        context.bot.send_message(update.effective_chat.id, f"Введите вопрос {speaker}")
        context.bot.send_message(update.effective_chat.id, 'Чтобы сменить спикера, нажмите кнопку "Назад"')
        conversation(update, context, speaker_chat_id=speaker.id_telegram)
    elif q.data == 'Everest_questuion_1_5':
        speaker = speakers['seaction_2'][4]
        context.bot.send_message(update.effective_chat.id, f"Введите вопрос {speaker}")
        context.bot.send_message(update.effective_chat.id, 'Чтобы сменить спикера, нажмите кнопку "Назад"')
        conversation(update, context, speaker_chat_id=speaker.id_telegram)
    elif q.data == 'Back_speakers':
        flag = False
        return program_keyboard(update, context, title='Questions')
    elif q.data == 'Everest_questuion_2_1':
        speaker = speakers['seaction_3'][0]
        context.bot.send_message(update.effective_chat.id, f"Введите вопрос {speaker}")
        context.bot.send_message(update.effective_chat.id, 'Чтобы сменить спикера, нажмите кнопку "Назад"')
        conversation(update, context, speaker_chat_id=speaker.id_telegram)
    elif q.data == 'Everest_questuion_2_2':
        speaker = speakers['seaction_3'][1]
        context.bot.send_message(update.effective_chat.id, f"Введите вопрос {speaker}")
        context.bot.send_message(update.effective_chat.id, 'Чтобы сменить спикера, нажмите кнопку "Назад"')
        conversation(update, context, speaker_chat_id=speaker.id_telegram)
    elif q.data == 'Everest_questuion_2_3':
        speaker = speakers['seaction_3'][2]
        context.bot.send_message(update.effective_chat.id, f"Введите вопрос {speaker}")
        context.bot.send_message(update.effective_chat.id, 'Чтобы сменить спикера, нажмите кнопку "Назад"')
        conversation(update, context, speaker_chat_id=speaker.id_telegram)
    elif q.data == 'Everest_questuion_2_4':
        speaker = speakers['seaction_3'][3]
        context.bot.send_message(update.effective_chat.id, f"Введите вопрос {speaker}")
        context.bot.send_message(update.effective_chat.id, 'Чтобы сменить спикера, нажмите кнопку "Назад"')
        conversation(update, context, speaker_chat_id=speaker.id_telegram)
    elif q.data == 'Everest_questuion_2_5':
        speaker = speakers['seaction_3'][4]
        context.bot.send_message(update.effective_chat.id, f"Введите вопрос {speaker}")
        context.bot.send_message(update.effective_chat.id, 'Чтобы сменить спикера, нажмите кнопку "Назад"')
        conversation(update, context, speaker_chat_id=speaker.id_telegram)
    elif q.data == 'Everest_questuion_2_6':
        speaker = speakers['seaction_3'][5]
        context.bot.send_message(update.effective_chat.id, f"Введите вопрос {speaker}")
        context.bot.send_message(update.effective_chat.id, 'Чтобы сменить спикера, нажмите кнопку "Назад"')
        conversation(update, context, speaker_chat_id=speaker.id_telegram)
    elif q.data == 'Everest_questuion_2_7':
        speaker = speakers['seaction_3'][6]
        context.bot.send_message(update.effective_chat.id, f"Введите вопрос {speaker}")
        context.bot.send_message(update.effective_chat.id, 'Чтобы сменить спикера, нажмите кнопку "Назад"')
        conversation(update, context, speaker_chat_id=speaker.id_telegram)
    elif q.data == 'Everest_questuion_2_8':
        speaker = speakers['seaction_3'][7]
        context.bot.send_message(update.effective_chat.id, f"Введите вопрос {speaker}")
        context.bot.send_message(update.effective_chat.id, 'Чтобы сменить спикера, нажмите кнопку "Назад"')
        conversation(update, context, speaker_chat_id=speaker.id_telegram)
    elif q.data == 'Everest_questuion_2_9':
        speaker = speakers['seaction_3'][8]
        context.bot.send_message(update.effective_chat.id, f"Введите вопрос {speaker}")
        context.bot.send_message(update.effective_chat.id, 'Чтобы сменить спикера, нажмите кнопку "Назад"')
        conversation(update, context, speaker_chat_id=speaker.id_telegram)
    elif q.data == 'Back_speakers':
        flag = False
        return program_keyboard(update, context, title='Questions')
    elif q.data == 'Alps_questuion_1':
        return table_speakers_blocks(update, context,
                                     bases=speakers['seaction_4'],
                                     button_name='Alps_questuion_1')
    elif q.data == 'Alps_questuion_2':
        return table_speakers_blocks(update, context,
                             bases=speakers['seaction_5'],
                             button_name='Alps_questuion_2')
    elif q.data == 'Back_speakers':
        return program_keyboard(update, context, title='Questions')
    elif q.data == 'Alps_questuion_1_1':
        speaker = speakers['seaction_4'][0]
        context.bot.send_message(update.effective_chat.id, f"Введите вопрос {speaker}")
        context.bot.send_message(update.effective_chat.id, 'Чтобы сменить спикера, нажмите кнопку "Назад"')
        conversation(update, context, speaker_chat_id=speaker.id_telegram)
    elif q.data == 'Alps_questuion_1_2':
        speaker = speakers['seaction_4'][1]
        context.bot.send_message(update.effective_chat.id, f"Введите вопрос {speaker}")
        context.bot.send_message(update.effective_chat.id, 'Чтобы сменить спикера, нажмите кнопку "Назад"')
        conversation(update, context, speaker_chat_id=speaker.id_telegram)
    elif q.data == 'Alps_questuion_1_3':
        speaker = speakers['seaction_4'][2]
        context.bot.send_message(update.effective_chat.id, f"Введите вопрос {speaker}")
        context.bot.send_message(update.effective_chat.id, 'Чтобы сменить спикера, нажмите кнопку "Назад"')
        conversation(update, context, speaker_chat_id=speaker.id_telegram)
    elif q.data == 'Alps_questuion_1_4':
        speaker = speakers['seaction_4'][3]
        context.bot.send_message(update.effective_chat.id, f"Введите вопрос {speaker}")
        context.bot.send_message(update.effective_chat.id, 'Чтобы сменить спикера, нажмите кнопку "Назад"')
        conversation(update, context, speaker_chat_id=speaker.id_telegram)
    elif q.data == 'Back_speakers':
        flag = False
        return program_keyboard(update, context, title='Questions')
    elif q.data == 'Alps_questuion_2_1':
        speaker = speakers['seaction_5'][0]
        context.bot.send_message(update.effective_chat.id, f"Введите вопрос {speaker}")
        context.bot.send_message(update.effective_chat.id, 'Чтобы сменить спикера, нажмите кнопку "Назад"')
        conversation(update, context, speaker_chat_id=speaker.id_telegram)
    elif q.data == 'Alps_questuion_2_2':
        speaker = speakers['seaction_5'][0]
        context.bot.send_message(update.effective_chat.id, f"Введите вопрос {speaker}")
        context.bot.send_message(update.effective_chat.id, 'Чтобы сменить спикера, нажмите кнопку "Назад"')
        conversation(update, context, speaker_chat_id=speaker.id_telegram)
    elif q.data == 'Alps_questuion_2_3':
        speaker = speakers['seaction_5'][1]
        context.bot.send_message(update.effective_chat.id, f"Введите вопрос {speaker}")
        context.bot.send_message(update.effective_chat.id, 'Чтобы сменить спикера, нажмите кнопку "Назад"')
        conversation(update, context, speaker_chat_id=speaker.id_telegram)
    elif q.data == 'Alps_questuion_2_4':
        speaker = speakers['seaction_5'][2]
        context.bot.send_message(update.effective_chat.id, f"Введите вопрос {speaker}")
        context.bot.send_message(update.effective_chat.id, 'Чтобы сменить спикера, нажмите кнопку "Назад"')
        conversation(update, context, speaker_chat_id=speaker.id_telegram)
    elif q.data == 'Alps_questuion_2_5':
        speaker = speakers['seaction_5'][3]
        context.bot.send_message(update.effective_chat.id, f"Введите вопрос {speaker}")
        context.bot.send_message(update.effective_chat.id, 'Чтобы сменить спикера, нажмите кнопку "Назад"')
        conversation(update, context, speaker_chat_id=speaker.id_telegram)
    elif q.data == 'Alps_questuion_2_6':
        speaker = speakers['seaction_5'][4]
        context.bot.send_message(update.effective_chat.id, f"Введите вопрос {speaker}")
        context.bot.send_message(update.effective_chat.id, 'Чтобы сменить спикера, нажмите кнопку "Назад"')
        conversation(update, context, speaker_chat_id=speaker.id_telegram)
    elif q.data == 'Alps_questuion_2_7':
        speaker = speakers['seaction_5'][5]
        context.bot.send_message(update.effective_chat.id, f"Введите вопрос {speaker}")
        context.bot.send_message(update.effective_chat.id, 'Чтобы сменить спикера, нажмите кнопку "Назад"')
        conversation(update, context)
    elif q.data == 'Back_speakers':
        flag = False
        return program_keyboard(update, context, title='Questions')


def conversation(update, context, speaker_chat_id):
    flag = True
    def forward_message(update, context):
        nonlocal speaker_chat_id
        if flag:
            forwarded = update.message.forward(chat_id=speaker_chat_id)
            if not forwarded.forward_from:
                context.bot.send_message(
                        chat_id=speaker_chat_id,
                        reply_to_message_id=forwarded.message_id,
                        text=f'{update.message.from_user.id}'
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

# Финалочка