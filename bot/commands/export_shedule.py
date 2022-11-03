import random

from ..BotClasses import Command as command_class, traceback
from ..BotClasses import User, Message, StudentShedule, Keyboards
from ..BotClasses.ExportShedule import ExportShedule
from clients.tg.api import TgClient


async def processor(user: User, message: Message, tg_client: TgClient, callback_query=False, stage=None):
    export = ExportShedule(user, message)
    ics_export = await export.makeFile(2)
    print(ics_export)
    print(await tg_client.send_document(user.id, ics_export, caption='Расписание для календаря'))
    return


command = command_class()

command.keys = ["export icalendar"]
command.process = processor
command.role = [1]
