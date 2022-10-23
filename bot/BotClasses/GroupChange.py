import datetime
import json
import traceback

import aiohttp

from .Database_connection import cursor, connection

from .User import User


async def getGroupsResponse(groupNumber):
    try:
        cursor.execute("SELECT shedule,date_update FROM saved_timetable WHERE groupp = 1")
        result_query = cursor.fetchone()
        result = result_query[0]
        date_update = result_query[1]
        result = json.loads(result)
        for elem in result:
            if int(elem["group"]) == int(groupNumber):
                return elem["id"], date_update
        return False, False
    except:
        return False, False


class GroupChange:
    def __init__(self, group_name, user: User):
        self.group_name = group_name
        self.group_id = None
        self.cursor = cursor
        self.connection = connection
        self.id = user.id

    async def processing(self):
        try:
            group = int(self.group_name)
            if group < 1000 or group > 100000:
                raise AssertionError
            group_id = await self._show_groupId(group)
            if not group_id:
                raise TypeError
        except AssertionError:
            return False, "Ты ввел некорректный номер группы. Повтори ввод номера группы."
        except TypeError:
            return False, "К сожалению, мне не удалось получить параметры твоей группы с сайта...\n" \
                          "Такое бывает, когда на сайт не добавили твою группу, либо номер группы введен не верно. " \
                          "Повтори ввод."
        except:
            return False, "Совсем не могу разобрать что ты ввел! Повтори ввод номера группы."
        self.group_id = await self._show_groupId(self.group_name)
        return self.save_changes()

    def _execute(self, sql_query):
        self.cursor.execute(sql_query)
        self.connection.commit()
        return cursor

    def save_changes(self):
        sql = "UPDATE tg_users SET groupid = {groupid}, groupname = {groupname} WHERE id = {id}".format(
            id=self.id,
            groupname=self.group_name,
            groupid=self.group_id
        )
        self._execute(sql)
        return True, 'Номер группы изменен'

    async def _show_groupId(self, groupNumber):
        BASE_URL = 'https://kai.ru/raspisanie'
        try:
            group, date_update = await getGroupsResponse(groupNumber)
            if not group:
                return False, 'Такой группы нет :('
            today = datetime.date.today()
            date = datetime.date(today.year, today.month, today.day)
            if date_update == date:
                return group
            else:
                async with aiohttp.ClientSession() as session:
                    async with await session.post(
                            BASE_URL + "?p_p_id=pubStudentSchedule_WAR_publicStudentSchedule10&p_p_lifecycle=2&p_p_resource_id=getGroupsURL&query=",
                            headers={'Content-Type': "application/x-www-form-urlencoded"},
                            params={"p_p_id": "pubStudentSchedule_WAR_publicStudentSchedule10", "p_p_lifecycle": "2",
                                    "p_p_resource_id": "schedule"}, timeout=8) as response:
                        response = await response.json(content_type='text/html')
                if str(response.status_code) != '200':
                    raise ConnectionError
                cursor.execute("UPDATE saved_timetable SET shedule = '{}', date_update = '{}' WHERE groupp = 1".format(
                    json.dumps(response), date))
                connection.commit()
            group, _ = await getGroupsResponse(groupNumber)
            if group:
                return group
            print('Ошибка:\n', traceback.format_exc())
            return False, 'Ошибка'
        except aiohttp.ServerConnectionError:
            return False, "&#9888;Ошибка подключения к серверам.&#9888; \n Вероятно, на стороне kai.ru произошел сбой. Вам необходимо продолжить регистрацию (ввод номера группы) как только сайт kai.ru станет доступным."
        except (ConnectionError, TimeoutError, aiohttp.ServerTimeoutError, aiohttp.ServerConnectionError):
            group, _ = await getGroupsResponse(groupNumber)
            if group:
                return group, ''
            return False, "&#9888;Ошибка подключения к серверам.&#9888; \n Вероятно, на стороне kai.ru произошел сбой. Вам необходимо продолжить регистрацию (ввод номера группы) как только сайт kai.ru станет доступным."
        except:
            group, _ = await getGroupsResponse(groupNumber)
            if group:
                return group
            print('Ошибка:\n', traceback.format_exc())
            return False, 'Ошибка'
