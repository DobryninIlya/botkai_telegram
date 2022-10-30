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
    msg = 'Поддержи разработчика донатом! Это поможет развивать экосистему бота и делать его более удобным для использования. ' \
          'Помни - бот существует только от поддержки подписчиков.'
    await tg_client.send_message(user.id, msg, buttons=keyboard('donate_link', user).get_link())
    return


command = command_class()

command.keys = ["донат", 'поддержать проект', 'donate']
command.process = processor
command.role = [1, 2, 3, 4]
command.payload = ['donate']
