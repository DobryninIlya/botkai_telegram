import random

from ..BotClasses import Command as command_class, traceback
from ..BotClasses import User, Message, Stage_handler
from clients.tg.api import TgClient


async def processor(user: User, message: Message, tg_client: TgClient):
    Stage_handler.Stage(user, message, tg_client)._set_status(101)
    return


command = command_class()

command.keys = ["обратная связь"]
command.process = processor
command.role = [1]
