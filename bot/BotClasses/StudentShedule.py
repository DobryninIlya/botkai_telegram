import os
import traceback

import aiohttp, asyncio
import datetime
import json

from pprint import pprint
from .User import User
from .Message import Message
from .Database_connection import cursor, connection, cursorR, conn
from clients.tg.api import TgClient

class StudentShedule:
    def __init__(self, user: User, message: Message, tg_client: TgClient):
        self.user = user
        self.tg_client = tg_client
        self.group_id = user.group_id
        self.BASE_URL = 'https://kai.ru/raspisanie'
        self.today = datetime.date.today()
        self.chetn = int(os.getenv("CHETN"))

    async def alert_for_differences(self, groupname: str, diff: str):
        sql = "SELECT id FROM tg_users WHERE groupname={}".format(groupname)
        cursor.execute(sql)
        result = cursor.fetchall()
        diff += "\n*Изменения уже сохранены.*"
        for elem in result:
            try:
                res = await self.tg_client.send_message(elem[0], diff, parse_mode=True)
                print(res)
            except:
                print('Ошибка:\n', traceback.format_exc(), flush=True)

    async def timetable_differences(self, old: list, new: list):
        week_elements = {
            '1': 'Понедельник',
            '2': 'Вторник',
            '3': 'Среда',
            '4': 'Четверг',
            '5': 'Пятница',
            '6': 'Суббота',
            '7': 'Воскресенье',
        }
        if old != new:
            result = "*Обратите внимание!* \nИзменения в вашем расписании:\n"
            for day in sorted(new.keys()):
                try:
                    if new[day] != old[day]:
                        for lesson in new[day]:
                            if lesson not in old[day]:
                                result += "*(+)*:: `{dayNum}| [{dayTime}] {dayDate} {disciplName}`\n".format(
                                    dayNum=week_elements[lesson['dayNum']],
                                    dayTime=lesson['dayTime'].rstrip(),
                                    dayDate=lesson['dayDate'].rstrip(),
                                    disciplName=lesson['disciplName'].rstrip()
                                )
                except KeyError:
                    print("Ошибка в триггере обновления расписания. День:", day, flush=True)
                    continue
            await self.alert_for_differences(self.user.group_name, result)
            return

    async def _get_response(self):
        sql = "SELECT * FROM saved_timetable WHERE groupp={}".format(self.group_id)
        cursor.execute(sql)
        result = cursor.fetchone()
        if result == None or result[2]=='{}':
            try:
                async with aiohttp.ClientSession() as session:
                    async with await session.post(self.BASE_URL, data="groupId=" + str(self.group_id),
                                                  headers={'Content-Type': "application/x-www-form-urlencoded", "user-agent": "BOT RASPISANIE v.1"},
                                                  params={"p_p_id": "pubStudentSchedule_WAR_publicStudentSchedule10",
                                                          "p_p_lifecycle": "2", "p_p_resource_id": "schedule"},
                                                  timeout=3) as response:
                        response = await response.json(content_type='text/html')
                sql = "INSERT INTO saved_timetable VALUES ({}, '{}', '{}')".format(self.group_id, datetime.date.today(),
                                                                                   json.dumps(response))
                cursor.execute(sql)
                connection.commit()
                return True, response
            except ConnectionError as err:
                return False, "&#9888;Ошибка подключения к серверу типа ConnectionError. Вероятно, сервера КАИ были выведены из строя.&#9888;"
            except aiohttp.ServerTimeoutError as err:
                return False, "&#9888;Ошибка подключения к серверу типа Timeout. Вероятно, сервера КАИ перегружены.&#9888;"
            except:
                print('Ошибка:\n', traceback.format_exc())
                return False, "&#9888;Произошла непредвиденная ошибка :( &#9888;"
        else:
            date_update = result[1]
            timetable = result[2]
            if date_update + datetime.timedelta(days=2) < self.today: # Если старое, то обновить и вернуть
                try:
                    async with aiohttp.ClientSession() as session:
                        async with await session.post(self.BASE_URL, data="groupId=" + str(self.group_id),
                                                      headers={'Content-Type': "application/x-www-form-urlencoded", "user-agent": "BOT RASPISANIE v.1"},
                                                      params={
                                                          "p_p_id": "pubStudentSchedule_WAR_publicStudentSchedule10",
                                                          "p_p_lifecycle": "2", "p_p_resource_id": "schedule"},
                                                      timeout=3) as response:
                            response = await response.json(content_type='text/html')
                    assert json.dumps(response), "Расписание имеет некорректную форму"
                    await self.timetable_differences(json.loads(timetable), response)
                    sql = "UPDATE saved_timetable SET shedule = '{}', date_update = '{}' WHERE groupp = {}".format(
                        json.dumps(response), datetime.date.today(), self.group_id)
                    cursor.execute(sql)
                    connection.commit()
                    return True, response
                except asyncio.exceptions.TimeoutError:
                    print("Ошибка таймаута в расписании", flush=True)
                except:
                    print('Ошибка (расписание):\n', traceback.format_exc(), flush=True)
                    return True, json.loads(timetable)
            else:
                return True, json.loads(timetable)
        return

    def _get_week_shedule(self, response):
        week_elements = {
            '1': 'Понедельник',
            '2': 'Вторник',
            '3': 'Среда',
            '4': 'Четверг',
            '5': 'Пятница',
            '6': 'Суббота',
            '7': 'Воскресенье',
        }
        result = ''
        for key in sorted(response):
            day = response[key]
            result += "═──────{}{}────═\n".format(week_elements[key], '─' * (11 - len(week_elements[key])) if len(
                week_elements[key]) < 11 else '')
            for para in day:
                if '---' in (para["audNum"]).rstrip():  # Экранирование множественных тире
                    para["audNum"] = "--"
                if '---' in (para["buildNum"]).rstrip():
                    para["buildNum"] = "--"
                para_structure = {
                    'dayDate': para["dayDate"][:100].rstrip(),
                    'disciplName': (para["disciplName"]).rstrip(),
                    'audNum': para["audNum"].rstrip(),
                    'buildNum': para["buildNum"].rstrip(),
                    'dayTime': para["dayTime"][:5].rstrip(),
                    'disciplType': para["disciplType"][:4].rstrip()
                }
                result += "➤ *{dayDate} ⌛{dayTime} {disciplType}* _{disciplName}_ {audNum} {buildNum}зд. \n".format(
                    dayDate=para_structure['dayDate'],
                    disciplType=para_structure['disciplType'],
                    disciplName=para_structure['disciplName'],
                    audNum=para_structure['audNum'],
                    buildNum=para_structure['buildNum'],
                    dayTime=para_structure['dayTime']
                )
        return result

    def _get_teacher_list(self, response):
        prepodList = []
        resultList = []
        prepodElement = {'disciplType': None, 'disciplName': None,
                         'prepodName': None}
        for key in response:
            for elem in response[key]:
                prepodElement = {'disciplType': elem["disciplType"].rstrip(),
                                 'disciplName': elem["disciplName"].rstrip(),
                                 'prepodName': elem["prepodName"].rstrip()}
                if elem["prepodName"].rstrip() == "":
                    prepodElement['prepodName'] = ":не-задан:"
                prepodList.append(prepodElement)
        prepodList.sort(key=lambda prepodElement: (prepodElement['disciplName'], prepodElement['prepodName']))
        i = 0
        for prepod in prepodList:
            disciplType = []
            disciplType.append(prepod['disciplType'])
            try:
                while prepod['prepodName'] == prepodList[i + 1]['prepodName']:
                    if prepodList[i + 1]['disciplType'] not in disciplType:
                        disciplType.append(prepodList[i + 1]['disciplType'])
                    prepodList.pop(i)
            except:
                pass
            i += 1
            if disciplType:
                st = ""
                for discipl in disciplType:
                    st += str(discipl).rstrip() + ", "
                st = st[:-2]
                prepod['disciplType'] = st
            res = "👨‍🏫 |" + str(prepod['disciplType']) + "| *" + (
                str(prepod['disciplName'])).rstrip() + "* \n`" + str(prepod['prepodName']).title() + "`"
            if res not in resultList:
                resultList.append(res)
        result = ''
        for row in resultList:
            result += "\n---------------------------------------------------\n" + row
        return result

    async def showTimetable(self, groupId: int, tomorrow=0):
        try:
            isNormal, response = await self._get_response()
            if not isNormal:
                return response
            if tomorrow == -1:
                return self._get_week_shedule(response)  # Расписание по дню недели
            elif tomorrow == -2:
                return self._get_teacher_list(response)  # Список преподов
            elif tomorrow == -3:
                print(self.today.isocalendar()[1] + self.chetn % 2)
                return True if (int(self.today.isocalendar()[1] + self.chetn) % 2) == 0 else False  # Четность недели
            now = datetime.date.today() + datetime.timedelta(days=tomorrow)
            response = response[str(datetime.date(now.year, now.month, now.day).isoweekday())]
            result = ''
            month = now.month
            if month < 10:
                month = "0" + str(month)
            day = str(now.day) + "." + str(month)
            para_list = []
            for elem in response:
                dayDate = elem["dayDate"].rstrip()

                if '---' in (elem["audNum"]).rstrip():  # Экранирование множественных тире
                    elem["audNum"] = "-нет-"
                if '---' in (elem["buildNum"]).rstrip():
                    elem["buildNum"] = "-нет-"

                para_structure = {
                    'dayDate': elem["dayDate"][:100].rstrip(),
                    'disciplName': elem["disciplName"].rstrip(),
                    'audNum': elem["audNum"].rstrip(),
                    'buildNum': elem["buildNum"].rstrip(),
                    'dayTime': elem["dayTime"][:5].rstrip(),
                    'disciplType': elem["disciplType"][:4].rstrip()
                }
                dateinstr = str((elem["dayDate"]).rstrip()).find(day)
                # print((self.today.isocalendar()[1] + self.chetn) % 2, self.today.isocalendar()[1])
                if ((now.isocalendar()[1] + self.chetn) % 2) == 0:  # Если неделя четная
                    chetn = True
                else:
                    chetn = False
                if dayDate == 'чет' and chetn:
                    para_list.append(para_structure)
                elif dayDate == 'неч' and not chetn:
                    para_list.append(para_structure)
                elif dayDate == 'чет\неч' and chetn or dayDate == 'неч\чет' and not chetn:
                    para_structure['dayDate'] = "1️гр. " + para_structure['dayDate']
                    para_list.append(para_structure)
                elif dayDate == 'неч\чет' and chetn or dayDate == 'чет\неч' and not chetn:
                    para_structure['dayDate'] = "2️гр. " + para_structure['dayDate']
                    para_list.append(para_structure)
                elif dateinstr != -1:
                    para_structure['dayDate'] = f"{day} " + para_structure['dayDate']
                    para_list.append(para_structure)
                else:  # No sorted, but can view
                    if dayDate not in ['чет', 'неч', 'чет\неч', 'неч\чет']:
                        para_list.append(para_structure)
            for para in para_list:
                # result += "➤ *{dayDate} ⌛{dayTime} {disciplType}* _{disciplName}_ {audNum} {buildNum}зд. \n".format(
                result += "➤ {dayDate} ⌛{dayTime} {disciplType} ```\n{disciplName}``` {audNum} {buildNum}зд. \n".format(
                    dayDate=para['dayDate'],
                    disciplType=para['disciplType'],
                    disciplName=para['disciplName'],
                    audNum=para['audNum'],
                    buildNum=para['buildNum'],
                    dayTime=para['dayTime']
                )
            return result
        except ConnectionError:
            return "&#9888;Ошибка подключения к серверу типа ConnectionError. Вероятно, сервера КАИ были выведены из строя.&#9888;"
        except aiohttp.ServerTimeoutError:
            return "&#9888;Ошибка подключения к серверу типа Timeout. Вероятно, сервера КАИ перегружены.&#9888;"
        except KeyError:
            return False
        except:
            print('Ошибка:\n', traceback.format_exc())
            return ""
