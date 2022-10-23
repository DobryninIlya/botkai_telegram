import random

from ..BotClasses import Command as command_class, traceback
from ..BotClasses import User, Message, StudentShedule
from ..BotClasses.Keyboards import keyboard
from clients.tg.api import TgClient


async def processor(user: User, message: Message, tg_client: TgClient, callback_query=False):
    await tg_client.send_message(user.id, 'Главное меню', buttons=keyboard('main_keyboard', user).get_keyboard())
    await tg_client.answer_callback_query(message.callback_query_id)
    return


command = command_class()

command.keys = []
command.process = processor
command.role = [1]
command.payload = ['exit', 'main_menu', 'выход']