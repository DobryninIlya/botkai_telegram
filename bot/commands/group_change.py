import datetime

from ..BotClasses import Command as command_class, traceback
from ..BotClasses import User, Message, StudentShedule
from ..BotClasses.Keyboards import keyboard
from ..BotClasses.GroupChange import GroupChange
from ..BotClasses.Stage_handler import Stage
from clients.tg.api import TgClient


async def processor(user: User, message: Message, tg_client: TgClient, callback_query=False, stage=None):
    status = stage.status
    if not status:
        if message.button == 'group_change_commit':
            await tg_client.send_message(user.id, 'Введи номер группы',
                                         buttons=keyboard('exit', user).get_keyboard())
            stage._set_status(101)
            return
        await tg_client.send_message(user.id, 'Хочешь изменить номер группы?',
                                     buttons=keyboard('group_change', user).get_inline_keyboard())
        return
    if status == 101:
        result, msg = await GroupChange(message.text, user).processing()
        if result:
            await tg_client.send_message(user.id, msg, buttons=keyboard('main_keyboard', user).get_keyboard())
            stage._set_status(0)
            return
        await tg_client.send_message(user.id, msg)


command = command_class()

command.keys = ['изменить группу', 'сменить группу', 'изменить номер группы']
command.process = processor
command.role = [1]
command.payload = ['groupchange', 'group_change_commit']
command.status_list = [101]