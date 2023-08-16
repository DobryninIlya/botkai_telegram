import random
from datetime import date

from ..BotClasses import Command as command_class, traceback
from ..BotClasses import User, Message, StudentShedule, Keyboards, connection, cursor
from ..BotClasses.ExportShedule import ExportShedule
from clients.tg.api import TgClient

def start_of_school_year():
    today = date.today()
    if today.month >= 8:
        return date(today.year, 9, 1)
    else:
        return date(today.year - 1, 9, 1)


async def processor(user: User, message: Message, tg_client: TgClient, callback_query=False, stage=None):
    if message.button == 'drop_groups_new_year':
        print("ОЧИСТКА НОМЕРОВ ГРУПП СТАРОГО УЧЕБНОГО ГОДА")
        sql = "UPDATE tg_users SET groupid = 0".format(start_of_school_year())
        cursor.execute(sql)
        connection.commit()
        await tg_client.send_message(user.id, "ОЧИСТКА НОМЕРОВ ГРУПП СТАРОГО УЧЕБНОГО ГОДА ПРОИЗВЕДЕНА", parse_mode=True)

    return


command = command_class()

command.keys = ["drop_groups_new_year"]
command.process = processor
command.role = [1]
command.payload = ['drop_groups_new_year']
command.admlevel = 50