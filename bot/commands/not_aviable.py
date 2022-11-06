import random

from ..BotClasses import Command as command_class, traceback
from ..BotClasses import User, Message, StudentShedule
from ..BotClasses.Keyboards import keyboard
from clients.tg.api import TgClient


async def processor(user: User, message: Message, tg_client: TgClient, callback_query=False, stage=None):
    msg = '⛔ Данная команда временно недоступна 💤💤💤'
    if message.text.lower() in ["задания и объявления", 'стать старостой']:
        msg = 'Данная команда более не поддерживается в связи ее непопулярностью'
    await tg_client.send_message(user.id, msg, buttons=keyboard('main_keyboard', user).get_keyboard())
    return


command = command_class()

command.keys = ["задания и объявления", 'пожертвования', 'график посещения занятий (для старосты)', 'баллы брс']
command.process = processor
command.role = [1]
command.payload = ['group_members', 'my_groups_list', 'my_faculty']
