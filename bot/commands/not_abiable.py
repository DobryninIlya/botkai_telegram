import random

from ..BotClasses import Command as command_class, traceback
from ..BotClasses import User, Message, StudentShedule, Keyboards
from clients.tg.api import TgClient


async def processor(user: User, message: Message, tg_client: TgClient):
    msg = '💤💤💤 Данная команда временно недоступна ⛔'
    await tg_client.send_message(user.id, msg, buttons=Keyboards.main_keyboard)
    return


command = command_class()

command.keys = ["задания и объявления",
                "разное",
                "обратная связь", "профиль"
                ]
command.process = processor
command.role = [1]
