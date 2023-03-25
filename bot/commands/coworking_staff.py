import random
import datetime as dt
from ..BotClasses import Command as command_class, traceback
from ..BotClasses import User, Message, StudentShedule
from ..BotClasses.Keyboards import keyboard
from ..BotClasses.Stage_handler import Stage
from clients.tg.api import TgClient
from ..BotClasses.Database_connection import cursor, connection

def get_last_rent():
    sql = """SELECT * 
    FROM coworking_rent 
    WHERE status = 1 LIMIT 1
    """
    cursor.execute(sql)
    res = cursor.fetchone()
    return res

def set_rent_status(status:int):
    sql = f"UPDATE coworking_rent SET status = {status} WHERE"

def get_rents(day):
    msg = ""
    sql = f"SELECT c.id, c.tg_user, c.status, c.date, c.time, " \
          f"COALESCE(u.username, ''), COALESCE(u.name, '') , COALESCE(u.lastname, '') " \
          f"FROM coworking_rent c LEFT JOIN tg_users u ON u.id = c.tg_user WHERE status = 2 AND date='{day}'"
    cursor.execute(sql)
    res = cursor.fetchall()
    if res == []:
        return f"Записей на {day} не найдено"
    for rent in res:
        msg += "====RENT====\n"
        msg += f"ID:{rent[0]} | USER_ID: {rent[1]}\n {'@' + rent[5].rstrip() if rent[5].rstrip() else ''} {rent[6].rstrip()} {rent[7].rstrip()}\n{rent[3]}, {rent[4]}\n ============== \n"
    return msg


def get_rents_week(start, finish):
    msg = ""
    sql = f"SELECT c.id, c.tg_user, c.status, c.date, c.time, " \
          f"COALESCE(u.username, ''), COALESCE(u.name, '') , COALESCE(u.lastname, '') " \
          f"FROM coworking_rent c LEFT JOIN tg_users u ON u.id = c.tg_user WHERE status = 2 AND date BETWEEN '{start}' AND '{finish}'"
    cursor.execute(sql)
    res = cursor.fetchall()
    if res == []:
        return f"Записей на {start} -> {finish} не найдено"
    for rent in res:
        msg += "====RENT====\n"
        msg += f"ID:{rent[0]} | USER_ID: {rent[1]}\n {'@' + rent[5].rstrip() if rent[5].rstrip() else ''} {rent[6].rstrip()} {rent[7].rstrip()}\n{rent[3]}, {rent[4]}\n ============== \n"
    return msg

async def processor(user: User, message: Message, tg_client: TgClient, callback_query=False, stage=None):
    if message.button == 'coworking_accept':
        rents = get_last_rent()
        msg = "====RENT====\n"
        id = 0
        if rents == None:
            msg = "Все заявки обработаны."
        else:
            msg += f"ID:{id} | USER_ID: {rents[1]}\n {rents[3]}, {rents[4]}"
            id = rents[0]
        await tg_client.edit_message(user.id, message.message_id, keyboard('coworking_rent_accept', user, payload=id).get_inline_keyboard(), msg)
    elif message.button == 'rent_accept':
        sql = f"UPDATE coworking_rent SET status = 2 WHERE id={message.button_data}"
        cursor.execute(sql)
        connection.commit()
        sql = f"SELECT tg_user FROM coworking_rent WHERE id={message.button_data} ORDER BY date DESC LIMIT 1"
        cursor.execute(sql)
        result = cursor.fetchone()[0]
        accept_message = "Ваша заявка на коворкинг одобрена"
        await tg_client.send_message(result, accept_message,
                                     keyboard('coworking_main', user).get_inline_keyboard())
        rents = get_last_rent()
        msg = "====RENT====\n"
        id = 0
        if rents == None:
            msg = "Все заявки обработаны."
        else:
            msg += f"ID:{rents[0]} | USER_ID: {rents[1]}\n {rents[3]}, {rents[4]}"
            id = rents[0]
        await tg_client.edit_message(user.id, message.message_id,
                                     keyboard('coworking_rent_accept', user, payload=id).get_inline_keyboard(),
                                     msg)
    elif message.button == 'rent_decline':
        sql = f"UPDATE coworking_rent SET status = 3 WHERE id={message.button_data}"
        cursor.execute(sql)
        connection.commit()
        sql = f"SELECT tg_user FROM coworking_rent WHERE id={message.button_data} ORDER BY date DESC LIMIT 1"
        cursor.execute(sql)
        result = cursor.fetchone()[0]
        accept_message = "Ваша заявка на коворкинг отклонена"
        await tg_client.send_message(result, accept_message,
                                     keyboard('coworking_main', user).get_inline_keyboard())
        rents = get_last_rent()
        msg = "====RENT====\n"
        id = 0
        if rents == None:
            msg = "Все заявки обработаны."
        else:
            msg += f"ID:{rents[0]} | USER_ID: {rents[1]}\n {rents[3]}, {rents[4]}"
            id = rents[0]
        await tg_client.edit_message(user.id, message.message_id,
                                     keyboard('coworking_rent_accept', user, payload=id).get_inline_keyboard(),
                                     msg)
    elif message.button == 'coworking_staff':
        msg = """staff functions
                    """
        await tg_client.edit_message(user.id, message.message_id, keyboard('coworking_staff', user).get_inline_keyboard(), msg)
    elif message.button == 'coworking_today':
        msg = "===RENTS TODAY====\n"
        msg += get_rents(dt.date.today())
        await tg_client.edit_message(user.id, message.message_id, keyboard('coworking_staff', user).get_inline_keyboard(), msg)
    elif message.button == 'coworking_tomorrow':
        msg = "===RENTS TOMORROW====\n"
        msg += get_rents(dt.date.today() + dt.timedelta(days=1))
        await tg_client.edit_message(user.id, message.message_id, keyboard('coworking_staff', user).get_inline_keyboard(), msg)
    elif message.button == 'coworking_week':
        msg = "===RENTS WEEK====\n"
        msg += get_rents_week(dt.date.today(), dt.date.today()+ dt.timedelta(days=7))
        await tg_client.edit_message(user.id, message.message_id, keyboard('coworking_staff', user).get_inline_keyboard(), msg)
    else:
        msg = """staff functions
            """
        await tg_client.send_message(user.id, msg, buttons=keyboard('coworking_staff', user).get_inline_keyboard())


    return


command = command_class()

command.keys = ["coworking-staff"]
command.process = processor
command.role = [1, 2, 5]
command.payload = ['coworking_accept', 'rent_accept', 'rent_decline', 'coworking_staff', 'coworking_today', 'coworking_tomorrow', 'coworking_week']
command.status_list = []
command.admlevel = 2