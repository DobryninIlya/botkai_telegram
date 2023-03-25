import random
import datetime as dt
from ..BotClasses import Command as command_class, traceback
from ..BotClasses import User, Message, StudentShedule
from ..BotClasses.Keyboards import keyboard
from ..BotClasses.Stage_handler import Stage
from clients.tg.api import TgClient
from ..BotClasses.Database_connection import cursor, connection

def check_users_rent(tg_user:int):
    sql = f"SELECT COUNT(*) FROM coworking_rent WHERE tg_user={tg_user}"
    cursor.execute(sql)
    result = cursor.fetchone()
    if result == None:
        return 0
    return result

def delete_users_rents(tg_user:int):
    sql = f"DELETE FROM coworking_rent WHERE tg_user={tg_user}"
    cursor.execute(sql)
    connection.commit()

def check_rents_count(date:dt.date):
    cursor.execute("SELECT COUNT(*) FROM coworking_rent WHERE date='%s' AND status in (0,1,2)" % date)
    result = cursor.fetchone()
    if result == None:
        return 0
    return result[0]

def get_my_rent(tg_user):
    cursor.execute(f"""SELECT cow.date, cow.time, s.name 
                   FROM coworking_rent cow JOIN rent_status s ON cow.status = s.id 
                   WHERE cow.tg_user = {tg_user}""")
    res = cursor.fetchone()
    if res == None:
        return "Брони не найдено"
    res = f"===ВАША БРОНЬ===\n{res[0].strftime('%a: %d-%m-%Y')} {res[1].strftime('%H:%M')}\nСтатус: {res[2].rstrip()}"
    return res

async def processor(user: User, message: Message, tg_client: TgClient, callback_query=False, stage=None):
    msg = "Выберите дату:"
    if message.button == 'coworking_rent':
        if check_users_rent(user.id) != 0:
            delete_users_rents(user.id)
            msg = "(Ваше предыдущее бронирование было удалено)\n Выберите дату:"
        await tg_client.edit_message(user.id, message.message_id, keyboard('coworking_rent_date', user).get_inline_keyboard(), msg)
        # await tg_client.send_message(user.id, msg, buttons=keyboard('coworking_rent_date', user).get_inline_keyboard())
    elif message.button == 'coworking_setdate':
        date = message.button_data
        if check_rents_count(date) > 30:
            msg = "Данный день загружен полностью. Выберите другую дату"
            await tg_client.edit_message(user.id, message.message_id, keyboard('coworking_rent_date', user).get_inline_keyboard(), msg)
            return
        try:
            sql = f"INSERT INTO coworking_rent (tg_user, status, date, time) VALUES ({user.id}, 0, '{date}', '00:00:00')"
            cursor.execute(sql)
            connection.commit()
        except:
            print(sql)
            print('Ошибка:\n', traceback.format_exc(), flush=True)
            msg = "Данное действие не разрешено"
            await tg_client.edit_message(user.id, message.message_id,
                                         keyboard('coworking_rent_date', user).get_inline_keyboard(), msg)
            return

        msg = "Выбрана дата: " + date + "\nВыберите час:"
        await tg_client.edit_message(user.id, message.message_id, keyboard('coworking_rent_time', user).get_inline_keyboard(), msg)
        return
    elif message.button == 'coworking_settime':
        sql = f"UPDATE coworking_rent SET time='{message.button_data}:00:00' WHERE tg_user={user.id}"
        cursor.execute(sql)
        connection.commit()
        msg = f"Выбран час: {message.button_data}\nВыберите минуты:"
        await tg_client.edit_message(user.id, message.message_id, keyboard('coworking_rent_time_minute', user).get_inline_keyboard(), msg)
    elif message.button == 'coworking_rent_time_minute':
        sql = f"SELECT time, date FROM coworking_rent WHERE tg_user={user.id}"
        cursor.execute(sql)
        result = cursor.fetchone()
        time = result[0]
        date = result[1]
        result = dt.datetime.combine(date.today(), time) + dt.timedelta(minutes=int(message.button_data))
        time = result.time()
        # time += dt.timedelta(minutes=int(message.button_data))
        # time = time[0,2] + ":" + message.button_data + ":00"
        sql = f"UPDATE coworking_rent SET time='{time}', status=1 WHERE tg_user={user.id}"
        cursor.execute(sql)
        connection.commit()
        msg = f"Ваша заявка создана!\nДата: {date} \n Время: {time}"
        await tg_client.edit_message(user.id, message.message_id,
                                     keyboard('coworking_main', user).get_inline_keyboard(), msg)
    elif message.button == 'coworking_rent_event':
        pass

    elif message.button == 'coworking_rent_my':
        msg = get_my_rent(user.id)
        await tg_client.edit_message(user.id, message.message_id,
                                     keyboard('coworking_main', user).get_inline_keyboard(), msg)

    elif message.button == 'coworking_main':
        msg = """Коворкинг работает в будни с 9:00 до 17:00 в будние дни. 
                    В выходные и праздничные дни возможности забронировать место нет.
                    Также вы можете согласовать проведения мероприятия в любой удобный день.
                    * Информация может быть дополнена
                    """
        await tg_client.edit_message(user.id, message.message_id,
                                     keyboard('coworking_main', user).get_inline_keyboard(), msg)
    else:
        msg = """Коворкинг работает в будни с 9:00 до 17:00 в будние дни. 
            В выходные и праздничные дни возможности забронировать место нет.
            Также вы можете согласовать проведения мероприятия в любой удобный день.
            * Информация может быть дополнена
            """
        answer = await tg_client.send_message(user.id, msg, buttons=keyboard('coworking_main', user).get_inline_keyboard())


    return


command = command_class()

command.keys = ["коворкинг", 'бронирование коворкинга']
command.process = processor
command.role = [1, 2, 5]
command.payload = ['coworking_rent', 'coworking_rent_event', 'coworking_setdate', 'coworking_settime', 'coworking_rent_time_minute', 'coworking_rent_my', 'coworking_main']
command.status_list = [500]
