import random

from ..BotClasses import Command as command_class, traceback
from ..BotClasses import User, Message, StudentShedule, Keyboards
from ..BotClasses.ExportShedule import ExportShedule
from clients.tg.api import TgClient


async def processor(user: User, message: Message, tg_client: TgClient, callback_query=False, stage=None):
    export = ExportShedule(user, message, tg_client)
    ics_export = await export.makeFile(2)
    await tg_client.send_message(user.id, "Данный функционал здесь более не поддерживается. Ожидайте эту функцию в КапиПаре capypara.kai.ru", parse_mode=True)
    return
    if not ics_export:
        await tg_client.send_message(user.id, "*Ошибка!*\n_Расписание не обнаружено_", parse_mode=True)
    if message.button == 'export_ics':
        ics_export = await export.makeFile(2)
        print(await tg_client.send_document(user.id, ics_export, caption='Расписание для календаря', filename='PersonalTimetable.ics'))
    elif message.button == 'export_word':
        ics_export = await export.createDocShedule()
        with open(ics_export, 'rb') as file:
            await tg_client.send_document(user.id, file, caption='Расписание в формате документа MS Word', filename='PersonalTimetable.docx')
    return


command = command_class()

command.keys = ["export icalendar", 'экспорт в календарь', 'word документ']
command.process = processor
command.role = [1]
command.payload = ['export_ics', 'export_word', 'export_entries_control']