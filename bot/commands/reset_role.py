import random

from ..BotClasses import Command as command_class, traceback
from ..BotClasses import User, Message, Stage_handler, connection, cursor
from ..BotClasses.Keyboards import keyboard
from clients.tg.api import TgClient


async def processor(user: User, message: Message, tg_client: TgClient, callback_query=False, stage=None):
    if message.button == 'reset_role' or message.text.lower() == "сбросить регистрацию":
        msg = "Вы можете сбросить свои настройки и зарегистрироваться заново. Продолжить?"
        await tg_client.send_message(user.id, msg, buttons=keyboard('reset_role_commit', user).get_inline_keyboard())
    elif message.button == 'reset_role_commit':
        cursor.execute("DELETE FROM tg_users WHERE id={id}". format(id=user.id))
        connection.commit()
        msg = "Регистрация сброшена. \n /start"
        await tg_client.send_message(user.id, msg, buttons=keyboard([], user).get_keyboard())
    return


command = command_class()

command.keys = ["сбросить регистрацию"]
command.process = processor
command.role = [1, 2]
command.payload = ['reset_role', 'reset_role_commit']
