import random

from ..BotClasses import Command as command_class, traceback
from ..BotClasses import User, Message, Stage_handler
from ..BotClasses.Keyboards import keyboard
from clients.tg.api import TgClient


async def processor(user: User, message: Message, tg_client: TgClient, callback_query=False, stage=None):
    msg = "Профиль"
    await tg_client.send_message(user.id, msg, buttons=keyboard('profile', user).get_inline_keyboard())
    return


command = command_class()

command.keys = ["профиль"]
command.process = processor
command.role = [1]
