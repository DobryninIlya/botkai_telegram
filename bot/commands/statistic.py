import random

from ..BotClasses import Command as command_class, traceback
from ..BotClasses import User, Message, StudentShedule, Keyboards, statistic_updates, statistic_users_active
from clients.tg.api import TgClient


async def processor(user: User, message: Message, tg_client: TgClient, callback_query=False, stage=None):
    msg = f'Пользователей активно: {message.cmd_payload[0]}\nОбращений к боту: {message.cmd_payload[1]}'
    await tg_client.send_message(user.id, msg)
    return


command = command_class()

command.keys = ["stat"]
command.process = processor
command.role = [1]
command.admlevel = 2
############# add admin verification
