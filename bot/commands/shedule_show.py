import random

from ..BotClasses import Command as command_class, traceback
from ..BotClasses import User, Message, StudentShedule
from ..BotClasses.Keyboards import keyboard
from clients.tg.api import TgClient


frazi = ["Можно сходить в кино 😚", "Можно почитать 😚", "Можно прогуляться в лесу 😚",
         "Можно распланировать дела на неделю 😚", "Можно заняться спортом, например. 😚",
         "Можно вспомнить строчки гимна КАИ 😚", "Можно заняться чем то интересным 😚",
         "Можно встретиться с друзьями 😚"]


async def processor(user: User, message: Message, tg_client: TgClient, callback_query=False, stage=None):
    day_count = 0
    text = message.text.lower()
    day_week = ''
    if text in ['на завтра', 'расписание на завтра', 'завтра', 'tomorrow']:
        day_week = "Завтра"
        day_count = 1
    elif text in ['на сегодня', 'расписание на сегодня', 'сегодня', 'today']:
        day_week = "Сегодня"
        day_count = 0
    elif text in ['на послезавтра', 'расписание на послезавтра', 'послезавтра', 'afterday']:
        day_week = "Послезавтра"
        day_count = 2
    elif text in ['полностью', 'расписание полностью', 'shedule']:
        day_week = "всю неделю"
        day_count = -1
    elif text in ['преподаватели', 'мои преподаватели', 'преподы']:
        day_count = -2
    elif text in ['четность', 'какая неделя', 'какая сейчас неделя', 'четность недели']:
        day_count = -3
    shedule = await StudentShedule(user, message).showTimetable(user.group_id, day_count)
    if day_count == -3:
        msg = 'Четная' if shedule else 'Нечетная'
        await tg_client.send_message(user.id, msg, buttons=keyboard('main_keyboard', user).get_keyboard())
        return
    if shedule:
        try:
            if day_count == -2:
                msg = "Список преподавателей:\n{}".format(shedule[:3000])
            else:
                msg = "Расписание на {}\n {}".format(day_week.lower(), shedule[:3000])
            await tg_client.send_message(user.id, msg, buttons=keyboard('main_keyboard', user).get_keyboard())
        except:
            print('Ошибка:\n', traceback.format_exc())
    else:
        msg = day_week + ' занятий нет 😎\n' + frazi[random.randint(0, len(frazi) - 1)]
        await tg_client.send_message(user.id, msg, buttons=keyboard('main_keyboard', user).get_keyboard())
    return


command = command_class()

command.keys = ['на завтра', 'расписание на завтра', 'завтра', 'tomorrow',
                'на сегодня', 'расписание на сегодня', 'сегодня', 'today',
                'на послезавтра', 'расписание на послезавтра', 'послезавтра', 'afterday',
                'полностью', 'расписание полностью', 'shedule',
                'преподаватели', 'мои преподаватели', 'преподы',
                'четность', 'какая неделя', 'какая сейчас неделя', 'четность недели'
                ]
command.process = processor
command.role = [1]
