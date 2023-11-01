import json
import random

from ..BotClasses import Command as command_class, traceback
from ..BotClasses import User, Message
from ..BotClasses.Keyboards import keyboard
from ..BotClasses.Stage_handler import Stage
from ..BotClasses.DB_values import Value
from clients.tg.api import TgClient

_admin_id = 393867797
media_group_id_list = []


async def processor(user: User, message: Message, tg_client: TgClient, callback_query=False, stage=None):
    msg = 'У нас есть прикольный чат со студентами. Там точно не будет преподавателей и других посторонних. ' \
          'Только ты и другие студенты'
    await tg_client.send_message(user.id, msg, buttons=keyboard('invite_to_chat', user).get_link())
    return


command = command_class()

command.keys = ["чат студентов", 'беседа']
command.process = processor
command.role = [1]
command.payload = ['chat']
