import random

from ..BotClasses import Command as command_class, traceback
from ..BotClasses import User, Message, StudentShedule
from ..BotClasses.Keyboards import keyboard
from ..BotClasses.Stage_handler import Stage
from clients.tg.api import TgClient

button_template = [[['Открыть', '']]]

app = "https://t.me/knrtukaibot/exams?startapp=groupid%3D{}"
async def processor(user: User, message: Message, tg_client: TgClient, callback_query=False, stage=None):
    button = button_template
    button[0][0][1] = app.format(user.group_id)
    await tg_client.send_message(user.id, 'Твои экзамены:', buttons=keyboard('attestation', user, buttons=button).get_link())
    await tg_client.answer_callback_query(message.callback_query_id)
    return


command = command_class()

command.keys = ['экзамены', 'сессия']
command.process = processor
command.role = [1]
command.payload = ['exams']