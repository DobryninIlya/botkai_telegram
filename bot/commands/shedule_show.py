import random
import datetime
from ..BotClasses import Command as command_class, traceback
from ..BotClasses import User, Message, StudentShedule
from ..BotClasses.Keyboards import keyboard
from clients.tg.api import TgClient


frazi = ["Можно сходить в кино 😚", "Можно почитать 😚", "Можно прогуляться в лесу 😚",
         "Можно распланировать дела на неделю 😚", "Можно заняться спортом, например. 😚",
         "Можно вспомнить строчки гимна КАИ 😚", "Можно заняться чем то интересным 😚",
         "Можно встретиться с друзьями 😚"]


def getWeekDayNum(day):
    today = datetime.date.today()
    current_day = today.isoweekday()
    date_day = 0
    if day < current_day:
        date_day = 7 - current_day + day
    elif day == current_day:
        date_day = 7
    else:
        date_day = day - current_day
    return date_day

week = {
    1: 'Понедельник',
    2: 'Вторник',
    3: 'Среда',
    4: 'Четверг',
    5: 'Пятница',
    6: 'Суббота',
    7: 'Воскресенье'
}

async def groupid_assert(user: User, tg_client: TgClient):
    if user.group_id == 0:
        await tg_client.send_message(user.id, "*Номер вашей группы установлен в прошлом году.*", buttons=keyboard('group_change', user).get_inline_keyboard(), parse_mode=True)
        return False
    return True
async def processor(user: User, message: Message, tg_client: TgClient, callback_query=False, stage=None):
    day_count = 0
    text = message.text.lower()
    day_week = ''
    if not await groupid_assert(user, tg_client):
        return
    getWeekDayNum(1)
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
    elif text in ['по дням', 'понедельник', 'вторник', 'среда', 'четверг', 'пятница', 'суббота']:
        msg = 'По дням недели'
        await tg_client.send_message(user.id, msg, buttons=keyboard('week_shedule', user).get_inline_keyboard(),
                                     parse_mode=True)
        return
    elif message.button == 'shed_week':
        day = int(message.button_data)
        msg = f"_Расписание на_ *{week[day].lower()}*\n"
        day_count = getWeekDayNum(day)
        shedule = await StudentShedule(user, message, tg_client).showTimetable(user.group_id, day_count)
        msg += shedule if shedule else "Занятий нет"
        await tg_client.edit_message(user.id, message.message_id,
                                     keyboard('week_shedule', user).get_inline_keyboard(), msg, parse_mode=True)
        return
    shedule = await StudentShedule(user, message, tg_client).showTimetable(user.group_id, day_count)
    if day_count == -3:
        msg = 'Четная' if shedule else 'Нечетная'
        await tg_client.send_message(user.id, msg, buttons=keyboard('main_keyboard', user).get_keyboard(), parse_mode=True)
        return
    if shedule:
        try:
            if day_count == -2:
                msg = "Список преподавателей:\n{}".format(shedule[:3000])
                await tg_client.send_message(user.id, msg, buttons=keyboard('main_keyboard', user).get_keyboard(), parse_mode=True)
            else:
                separator = "═──────Четверг────────═"
                shedule_parts = shedule.split(separator, 1)  # Разделяем расписание на две части по разделителю

                # Первая часть расписания (до разделителя) отправляется в первом сообщении
                msg = "Расписание на {}\n {}".format(day_week.lower(), shedule_parts[0])
                await tg_client.send_message(user.id, msg, buttons=keyboard('main_keyboard', user).get_keyboard(), parse_mode=True)

                # Вторая часть расписания (после разделителя) отправляется во втором сообщении
                if len(shedule_parts) > 1:  # Если есть вторая часть расписания
                    await tg_client.send_message(user.id, separator + shedule_parts[1],
                                                 buttons=keyboard('main_keyboard', user).get_keyboard(), parse_mode=True)
        except:
            print('Ошибка:\n', traceback.format_exc())
    else:
        msg = day_week + ' занятий нет 😎\n' + frazi[random.randint(0, len(frazi) - 1)]
        await tg_client.send_message(user.id, msg, buttons=keyboard('main_keyboard', user).get_keyboard(), parse_mode=True)
    return


command = command_class()

command.keys = ['на завтра', 'расписание на завтра', 'завтра', 'tomorrow',
                'на сегодня', 'расписание на сегодня', 'сегодня', 'today',
                'на послезавтра', 'расписание на послезавтра', 'послезавтра', 'afterday',
                'полностью', 'расписание полностью', 'shedule',
                'преподаватели', 'мои преподаватели', 'преподы',
                'четность', 'какая неделя', 'какая сейчас неделя', 'четность недели',
                'по дням', 'понедельник', 'вторник', 'среда', 'четверг', 'пятница', 'суббота'
                ]
command.process = processor
command.role = [1]
command.payload = ['shed_week']
