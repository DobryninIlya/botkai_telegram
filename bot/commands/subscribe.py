import random

from ..BotClasses import Command as command_class, traceback
from ..BotClasses import User, Message, StudentShedule
from ..BotClasses.Keyboards import keyboard
from ..BotClasses.Stage_handler import Stage
from clients.tg.api import TgClient

button_template = [[['Открыть', '']]]

app = "https://t.me/knrtukaibot/subscribe?startapp=client_id%3Dtg{}"
async def processor(user: User, message: Message, tg_client: TgClient, callback_query=False, stage=None):
    button = button_template
    button[0][0][1] = app.format(user.id)
    await tg_client.send_message(user.id, 'Для поддержки разработчика перейдите по ссылке ниже', buttons=keyboard('attestation', user, buttons=button).get_link())
    return


command = command_class()

command.keys = ['подписка', 'платная подписка']
command.process = processor
command.role = [1]
command.payload = ['subscribe']