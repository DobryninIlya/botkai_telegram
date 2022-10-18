import random

from ..BotClasses import Command as command_class, traceback
from ..BotClasses import User, Message, StudentShedule
from ..BotClasses.Keyboards import keyboard
from clients.tg.api import TgClient


async def processor(user: User, message: Message, tg_client: TgClient, callback_query=False):
    msg = '⛔ Данная команда временно недоступна 💤💤💤'
    await tg_client.send_message(user.id, msg, buttons=keyboard('main_keyboard', user).get_keyboard())
    return


command = command_class()

command.keys = ["задания и объявления",
                "разное",
                'пожертвования', 'донат'
                ]
command.process = processor
command.role = [1]
