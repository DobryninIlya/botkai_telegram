import random

from ..BotClasses import Command as command_class, traceback
from ..BotClasses import User, Message
from ..BotClasses.Keyboards import keyboard
from ..BotClasses.Stage_handler import Stage
from clients.tg.api import TgClient


async def processor(user: User, message: Message, tg_client: TgClient, callback_query=False, stage=None):
    stage = Stage(user, message)
    if message.text.lower() == 'обратная связь':
        msg = "Здесь ты можешь задать свой вопрос, предложить улучшение для бота \
    или сообщить об ошибке. Учтите, что принимаются вопросы ТОЛЬКО по вопросом, касательно работы чат-бота. \
    Я не отвечаю на вопросы, связанные с учебным процессом, я не знаю какая у вас группа и режим работы Здравпункта. \
    Не тратьте свое и мое время - воспользуйтесь гуглом google.com . Нажми на кнопку продолжить, чтобы сделать обращение"
        await tg_client.send_message(user.id, msg, buttons=keyboard('feedback_create', user).get_inline_keyboard())
        return
    elif message.button == 'feedback_create':
        msg = 'Введите текст вопроса. \n(медиафайлы временно не поддерживаются)'
        stage._set_status(110)
        await tg_client.send_message(user.id, msg, buttons=keyboard('exit', user).get_keyboard())
    elif stage.status == 110:
        feedback_msg = message.text
        if len(feedback_msg) > 500:
            pass
        print(feedback_msg)
    return


command = command_class()

command.keys = ["обратная связь"]
command.process = processor
command.role = [1, 2, 3, 4]
command.payload = ['feedback_create']
command.status_list = [110]