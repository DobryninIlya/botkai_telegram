import random

from ..BotClasses import Command as command_class, traceback
from ..BotClasses import User, Message, Stage_handler
from ..BotClasses.Keyboards import keyboard
from clients.tg.api import TgClient


async def processor(user: User, message: Message, tg_client: TgClient, callback_query=False):
    # Stage_handler.Stage(user, message, tg_client)._set_status(101)
    msg = "Здесь ты можешь задать свой вопрос, предложить улучшение для бота \
или сообщить об ошибке. Учтите, что принимаются вопросы ТОЛЬКО по вопросом, касательно работы чат-бота. \
Я не отвечаю на вопросы, связанные с учебным процессом, я не знаю какая у вас группа и режим работы Здравпункта. \
Не тратьте свое и мое время - воспользуйтесь гуглом google.com . Нажми на кнопку продолжить, чтобы сделать обращение"
    await tg_client.send_message(user.id, msg, buttons=keyboard('feedback_create', user).get_inline_keyboard())
    return


command = command_class()

command.keys = ["обратная связь"]
command.process = processor
command.role = [1, 2, 3, 4]
command.payload = 'feedback_create'
