import random

from ..BotClasses import Command as command_class, traceback
from ..BotClasses import User, Message, StudentShedule, keyboard, connection, cursor
from clients.tg.api import TgClient

msg = "Ваш статус оповещения об изменениях в расписании: *{}*. \nХотите изменить?"
msg_changed = "Статус оповещения изменен на: *{}*"

async def processor(user: User, message: Message, tg_client: TgClient, callback_query=False, stage=None):
    cursor.execute("SELECT schedule_change FROM notify_clients WHERE destination_id = {dId} AND source = '{source}'".format(
        dId=user.id,
        source="tg"
    ))
    result_query = cursor.fetchone()
    if result_query == None:
        cursor.execute("INSERT INTO notify_clients (id, destination_id, schedule_change, source) VALUES ("
                       "(SELECT COUNT(*) FROM notify_clients), {id}, true, 'tg');".format(id=user.id))
        result_query = [True]

    flag: bool = result_query[0]
    if message.button == "notifier_change":
        flag = not flag
        cursor.execute(
            "UPDATE notify_clients SET schedule_change = {flag} WHERE destination_id = {dId} AND source = '{source}'".format(
                flag=flag,
                dId=user.id,
                source="tg"
            ))
        connection.commit()
        message_send = msg_changed.format("Активно" if flag else "Неактивно")
        # await tg_client.send_message(user.id, message_send, buttons=keyboard('notifier_change', user).get_inline_keyboard(), parse_mode=True)
        await tg_client.edit_message(user.id, message.message_id, message=message_send,buttons=keyboard('notifier_change', user).get_inline_keyboard(), parse_mode=True)
        return
    message_send = msg.format("Активно" if flag else "Неактивно")
    await tg_client.send_message(user.id, message_send, buttons=keyboard('notifier_change', user).get_inline_keyboard(), parse_mode=True)
    return


command = command_class()

command.keys = ["изменить оповещения", "оповещения изменить", "изменения в расписании", "управление оповещениями"]
command.process = processor
command.role = [1]
command.payload = ["notifier_change"]
