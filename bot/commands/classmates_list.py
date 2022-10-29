import json
import random

import aiohttp

from ..BotClasses import Command as command_class, traceback
from ..BotClasses import User, Message
from ..BotClasses.Keyboards import keyboard
from ..BotClasses.Stage_handler import Stage
from ..BotClasses.DB_values import Value
from clients.tg.api import TgClient
from bs4 import BeautifulSoup


async def processor(user: User, message: Message, tg_client: TgClient, callback_query=False, stage=None):
    msg = "Запрос отправлен на обработку"
    await tg_client.send_message(user.id, msg)
    i = 1
    async with aiohttp.ClientSession() as session:
        async with await session.post(
                ("https://kai.ru/infoClick/-/info/group?id={id}").format(id=user.group_id)) as response:
            response = await response.text()
    soup = BeautifulSoup(response, 'lxml')
    list_students = soup.find(id="p_p_id_infoClick_WAR_infoClick10_")
    result = ""
    if not response:
        msg = "Данные не найдены на сайте КАИ."
        await tg_client.send_message(user.id, msg)
    for tag in list_students.find_all("td"):
        if len(tag.text) > 6:
            result += str(i) + ". " + tag.text.strip().replace("\n", "").replace(
                "                                                                Староста", " *(🙋 Староста)*") + "\n"
            i += 1
    await tg_client.send_message(user.id, result, parse_mode="Markdown")
    return



command = command_class()

command.keys = ["одногруппники"]
command.process = processor
command.role = [1, 2, 3, 4]
command.payload = ['classmates_list']
