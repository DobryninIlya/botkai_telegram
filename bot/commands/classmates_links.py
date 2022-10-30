import json
import random

import aiohttp

from ..BotClasses import Command as command_class, traceback
from ..BotClasses import User, Message
from ..BotClasses.Keyboards import keyboard
from ..BotClasses.Stage_handler import Stage
from ..BotClasses.DB_values import Value
from ..BotClasses.Database_connection import cursor
from clients.tg.api import TgClient
from bs4 import BeautifulSoup



async def processor(user: User, message: Message, tg_client: TgClient, callback_query=False, stage=None):
    sql = 'SELECT * FROM tg_users WHERE groupid = {}'.format(user.group_id)
    cursor.execute(sql)
    query_result = cursor.fetchall()
    result = ""
    i = 1
    for row in query_result:
        result += "{}. [{} {}](tg://user?id={}) \n".format(i, row[1].rstrip(), row[2].rstrip(), row[0])
        i+=1
    await tg_client.send_message(user.id, result, parse_mode="Markdown")
    return



command = command_class()

command.keys = ["ссылки на одногруппников"]
command.process = processor
command.role = [1, 2, 3, 4]
command.payload = ['classmates_links']
