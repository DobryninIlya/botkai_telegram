import json
import random

from ..BotClasses import Command as command_class, traceback
from ..BotClasses import User, Message
from ..BotClasses.Keyboards import keyboard
from ..BotClasses.Stage_handler import Stage
from ..BotClasses.DB_values import Value
from clients.tg.api import TgClient


async def processor(user: User, message: Message, tg_client: TgClient, callback_query=False, stage=None):
    if message.text.lower() == 'разное':
        await tg_client.send_message(user.id, 'Разное', buttons=keyboard('other_functions', user).get_inline_keyboard())
    return


command = command_class()

command.keys = ["разное"]
command.process = processor
command.role = [1, 2]
command.payload = []
