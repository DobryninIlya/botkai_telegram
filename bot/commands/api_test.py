import random

from ..BotClasses import Command as command_class, traceback
from ..BotClasses import User, Message, StudentShedule, Keyboards
from clients.tg.api import TgClient


async def processor(user: User, message: Message, tg_client: TgClient):
    print(await tg_client.get_chat_member(user.id))
    return


command = command_class()

command.keys = ["test"]
command.process = processor
command.role = [1]
