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
    stage = Stage(user, message)
    if message.text.lower() == 'обратная связь':
        msg = "Здесь ты можешь задать свой вопрос, предложить улучшение для бота \
или сообщить об ошибке. Учтите, что принимаются вопросы ТОЛЬКО по вопросом, касательно работы чат-бота. \
Я не отвечаю на вопросы, связанные с учебным процессом, я не знаю какая у вас группа и режим работы Здравпункта. \
Не тратьте свое и мое время - воспользуйтесь гуглом google.com . Нажми на кнопку продолжить, чтобы сделать обращение"
        await tg_client.send_message(user.id, msg, buttons=keyboard('feedback_create', user).get_inline_keyboard())
        return
    elif message.button == 'feedback_create':
        msg = 'Введите текст вопроса. \nПрикрепляйте только фотографии с галочкой "Сжать фотографии"'
        stage._set_status(110)
        await tg_client.send_message(user.id, msg, buttons=keyboard('exit', user).get_keyboard())
    elif message.button == 'answer_feedback':
        msg = 'Введите ответ\n'
        stage._set_status(111)
        value = Value(user, message)
        user_anwser_id = json.loads(message.data)['user_id']
        value.save_id_to_answer(user_anwser_id)
        await tg_client.send_message(user.id, msg, buttons=keyboard('exit', user).get_keyboard())

    elif stage.status == 110:
        if message.media_group_id and message.media_group_id in media_group_id_list:
            return
        else:
            media_group_id_list.append(message.media_group_id)
        feedback_msg = message.text
        if len(feedback_msg) > 500:
            msg = 'Сообщение слишком длинное.'
            await tg_client.send_message(user.id, msg, buttons=keyboard('main_keyboard', user).get_keyboard())
            return
        from_username = "@" + user.username + "\n"
        msg = message.text if message.text else '[без подписи]'
        await tg_client.send_message(_admin_id, from_username + msg, buttons=keyboard('answer_for_feedback', user,
                                                                                      payload=str(
                                                                                          user.id)).get_inline_keyboard())
        await tg_client.send_media_group(_admin_id, message.attachments)
        stage._set_status(0)
        msg = 'Сообщение отправлено администратору'
        await tg_client.send_message(user.id, msg, buttons=keyboard('main_keyboard', user).get_keyboard())
        return
    elif stage.status == 111:
        if message.media_group_id and message.media_group_id in media_group_id_list:
            return
        feedback_msg = message.text
        from_username = "Ответ от администратора: \n"
        msg = message.text if message.text else '[без подписи]'
        value = Value(user, message)
        user_id = value.get_user_to_answer()
        await tg_client.send_message(user_id, from_username + msg)
        await tg_client.send_media_group(user_id, message.attachments)
        stage._set_status(0)
        msg = 'Сообщение отправлено пользователю'
        await tg_client.send_message(user.id, msg, buttons=keyboard('main_keyboard', user).get_keyboard())
        await tg_client.send_media_group(_admin_id, message.attachments)
    return


command = command_class()

command.keys = ["обратная связь"]
command.process = processor
command.role = [1, 2, 3, 4]
command.payload = ['feedback_create', 'answer_feedback']
command.status_list = [110, 111]
